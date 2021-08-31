from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


def scrape_dataset() -> pd.DataFrame:
    """
    This functions searches for all possible town names in CR and scrapes Wikipedia for their Latitude and Longitude,
    which will be further used in the project. It collects the data and assemblies a pd.DataFrame, which was further
    stored in .csv format. Function prints out the progress - it takes circa 45 minutes to complete the scraping,
    so the dataset was manually imported into the repository for simplicity.

    Input: Due to the monotonous objective of the function, no input needed.

    Output: A pd.DataFrame

    """
    url = "https://cs.wikipedia.org/"
    r = requests.get("https://cs.wikipedia.org/wiki/Seznam_obc%C3%AD_v_Česku")
    soup = BeautifulSoup(r.text.strip())
    data = []
    links = []
    for region in soup.select('td[class="navbox-list navbox-odd"]'):
        links.extend(region.div.find_all('a'))
    links = [url + i['href'] for i in links]
    print(f"Number of town availiable is: {len(links)}")
    i = 1
    for town in links:
        if BeautifulSoup(requests.get(town).text.strip()).h1.text == "Těšetice (okres Znojmo)":
            i += 1
            continue
        else:
            print(
                f"Currently scraping {i}/{len(links)} of the towns possible - currently {BeautifulSoup(requests.get(town).text.strip()).h1.text}")
            r = requests.get(town).text.strip()
            ss = str(BeautifulSoup(r).select('span[style="white-space:pre"]')[0]).split(">")[1].split(" s")[0]
            vd = str(BeautifulSoup(r).select('span[style="white-space:pre"]')[1]).split(">")[1].split(" v")[0]
            name = BeautifulSoup(r).h1.text
            data.append([name, ss, vd])
            i += 1
    data = pd.DataFrame(data)
    data.columns = ["Town name", "Latitude", "Longitude"]
    return data