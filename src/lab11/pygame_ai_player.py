import random
from lab11.turn_combat import CombatPlayer
from lab11.util import has_valid_route, routes_to_cities


""" Create PyGameAIPlayer class here"""

# For reference:
# state = State(
#         current_city=start_city,
#         destination_city=start_city,
#         travelling=False,
#         encounter_event=False,
#         cities=city_locations,
#         routes=routes,
#     )


class PyGameAIPlayer:
    all_cities = list(range(10))
    non_visited_cities = all_cities.copy()

    def selectAction(self, state):
        # update non_visited_cities
        if state.current_city in self.non_visited_cities:
            self.non_visited_cities.remove(state.current_city)

        # pick a random city from the non_visited_cities
        random_destination = random.choice(self.non_visited_cities)
        has_route = has_valid_route(state, ord(str(random_destination)))

        possible_destinations = self.non_visited_cities.copy()

        while not has_route:
            possible_destinations.remove(random_destination)

            if len(possible_destinations) == 0:
                self.non_visited_cities = self.all_cities.copy()
                self.non_visited_cities.remove(state.current_city)
                possible_destinations = self.non_visited_cities.copy()
                print("backtracking")

            random_destination = random.choice(possible_destinations)

            has_route = has_valid_route(state, ord(str(random_destination)))
            print(
                "has_route from %s to %s: %s"
                % (
                    state.current_city,
                    random_destination,
                    has_route,
                )
            )

        print("destination: %s" % random_destination)
        destination = ord(str(random_destination))
        return destination


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        choice = random.randint(1, 3)
        self.weapon = choice - 1
        return self.weapon
