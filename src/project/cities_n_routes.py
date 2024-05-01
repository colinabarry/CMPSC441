""" 
Lab 2: Cities and Routes

In the final project, you will need a bunch of cities spread across a map. Here you 
will generate a bunch of cities and all possible routes between them.
"""

from calendar import c
import random
import itertools

import numpy as np
from ga_cities import game_fitness, setup_GA, solution_to_cities
from util import has_valid_route, routes_to_cities, get_city_name_from_location


def get_randomly_spread_cities(
    size: tuple[int, int], n_cities: int
) -> list[tuple[int, int]]:
    """
    > This function takes in the size of the map and the number of cities to be generated
    and returns a list of cities with their x and y coordinates. The cities are randomly spread
    across the map.

    :param size: the size of the map as a tuple of 2 integers
    :param n_cities: The number of cities to generate
    :return: A list of tuples, each representing a city, with random x and y coordinates.
    """
    # Consider the condition where x size and y size are different
    return [
        (random.randint(0, size[0] - 1), random.randint(0, size[1] - 1))
        for _ in range(n_cities)
    ]


def get_routes(cities):
    """
    It takes a list of cities and returns a list of all possible routes between those cities.
    Equivalently, all possible routes is just all the possible pairs of the cities.

    :param cities: a list of city names
    :return: A list of tuples representing all possible links between cities/ pairs of cities,
                                    each item in the list (a link) represents a route between two cities.
    """
    return list(itertools.combinations(cities, 2))


def get_path_to_city(cities, routes, start, end):
    """Finds a valid route between specified start and end cities.
    Args:
        cities: A list of cities as tuples of coordinates [(x, y)]
        routes: A list of valid routes between cities [((x1, y1), (x2, y2))]
        start: The starting city as a tuple of coordinates (x, y)
        end: The destination city as a tuple of coordinates (x, y)

    Returns:
        A list representing the route [(startx, starty), ..., (endx, endy)]
        if a path exists, otherwise None.
    """

    def dfs(city, visited):
        if city == end:
            result.append(city)
            return True

        visited.add(city)
        for neighbor in find_neighbors(city, routes):
            if neighbor not in visited and dfs(neighbor, visited):
                result.append(city)
                return True

        visited.remove(city)
        return False

    result = []
    visited = set()
    if dfs(start, visited):
        # result.append(start)
        result.reverse()
        return result
    else:
        return None


def find_neighbors(city, routes):
    """Helper to find cities with a direct route from the given city"""
    neighbors = []
    routes = [(tuple(route[0]), tuple(route[1])) for route in routes]

    for route in routes:
        # print("route[0]", route[0], "city", city)
        if route[0] == city:
            neighbors.append(route[1])
        elif route[1] == city:
            neighbors.append(route[0])
    return neighbors


def setup_routes(city_locations):
    routes = get_routes(city_locations)
    random.shuffle(routes)
    routes = routes[:10]
    return routes


def setup_cities_and_routes(size, city_names, landscape):
    city_locations = []
    routes = []

    city_locations = get_randomly_spread_cities(size, len(city_names))
    # print("initial city locations", city_locations)

    landscape = np.array(landscape)
    landscape = (landscape - landscape.min()) / (landscape.max() - landscape.min())

    fitness = lambda ga_inst, solution, idx: game_fitness(
        ga_inst=ga_inst, solution=solution, idx=idx, elevation=landscape, size=size
    )
    fitness_function, ga_instance = setup_GA(fitness, len(city_names), size)

    # Show one of the initial solutions.
    # random_solution = ga_instance.initial_population[0]
    # cities = solution_to_cities(random_solution, size)

    # Run the GA to optimize the parameters of the function.
    ga_instance.run()
    # ga_instance.plot_fitness()
    # print("Final Population")

    # Show the best solution after the GA finishes running.
    best_solution = ga_instance.best_solution()[0]
    # print("best solution: ", best_solution)
    city_locations = solution_to_cities(best_solution, size)
    # print("city locations: ", city_locations)
    # print(fitness_function(ga_inst=ga_instance, solution=city_locations, idx=0))

    city_locations_dict = {
        name: location for name, location in zip(city_names, city_locations)
    }

    routes = setup_routes(city_locations)

    return (
        [tuple(city) for city in city_locations],
        [(tuple(route[0]), tuple(route[1])) for route in routes],
        city_locations_dict,
    )


def setup_path(size, city_names, city_locations, routes, min_path_length=5):
    city_locations_copy = [tuple(city) for city in city_locations]
    # print("city locations_copy", city_locations_copy)

    start = random.choice(city_locations_copy)
    # print("start", start)
    city_locations_copy.remove(start)

    end = random.choice(city_locations_copy)
    # print("end", end)
    city_locations_copy.remove(end)

    path = get_path_to_city(city_locations, routes, start, end)

    while path is None or len(path) < min_path_length:
        # print("invalid path, trying again")
        if len(city_locations_copy) < 1:
            routes = setup_routes(city_locations)
            city_locations_copy = [tuple(city) for city in city_locations]
        end = random.choice(city_locations_copy)
        # city_locations_copy = np.delete(city_locations_copy, end)
        city_locations_copy.remove(end)
        path = get_path_to_city(city_locations, routes, start, end)

    return path, routes


# TODO: Fix variable names
if __name__ == "__main__":
    city_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

    """print the cities and routes"""
    cities = get_randomly_spread_cities((100, 200), len(city_names))
    routes = get_routes(cities)
    random.shuffle(routes)
    routes = routes[:10]
    print("Cities:")
    for i, city in enumerate(cities):
        print(f"{city_names[i]}: {city}")
    print("Routes:")
    for i, route in enumerate(routes):
        print(f"{i}: {route[0]} to {route[1]}")

    cities_copy = cities.copy()
    start = random.choice(cities_copy)
    cities_copy.remove(start)
    end = random.choice(cities_copy)

    print("start", start, "end", end)
    path = get_path_to_city(cities, routes, start, end)
    print(path)
