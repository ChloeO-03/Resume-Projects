"""
Module: test_supplies


PyTest Unit Test cases for COMP120 PSA5 (Disaster Planning)
"""


import pytest


# the following is the module(s) we are testing
import supplies


def create_network(connected_pairs: list[tuple[str,str]]) -> dict[str,set[str]]:
   """Creates a road network, given a list of pairs of cities that are
   connected to each other.


   >>> create_network([("San Diego", "Los Angeles")])
   {'San Diego': {'Los Angeles'}, 'Los Angeles': {'San Diego'}}
   >>> network = create_network([("San Diego", "Los Angeles"), ("San Diego", "Tijuana")])
   >>> network == {'San Diego': {'Tijuana', 'Los Angeles'}, 'Los Angeles': {'San Diego'}, 'Tijuana': {'San Diego'}}
   True
   """


   network = {}


   for city1, city2 in connected_pairs:
       # Add the cities to the network if we haven't seen them yet.
       if city1 not in network:
           network[city1] = set()
       if city2 not in network:
           network[city2] = set()


       # add connection from city 1 to city 2
       network[city1].add(city2)


       # add connection from city 2 to city 1
       network[city2].add(city1)


   return network


def test_negative_max_cities():
   """Tests that when num_cities is negative, the precondition check raises
   an assertion."""


   with pytest.raises(AssertionError):
       result = supplies.can_be_disaster_ready({}, -1, set())




def test_max0_bad():
   """Test the base case of when num_cities is 0 and supply_locations is
   empty, so no way to cover the cities."""


   network = create_network([("San Diego", "Tijuana"),
                             ("San Diego", "Los Angeles"),
                             ("Los Angeles", "Palm Springs")])


   result = supplies.can_be_disaster_ready(network, 0, set())
   assert result == False




def test_too_many_supply_cities():
   """Test the base case of when the number of cities in supply_cities is
   greater than num_cities (should return False)."""


   network = create_network([("San Diego", "Tijuana"),
                             ("San Diego", "Los Angeles"),
                             ("Los Angeles", "Palm Springs")])


   supply_cities = set(['San Diego', 'Los Angeles'])
   result = supplies.can_be_disaster_ready(network, 1, supply_cities)


   assert result == False




def test_socal_bad():
   """Test the recursive case of when num_cities is 1, which isn't enough to
   cover all the cities."""


   network = create_network([("San Diego", "Tijuana"),
                             ("San Diego", "Los Angeles"),
                             ("Los Angeles", "Palm Springs")])


   # test with 1 cities (not possible)
   result = supplies.can_be_disaster_ready(network, 1, set())
   assert result == False




def test_socal_ok():
   """Test recursive case where num_cities is enough to cover all of the
   cities."""


   network = create_network([("San Diego", "Tijuana"),
                             ("San Diego", "Los Angeles"),
                             ("Los Angeles", "Palm Springs")])


   actual_supply_cities = set() # start off with no supply cities
   result = supplies.can_be_disaster_ready(network, 2, actual_supply_cities)


   expected_supply_cities = set(['Los Angeles', 'San Diego'])


   # check that result was true and that supply cities are SD and LA
   assert result == True
   assert ('Palm Springs' in actual_supply_cities or "Los Angeles" in actual_supply_cities) and ('San Diego' in actual_supply_cities or "Tijuana" in actual_supply_cities)




# TODO: Complete all of the test functions below.
# DO NOT modify any of the test functions above here.


def test_base_case_ok():
   """Test case where the given supply cities cover all of the cities WITHOUT
   adding any more cities as supply locations."""
   road_network = { "A": {"B", "C"}, "B": {"A", "C"}, "C": {"A", "B"}  }  # a simple road network where each city is directly connected to every other city.
   supply_locations = {"A", "B", "C"} # The set of supply locations containing all cities in the road network.
   num_cities = 3 #  the total number of cities in the road network.
   # checks that the can_be_disaster_ready function returns True when the given supply cities, covers all the cities in the road network without requiring additional supply
   assert supplies.can_be_disaster_ready(road_network, num_cities, supply_locations) == True
   #needs to be supplies. so that it can recongize where the fucntion can be found (did not work when it just can_be_diaster_ready)






def test_counter_intuitive_example():
   """Tests the "Counter-Intuitive Stockpiling" example from the PSA
   specifications (i.e. the "Ethane" example), checking that it returns False
   when num_cities is 1 and returns True when num_cities is 2 or 3."""
  
   network = create_network([("San Diego", "Los Angeles"), ("San Diego", "Tijuana"), ("Los Angeles", "Palm Springs")])
   # Test with num_cities as 1
   result_1 = supplies.can_be_disaster_ready(network, 1, set())
   assert result_1 == False
   # Test with num_cities as 2
   result_2 = supplies.can_be_disaster_ready(network, 2, set())
   assert result_2 == True
   # Test with num_cities as 3
   result_3 = supplies.can_be_disaster_ready(network, 3, set())
   assert result_3 == True


def test_dont_be_greedy_example():
   """Tests the "Don't Be Greedy" example from the PSA
   specifications, checking that it returns False when num_cities is 1 and
   returns True when num_cities is 2 or 3."""


   result = supplies.can_be_disaster_ready
   if result == 1:
       return False
   elif result==2 or result ==3:
       return True



<<<<<<< HEAD
=======
    result = supplies.can_be_disaster_ready
    if result == 1:
        return False
    elif result==2 or result ==3:
        return True

>>>>>>> c6259ddd7405265bc6097f4ae3e46013d6521a24

if __name__ == "__main__":
   pytest.main(['test_supplies.py'])




