"""
Lab 3: Travel Cost

Your player will need to move from one city to another in order to complete the game.
The player will have to spend money to travel between cities. The cost of travel depends 
on the difficulty of the terrain.
In this lab, you will write a function that calculates the cost of a route between two cities,
A terrain is generated for you 
"""

import numpy as np
from numpy.typing import NDArray
from numpy import float_


def get_route_cost(
    route_coordinate: list[tuple[int, int]], game_map: NDArray[float_]
) -> float:
    """
    This function takes in a route_coordinate as a tuple of coordinates of cities to connect,
    example:  and a game_map as a numpy array of floats,
    remember from previous lab the routes looked like this: [(A, B), (A, C)]
    route_coordinates is just inserts the coordinates of the cities into a route like (A, C).
    route_coordinate might look like this: ((0, 0), (5, 4))

    For each route this finds the cells that lie on the line between the
    two cities at the end points of a route, and then sums the cost of those cells

          1 | A |   |   |
            |-----------|
          2 |   |   |   |
            |-----------|
          3 |   | C |   |
            -------------
              I   J   K

    Cost between cities A and C is the sum of the costs of the cells
                                    I1, I2, J2 and J3.
    Alternatively you could use a direct path from A to C that uses diagonal movement, like
                                    I1, J2, J3

    :param route_coordinates: a list of tuples of coordinates of cities to connect
    :param game_map: a numpy array of floats representing the cost of each cell

    :return: a floating point number representing the cost of the route
    """
    # Build a path from start to end that looks like [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 4)]

    # Get the start and end coordinates from the first two elements in route_coordinate list
    start, end = route_coordinate[0], route_coordinate[1]
    path = [start]
    step = start

    # print(start, end)

    # Initialize the map with '-'
    map_size = game_map.shape
    terrain_map = np.full(map_size, " - ", dtype="<U3")

    # Set the start and end positions
    terrain_map[start] = " S "
    terrain_map[end] = " E "

    step_count = 1

    while step != end:
        x, y = step
        x_end, y_end = end

        if x < x_end:
            x += 1
        elif x > x_end:
            x -= 1

        if y < y_end:
            y += 1
        elif y > y_end:
            y -= 1

        step = (x, y)
        path.append(step)

        # Update the map with the step count
        # terrain_map[step] = str(step_count)
        terrain_map[step] = str(step_count).rjust(3)
        step_count += 1

    # print(
    #     np.array2string(terrain_map, separator="", formatter={"str_kind": lambda x: x})
    # )
    return int(game_map[tuple(zip(*path))].sum())


def route_to_coordinates(city_locations, city_names, routes):
    """get coordinates of each of the routes from cities and city_names"""
    route_coordinates = []
    for route in routes:
        start = city_names.index(route[0])
        end = city_names.index(route[1])
        route_coordinates.append((city_locations[start], city_locations[end]))
    return route_coordinates


def generate_terrain(map_size: tuple[int, int]) -> NDArray[float_]:
    """generate a terrain map of size map_size"""
    return np.random.rand(*map_size)


def main():
    # Ignore the following 4 lines. This is bad practice, but it's just to make the code work in the lab.
    import sys
    from pathlib import Path

    sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
    from lab2.cities_n_routes import get_randomly_spread_cities, get_routes

    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]
    map_size = 480, 360

    n_cities = len(city_names)
    game_map: NDArray[float_] = generate_terrain(map_size)
    print(f"Map size: {game_map.shape}")

    city_locations: list[tuple[int, int]] = get_randomly_spread_cities(
        map_size, n_cities
    )
    routes = get_routes(city_names)
    np.random.shuffle(routes)
    routes = routes[:10]
    route_coordinates = route_to_coordinates(city_locations, city_names, routes)
    # print(route_coordinates)

    for route, route_coordinate in zip(routes, route_coordinates):
        path = get_route_cost(route_coordinate, game_map)
        print(f"Cost between {route[0]} and {route[1]}: {path}")


if __name__ == "__main__":
    main()
