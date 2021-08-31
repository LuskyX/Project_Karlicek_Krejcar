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
            #town Těšetice has different Wiki page structure, and thus we weren't able to add it into the scraper
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


def prepare_to_convert(string: str) -> list:
    degrees, minutes, seconds = True, True, True
    if string == string.replace("°"," "):
        degrees = False
    if string == string.replace("′"," "):
        minutes = False
    if string == string.replace("″"," "):
        seconds = False
    string = string.replace("°"," ").replace("′"," ").replace("″", " ").split(" ")
    del(string[-1])
    if seconds is False:
        string.append(0)
    if minutes is False:
        string.insert(0, 1)
    if degrees is False:
        string.insert(0, 0)
    for i in range(len(string)):
         string[i] = float(string[i])
    return string


def degrees_to_decimal(degrees: int = 0, minutes: int = 0, seconds: int = 0) -> float:
    result = 0
    result += degrees
    result += minutes/60
    result += seconds/3600
    return result


def reorganize_dataset(dataset: pd.DataFrame) -> pd.DataFrame():
    for i in range(dataset.shape[0]):
        new_long = prepare_to_convert(dataset["Longitude"][i])
        new_lat = prepare_to_convert(dataset["Latitude"][i])
        dataset["Longitude"][i] = degrees_to_decimal(new_long[0], new_long[1], new_long[2])
        dataset["Latitude"][i] = degrees_to_decimal(new_lat[0], new_lat[1], new_lat[2])
    return dataset


def add_town(dataframe: pd.DataFrame, name: str, latitude: float, longitude: float) -> pd.DataFrame:
    new_datapoint = {"Town name": name, "Latitude": latitude, "Longitude": longitude}
    dataframe = dataframe.append(new_datapoint, ignore_index=True)
    return dataframe
