import mechanicalsoup
import requests
from bs4 import BeautifulSoup
from time import sleep
from config import URL_VACCENTERS, REGIONS
from data_structures import VaccCenter

class VaccCentersScraper():
    url = URL_VACCENTERS

    def __init__(self, regions=REGIONS):
        self.regions = regions
        self.vacc_centers = []

    def get_links(self):
        browser = mechanicalsoup.StatefulBrowser(raise_on_404=True)
        for reg in self.regions:
            browser.open(self.url)
            form = browser.select_form('form[id=filter]')
            form['FilteredByRegion'] = reg
            response = browser.submit_selected()
            self._extract_links_from_soup(BeautifulSoup(response.text.strip()), reg)
            sleep(1)
        browser.close()
        return None

    def get_information_about_centers(self):
        for center in self.vacc_centers:
            print(center.link)
            soup = BeautifulSoup(requests.get(center.link).text.strip())
            center.add_info(self._extract_info_from_soup(soup))
            center.add_open_hours(self._extract_open_hours_from_soup(soup))
            sleep(0.5)
        return None


    def _extract_links_from_soup(self, soup, region):
        centers_div = soup.select('div[class=center__container]')
        for center in centers_div:
            images = center.find_all('img')
            if 'Bez registrace' in [img['title'] for img in images]:
                no_registration = 1
            else:
                no_registration = 0
            name = center.select_one('span[class=center__name]').text
            link = self.url + center.a['href']
            self.vacc_centers.append(VaccCenter(name, region, link, no_registration))
        return None

    @staticmethod
    def _extract_info_from_soup(soup):
        table_info = soup.select('div[class=info] > table > tbody > tr')
        info = {i.select_one('td:nth-child(1)').text: i.select_one('td:nth-child(2)').text.replace("\r\n", "")
                for i in table_info[0:4]}
        info['Poznámka'] = table_info[4].select_one('td:nth-child(2)').text.replace("\t", " ").replace("\r\n", "")

        info['Vakcíny'] = [t.text for t in table_info[5].select_one('td:nth-child(2)').select('div[class=vaccineName]')]

        info['Dodatečné informace'] = [t.text.replace("👨\u200d🦽 ", "") for t in
                                       table_info[6].select_one('td:nth-child(2)').select('span')]

        info['Denní kapacita očkování'] = table_info[7].select_one('td:nth-child(2)').text.replace("\r\n", "")

        info['Způsob změny termínu druhé dávky vakcíny'] = [t.text.replace('\n', '') for t in
                                                            table_info[8].select_one('td:nth-child(2)' ).select('div')]
        return info

    @staticmethod
    def _extract_open_hours_from_soup(soup):
        open_table = soup.select('div[class=detail__aside] > div[class=opening] > table > tbody > tr')
        open_table = {i.select_one('td:nth-child(1)').text: i.select_one('td:nth-child(2)').text.strip().replace(" ", "")
                      for i in open_table}
        for day in open_table:
            hours = open_table[day].split("-")
            if hours[0] in ["Zavřeno", "Žádnádata"]:
                open_table[day] = [None, None]
            else:
                open_table[day] = [float(hours[0][:2]) + (float(hours[0][3:]) / 60),
                                   float(hours[1][:2]) + (float(hours[1][3:]) / 60)]
        return open_table


if __name__ == '__main__':
    v = VaccCentersScraper()
    v.get_links()
    v.get_information_about_centers()
    centers = v.vacc_centers
    centers[0].name
    centers[0].region
    centers[0].info
    centers[0].open_hours