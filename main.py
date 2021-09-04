import heapq as hq
from geopy import distance
from database_connector import DatabaseConnector
from vaccination_centers_scrapper import VaccCentersScraper
from location_scraper import LocationsScrapper
from query_creator import create_query
from data_classes import VaccCenter
from config import FINAL_QUERY
from datetime import datetime


def main(location="Praha 3", vaccine=None, age_group="adult", without_registration=None, self_payer=False, monday=None,
         tuesday=None, wednesday=None, thursday=None, friday=None, saturday=None, sunday=None, update=False):
    db = DatabaseConnector(update=update)
    if update:
        _update_vacc_centers(db)
        _update_locations(db)

    query = create_query(vaccine, age_group, without_registration, self_payer, monday, tuesday, wednesday, thursday,
                         friday, saturday, sunday)
    centers_gps = db.get_data(query)
    if len(centers_gps) == 0:
        raise Exception()
    elif len(centers_gps) <= 3:
        vacc_ids = [center[0] for center in centers_gps]
    else:
        location_gps = _get_location_gps(db, location)
        vacc_ids = three_closest_centers(location_gps, centers_gps)
    final_centers = _get_vaccine_centers(db, vacc_ids)
    for center in final_centers:
        print(center)


def three_closest_centers(location: tuple, centers: list) -> list:
    """
    :param coords: A tuple of both latitude and longitude of a given center
    :param other_centers: A list of tuples containing longitude and latitude of all other centers
    :param display_distances: If True, it also prints out the values of the calculated smallest distances
    :return: returns a list of three centers which are the closest from centre defined by coords (list[0] being the closest one)
    For the calculation of three smallest numbers, we used a Heap and Heapsort thanks to its low time and space complexity.
    """
    distances = []
    for center in centers:
        distances.append(distance.distance(location, (center[1], center[2])).km)
    closest_centers = hq.nsmallest(3, distances)
    # let's now extract the index and coordinates later
    indices = [distances.index(facility) for facility in closest_centers]
    # now having the indices of the closest centres, simply return out the three closest coordinates
    result = [centers[index] for index in indices]
    return [center[0] for center in result]


def _get_vaccine_centers(db, vacc_ids):
    centers = []
    for vacc_id in vacc_ids:
        query = FINAL_QUERY + f'"{vacc_id}"'
        data = db.get_data(query)[0]
        center = VaccCenter(data[1], data[2], data[3])
        center.add_open_hours({'monday': [data[4], data[5]], 'tuesday': [data[6], data[7]], 'wednesday': [data[8], data[9]],
                               'thursday': [data[10], data[11]], 'friday': [data[12], data[13]], 'saturday': [data[14], data[15]],
                               'sunday': [data[16], data[17]]})
        center.add_info({'address': data[18], 'address_spec': data[19], 'phone': data[20], 'email': data[21], 'note': data[22],
                         'vaccines': data[23], 'add_info': data[24], 'capacity': data[25], 'changing_date': data[26]})
        centers.append(center)
    return centers


def _get_location_gps(db, location):
    query_loc = f"""
    SELECT latitude, longitude
    FROM locations
    WHERE name = "{location}"
    """
    location_gps = db.get_data(query_loc)
    if len(location_gps) == 0: raise Exception
    return location_gps[0]


def _update_vacc_centers(db):
    vacc_scrap = VaccCentersScraper()
    vacc_scrap.get_links()
    vacc_scrap.get_information_about_centers()
    vacc_scrap.get_gps_of_centers()
    for center in vacc_scrap.vacc_centers:
        db.insert_vacc_center(center)


def _update_locations(db):
    loc_scrap = LocationsScrapper()
    loc_scrap.get_links()
    loc_scrap.get_gps()
    for location in loc_scrap.locations:
        db.insert_into_locations(location.name, location.gps)


if __name__ == '__main__':
    start = datetime.now()
    main(update=False, vaccine="Vaxzevria")
    end = datetime.now()
    print("\n \n \n \n")
    print((end - start).total_seconds())
