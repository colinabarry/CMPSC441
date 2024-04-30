def has_valid_route(state, action, city_from=None):
    if city_from is None:
        city_from = state.current_city

    action_value = int(chr(action))

    if 0 <= action_value <= 9:
        if action_value != state.current_city:
            city_routes = routes_to_cities(state)

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
        start = route[0]
        end = route[1]

        if start in state.cities and end in state.cities:
            cities.append((state.cities.index(start), state.cities.index(end)))
    return cities


def get_city_name_from_location(location, city_locations_dict):
    for name, loc in city_locations_dict.items():
        if loc == location:
            return name
    return None
