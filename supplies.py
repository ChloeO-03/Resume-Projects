"""
Module: supplies

An application to solve the Disaster Planning problem.

Authors:
1. Parter A's Name
2. Melissa Vargas Medina
"""
from sys import argv, exit
import re

class InvalidFileFormatError(Exception):
    pass

def parse_network_data(filename: str) -> tuple[dict[str, set[str]], dict[str, tuple[int,int]]]:
    """
    Reads city connection data <filename>, returning a dictionary that
    associates each city with the set of cities that are directly connected to
    it.

    DO NOT MODIFY THIS FUNCTION IN ANY WAY!!!!!

    Parameters:
        filename (str): Name of the file containing city connections.

    Returns:
        (tuple[dict[str, set[str]], dict[str, tuple[int,int]]]): Two dictionaries:
            (1) The cities and the set of cities they are directly connected
            (2) The "logical" location of these cities.
    """
    network = {}
    location = {}

    with open(filename, 'r') as f:
        for line in f:
            clean_line = line.strip()

            # skip over comment lines (start with a '#') and blank lines
            if len(clean_line) == 0 or clean_line[0] == '#':
                continue

            # use a regular expression to parse this line, pulling out the
            # city as well as comma separated list of neighbors.
            match = re.fullmatch("(?P<city>[\w\-\. ]+)\s+\((?P<x>\d+),\s*(?P<y>\d+)\):(\s+(?P<neighbors>[\w\-\. ]+(,\s+[\w\-\. ]+)*))?", clean_line)
            if not match:
                raise InvalidFileFormatError(f"Invalid line: {clean_line}")

            #print("Match:", clean_line)
            city = match.group('city')
            x_loc = int(match.group('x'))
            y_loc = int(match.group('y'))
            location[city] = (x_loc, y_loc)

            neighbors = match.group('neighbors')
            if neighbors is None:
                continue

            listed_neighbors = {n.strip() for n in neighbors.split(',')}

            # add a link from this city to all the listed neighbors
            network[city] = network.get(city, set()) | listed_neighbors

            # add a link back from each listed neighbor to this city
            for n in listed_neighbors:
                n_neighbors = network.get(n, set())
                n_neighbors.add(city)
                network[n] = n_neighbors


    return network, location


def is_covered(road_network, supply_locations, city):
    """ 
    Test whether the city is covered or not

    Parameters:
    road_network (dict[str, set[str]]): A dictionary representing the road network where each key is a city and its value is a set of cities directly connected to it.
    supply_locations (set[str]): A set of cities that are designated as supply locations.
    city (str): The city to check for coverage.
    
    Returns:
    bool: True if the city is covered, False otherwise.
 
    """
    # Create a set containing the input city and all cities directly connected to it in the road network
    return len(({city}|(road_network[city])) & (supply_locations)) > 0 

def uncovered_cities(road_network, supply_locations):
    """
    finds the list of cities that havent been covered yet

    Parameters:
    road_network (dict[str, set[str]]): A dictionary representing the road network where each key is a city and its value is a set of cities directly connected to it.
    supply_locations (set[str]): A set of cities that are designated as supply locations.
    
    Returns:
    list: A list of uncovered cities.

    """
    # Initialize to store uncovered cities.
    uc = []
    # Iterate over all cities in the road network.
    for c in road_network.keys():
        if not is_covered(road_network, supply_locations, c):
             # If not covered, append the city to the list of uncovered cities.
            uc.append(c)
    # Return the list of uncovered cities.
    return uc

def can_be_disaster_ready(road_network: dict[str, set[str]], num_cities: int, supply_locations: set[str]) -> bool:
    """
    This fuction determines if every city in a road network should be considered disater ready: which is determined by if they have the
    proper resources and access to supply locations. 

     Parameters:
     road_network (dict[str, set[str]]): A dictionary representing the road network where each key is a city and its value is a set of cities directly connected to it.
     num_cities (int): The total number of cities in the road network.
     supply_locations (set[str]): A set of cities that are designated as supply locations.

    Returns:
     bool: True if all cities are disaster ready, False otherwise.

    """
    #esnures the number of cities is a non-neg
    assert num_cities >= 0 

    #finds the loist of cities that are still in need of diaster supplies 
    uc = uncovered_cities(road_network, supply_locations)

    # If there are more supply locations than cities, the network can't be fully covered
    if len(supply_locations) > num_cities:
        return False
     # If all cities are covered, return True
    if len(uc) == 0:
        return True 

    # Choose an uncovered city
    uncv_city = uc[0] 
    possible = {uncv_city}.union(road_network[uncv_city])  #tutoring unioun example: The union of {1, 2, 3} and {2, 3, 4} is the set {1, 2, 3, 4} 

    # Placing supplies in each possible location and recursively check.
    for city in possible:
        supply_locations.add(city)
        if can_be_disaster_ready(road_network, num_cities, supply_locations):
            return True 
        else:
            supply_locations.remove(city)
 # If no solution found, return False
    return False

if __name__ == "__main__":
    if len(argv) != 3:
        print("Error: wrong number of command line parameters")
        exit(1)

    n, _ = parse_network_data(argv[1])
    max_num_cities = int(argv[2])

    supply_cities: set[str] = set()

    ok = can_be_disaster_ready(n, max_num_cities, supply_cities)
    if ok:
        print("Supply Locations:", supply_cities)
        assert len(supply_cities) <= max_num_cities, f"Problem constraint has been voilated: too many cities ({len(supply_cities)}) selected!"
    else:
        print("No solution possible!")