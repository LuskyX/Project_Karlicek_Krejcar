import mechanicalsoup
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

    def _extract_links_from_soup(self, soup, region):
        centers_div = soup.select('div[class=center__container]')
        for center in centers_div:
            images = center.find_all('img')
            if 'Bez registrace' in [img['title'] for img in images]:
                name = center.select_one('span[class=center__name]').text
                link = self.url + center.a['href']
                self.vacc_centers.append(VaccCenter(name, region, link))
        return None

