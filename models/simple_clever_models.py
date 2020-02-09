from random import randint

from math import copysign

from game_objects import Model, ACTIONS, ENTITIES_STATES


def calc_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class SimpleCleverCat(Model):

    def __init__(self):
        super().__init__()
        self._name = 'Simple clever cat'

    def act(self, states_map, player_x, player_y):
        """Method responsible for the model action.

        Parameters
        ----------
        states_map : list
            Current state of the field, 2D array.
            Each element represents one of the ENTITIES_STATES values.
        player_x : int
            The player's current position on the X axis.
        player_y : type
            The player's current position on the Y axis.

        Returns
        -------
        tuple
            The direction of the player's movement, one of the ACTIONS values

        """
        possible_actions = []
        for action in ACTIONS.values():
            if action == ACTIONS['DO_NOTHING']:
                continue
            new_x = player_x + action[1]
            new_y = player_y + action[0]
            if 0 <= new_x < len(states_map[0]) and 0 <= new_y < len(states_map):
                new_state = states_map[new_y][new_x]
                if new_state != ENTITIES_STATES['wall'] and new_state != ENTITIES_STATES['hole']:
                    possible_actions.append(action)

        # mouse position finding
        mouse_position = []
        for i in range(len(states_map)):
            for j in range(len(states_map[i])):
                if states_map[i][j] == ENTITIES_STATES['mouse']:
                    mouse_position = [i, j]
                    break

        if len(mouse_position):
            direction = [
                mouse_position[0] - player_y,
                mouse_position[1] - player_x
            ]
            direction = (
                copysign(1, direction[0]) if direction[0] != 0 else 0,
                copysign(1, direction[1]) if direction[1] != 0 else 0
            )
            for action in possible_actions:
                if action == direction:
                    return action
        if len(possible_actions) == 0:
            possible_actions = [ACTIONS['DO_NOTHING']]
        selected_action_index = randint(0, len(possible_actions) - 1)
        return possible_actions[selected_action_index]


class SimpleCleverMouse(Model):

    def __init__(self):
        super().__init__()
        self._name = 'Simple clever mouse'

    def act(self, states_map, player_x, player_y):
        """Method responsible for the model action.

        Parameters
        ----------
        states_map : list
            Current state of the field, 2D array.
            Each element represents one of the ENTITIES_STATES values.
        player_x : int
            The player's current position on the X axis.
        player_y : type
            The player's current position on the Y axis.

        Returns
        -------
        tuple
            The direction of the player's movement, one of the ACTIONS values

        """
        possible_actions = []
        for action in ACTIONS.values():
            if action == ACTIONS['DO_NOTHING']:
                continue
            new_x = player_x + action[1]
            new_y = player_y + action[0]
            if 0 <= new_x < len(states_map[0]) and 0 <= new_y < len(states_map):
                new_state = states_map[new_y][new_x]
                if new_state != ENTITIES_STATES['wall'] and new_state != ENTITIES_STATES['cat']:
                    possible_actions.append(action)

        # closest cheese position finding
        closest_cheese_position = None
        min_cheese_distance = len(states_map) * len(states_map[0])
        for i in range(len(states_map)):
            for j in range(len(states_map[i])):
                if states_map[i][j] == ENTITIES_STATES['cheese']:
                    distance = calc_distance(player_x, player_y, j, i)
                    if not closest_cheese_position or distance < min_cheese_distance:
                        min_cheese_distance = distance
                        closest_cheese_position = [i, j]

        if closest_cheese_position:
            direction = [
                closest_cheese_position[0] - player_y,
                closest_cheese_position[1] - player_x
            ]
            direction = (
                copysign(1, direction[0]) if direction[0] != 0 else 0,
                copysign(1, direction[1]) if direction[1] != 0 else 0
            )
            for action in possible_actions:
                if action == direction:
                    return action
        if len(possible_actions) == 0:
            possible_actions = [ACTIONS['DO_NOTHING']]
        selected_action_index = randint(0, len(possible_actions) - 1)
        return possible_actions[selected_action_index]
