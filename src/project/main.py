import sys
from matplotlib.artist import get
import numpy as np
import pygame
import random

from cities_n_routes import setup_cities_and_routes, setup_path
from pygame_ai_player import PyGameAIPlayer
from util import has_valid_route, get_city_name_from_location
from landscape import get_elevation, elevation_to_rgba
from project.sprite import Sprite
from agent_environment import get_combat_surface, setup_window, displayCityNames, State
from travel_cost import get_route_cost


def main():
    size = width, height = (720, 720)
    # size = width, height = (128, 72)
    window = setup_window(width, height, "CMPSC 441 Final Project")

    screen = pygame.display.set_mode(size)
    elevation = get_elevation(size)
    landscape = elevation_to_rgba(elevation)
    landscape_surface = pygame.surfarray.make_surface(landscape)
    combat_surface = get_combat_surface(size)
    # pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])

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

    city_locations, routes, city_locations_dict = setup_cities_and_routes(
        size, city_names, elevation
    )

    path, routes = setup_path(size, city_names, city_locations, routes)

    # print routes by name
    # print(routes)
    # for route in routes:
    #     print(
    #         get_city_name_from_location(route[0], city_locations_dict),
    #         "to",
    #         get_city_name_from_location(route[1], city_locations_dict),
    #     )

    print(
        "Path: ",
        [get_city_name_from_location(city, city_locations_dict) for city in path],
    )

    print(
        "Cost of path: ",
        get_route_cost(
            path, (elevation - elevation.min()) / (elevation.max() - elevation.min())
        ),
    )

    player_sprite = Sprite("assets/lego.png", path[0])
    player = PyGameAIPlayer()

    state = State(
        current_city=np.where(city_locations == path[0]),
        destination_city=np.where(city_locations == path[-1]),
        travelling=False,
        encounter_event=False,
        cities=city_names,
        routes=routes,
        money=100,
    )

    # game loop
    while True:
        action = player.selectAction(state)
        print("looped")
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                """
                Check if a route exist between the current city and the destination city.
                """
                if not has_valid_route(state, action):
                    print(
                        "No route between", state.current_city, "and", int(chr(action))
                    )
                    continue
                start = city_locations[state.current_city]
                state.destination_city = int(chr(action))
                destination = city_locations[state.destination_city]
                player_sprite.set_location(city_locations[state.current_city])
                state.travelling = True
                print(
                    "Travelling from", state.current_city, "to", state.destination_city
                )
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         sys.exit()

        screen.fill((0, 0, 0))
        screen.blit(landscape_surface, (0, 0))

        # draw cities
        for city in city_locations_dict.values():
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        # draw routes
        for route in routes:
            pygame.draw.line(screen, (0, 255, 0), route[0], route[1], 2)

        # draw text for cities
        displayCityNames(city_locations, city_names, screen)
        # for name, location in city_locations_dict.items():
        #     font = pygame.font.Font(None, 32)
        #     text = font.render(name, True, (0, 0, 255))
        #     screen.blit(text, location)

        # draw path
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (0, 0, 255), path[i], path[i + 1], 3)

        # draw money counter
        font = pygame.font.Font(None, 32)
        text = font.render("Money: " + str(state.money), True, (255, 255, 255))
        screen.blit(text, (width / 2 - text.get_width() / 2, 10))

        pygame.display.flip()


if __name__ == "__main__":
    main()
