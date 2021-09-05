from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
from config import BASE_URL, PRAGUE_URL, LOCATIONS_URL, WRONG_WIKI
from tools.data_classes import Location


class LocationsScrapper:
    """
    This class searches for all possible town names in CZE and scrapes Wikipedia for their Latitude and Longitude,
    which will be further used in the project.
    """
    url = BASE_URL
    url_prague = BASE_URL + PRAGUE_URL
    locations_url = BASE_URL + LOCATIONS_URL

    def __init__(self):
        self.links = []
        self.locations = []

    def get_links(self):
        """
        Downloads links for town in CZ and links for parts of Prague, store them in self.links
        """
        soup = BeautifulSoup(requests.get(self.locations_url).text.strip(), features="lxml")
        for region in soup.select('td[class="navbox-list navbox-odd"]'):
            self.links.extend(region.div.find_all('a'))

        soup_prague = BeautifulSoup(requests.get(self.url_prague).text.strip(), features="lxml")
        table_prague = soup_prague.findAll('table', {"class": "wikitable"})[3]
        for prague_parts in table_prague.select("tr > td:nth-child(3)"):
            self.links.extend(prague_parts.find_all('a'))

        self.links = [self.url + i['href'] for i in self.links]
        self.links.append(self.url_prague)
        return None

    def get_gps(self) -> None:
        """
        download location coordinates from self.links, then create instance of Location and store it in self.locations
        """
        for link in tqdm(self.links):
            soup = BeautifulSoup(requests.get(link).text.strip(), features="lxml")
            name = soup.h1.text
            if name in WRONG_WIKI:
                # town Těšetice has different Wiki page structure, and thus we weren't able to add it into the scraper
                self.locations.append(Location(name, WRONG_WIKI[name]))
            else:
                lat = str(soup.select('span[style="white-space:pre"]')[0]).split(">")[1].split(" s")[0]
                lat = self._degrees_to_decimal(*self._prepare_to_convert(lat))
                long = str(soup.select('span[style="white-space:pre"]')[1]).split(">")[1].split(" v")[0]
                long = self._degrees_to_decimal(*self._prepare_to_convert(long))
                self.locations.append(Location(name, (lat, long)))
            sleep(0.1)
        return None

    @staticmethod
    def _prepare_to_convert(coordinates: str) -> tuple:
        """
        Converts string of coordinates to tuple of ints
        """
        degrees, minutes, seconds = True, True, True

        if coordinates == coordinates.replace("°", " "): degrees = False
        if coordinates == coordinates.replace("′", " "): minutes = False
        if coordinates == coordinates.replace("″", " "): seconds = False

        coordinates = coordinates.replace("°", " ").replace("′", " ").replace("″", " ").split(" ")
        del (coordinates[-1])

        if seconds is False: coordinates.append(0)
        if minutes is False: coordinates.insert(0, 1)
        if degrees is False: coordinates.insert(0, 0)

        for i in range(len(coordinates)):
            coordinates[i] = float(coordinates[i])
        return tuple(coordinates)

    @staticmethod
    def _degrees_to_decimal(degrees: int = 0, minutes: int = 0, seconds: int = 0) -> float:
        """
        Converts degree format to decimal format
        """
        result = 0
        result += degrees
        result += minutes / 60
        result += seconds / 3600
        return result
