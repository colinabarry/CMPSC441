import numpy as np


def has_valid_route(state, action, city_from=None):
    if city_from is None:
        city_from = state.current_city

    action_value = int(chr(action))

    if 0 <= action_value <= 9:
        if action_value != state.current_city:
            city_routes = routes_to_cities(state)
            # print("city_routes", city_routes)
            # print("city_from", city_from)
            # print("action_value", action_value)

            if (
                city_from,
                action_value,
            ) in city_routes or (
                action_value,
                city_from,
            ) in city_routes:
                return True

            return False
    return False


def routes_to_cities(state):
    cities = []
    for route in state.routes:
        # print("route", route)
        # print("state.cities", state.cities)
        start = route[0]
        end = route[1]

        if start in state.cities and end in state.cities:
            cities.append((state.cities.index(start), state.cities.index(end)))
            # cities.append(
            #     (np.where(state.cities == start), np.where(state.cities == end))
            # )

    return cities


def get_city_name_from_location(location, city_locations_dict):
    for name, loc in city_locations_dict.items():
        if tuple(loc) == tuple(location):
            return name
    return None


def write_to_timestamp_file(file_name, data):
    with open(file_name, "a") as file:
        file.write(data)
        file.write("\n")
