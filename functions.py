import heapq as hq
from geopy import distance



def three_closest_centers(coords: tuple, other_centers: list, display_distances: bool = False) -> list:
    """
    :param coords: A tuple of both latitude and longitude of a given center
    :param other_centers: A list of tuples containing longitude and latitude of all other centers
    :param display_distances: If True, it also prints out the values of the calculated smallest distances
    :return: returns a list of three centers which are the closest from centre defined by coords (list[0] being the closest one)
    For the calculation of three smallest numbers, we used a Heap and Heapsort thanks to its low time and space complexity.
    """
    distances = []
    for centre in other_centers:
        delta = distance.distance(coords, centre)
        distances.append(delta)
    closest_centers = hq.nsmallest(3, distances)
    # let's now extract the index and coordinates later
    indices = [distances.index(facility) for facility in closest_centers]
    # now having the indices of the closest centres, simply return out the three closest coordinates
    result = [other_centers[index] for index in indices]
    if display_distances is True:
        print(f"The respective distances are: {closest_centers}")
    return result