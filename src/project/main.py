import sys
from matplotlib.artist import get

import pygame
from cities_n_routes import get_randomly_spread_cities, get_routes, get_path_to_city
from util import get_city_name_from_location
from landscape import get_landscape
import random


def setup_cities_and_routes(size, city_names):
    city_locations = []
    routes = []

    city_locations = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(city_locations)

    city_locations_dict = {
        name: location for name, location in zip(city_names, city_locations)
    }
    random.shuffle(routes)
    routes = routes[:10]

    return city_locations, routes, city_locations_dict


def main():
    pygame.init()
    size = width, height = (128, 72)

    screen = pygame.display.set_mode(size)
    landscape = get_landscape(size)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])

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

    # city_locations, routes, city_locations_dict = [], [], {}

    city_locations, routes, city_locations_dict = setup_cities_and_routes(
        size, city_names
    )
    # city_locations = []
    # routes = []

    # city_locations = get_randomly_spread_cities(size, len(city_names))
    # routes = get_routes(city_locations)

    # city_locations_dict = {
    #     name: location for name, location in zip(city_names, city_locations)
    # }
    # random.shuffle(routes)
    # routes = routes[:10]

    city_locations_copy = city_locations.copy()
    start = random.choice(city_locations_copy)
    city_locations_copy.remove(start)
    end = random.choice(city_locations_copy)
    city_locations_copy.remove(end)

    path = get_path_to_city(city_locations, routes, start, end)

    while path is None or len(path) < 5:
        print("invalid path, trying again")
        if len(city_locations_copy) < 1:
            city_locations, routes, city_locations_dict = setup_cities_and_routes(
                size, city_names
            )
            city_locations_copy = city_locations.copy()
        end = random.choice(city_locations_copy)
        city_locations_copy.remove(end)
        path = get_path_to_city(city_locations, routes, start, end)

    # print routes by name
    # print(routes)
    for route in routes:
        print(
            get_city_name_from_location(route[0], city_locations_dict),
            "to",
            get_city_name_from_location(route[1], city_locations_dict),
        )

    print([get_city_name_from_location(city, city_locations_dict) for city in path])

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        screen.blit(pygame_surface, (0, 0))

        # draw cities
        for city in city_locations_dict.values():
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        # draw routes
        for route in routes:
            pygame.draw.line(screen, (0, 255, 0), route[0], route[1], 2)

        # draw text for cities
        for name, location in city_locations_dict.items():
            font = pygame.font.Font(None, 32)
            text = font.render(name, True, (0, 0, 255))
            screen.blit(text, location)

        pygame.display.flip()


if __name__ == "__main__":
    main()
