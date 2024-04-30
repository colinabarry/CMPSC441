import sys
import pygame
import random
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, elevation_to_rgba, get_elevation
from pygame_ai_player import PyGameAIPlayer
from util import has_valid_route
from cities_n_routes import get_randomly_spread_cities, get_routes


get_combat_bg = lambda pixel_map: elevation_to_rgba(get_elevation(pixel_map), "RdPu")

pygame.font.init()
game_font = pygame.font.Font(None, 32)


def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names, screen):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])


class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
        money,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes
        self.money = money


if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    screen = setup_window(width, height, "Game World Gen Practice")

    landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
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

    city_locations = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(city_locations)

    random.shuffle(routes)
    routes = routes[:10]
    print("routes: ", routes)

    player_sprite = Sprite(sprite_path, city_locations[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=city_locations,
        routes=routes,
        money=100,
    )

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

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in city_locations:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(city_locations, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print("Arrived at", state.destination_city)

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            run_pygame_combat(combat_surface, screen, player_sprite)
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print("You have reached the end of the game!")
            break