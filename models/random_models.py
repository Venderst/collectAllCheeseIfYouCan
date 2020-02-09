from random import randint

from game_objects import Model, ACTIONS, ENTITIES_STATES


class RandomCat(Model):

    def __init__(self):
        super().__init__()
        self._name = 'Random cat'

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
        possible_actions = [ACTIONS['DO_NOTHING']]
        for action in ACTIONS.values():
            new_x = player_x + action[1]
            new_y = player_y + action[0]
            if 0 <= new_x < len(states_map[0]) and 0 <= new_y < len(states_map):
                new_state = states_map[new_y][new_x]
                if new_state != ENTITIES_STATES['wall'] and new_state != ENTITIES_STATES['hole']:
                    possible_actions.append(action)
        selected_action_index = randint(0, len(possible_actions) - 1)
        return possible_actions[selected_action_index]


class RandomMouse(Model):

    def __init__(self):
        super().__init__()
        self._name = 'Random mouse'

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
        possible_actions = [ACTIONS['DO_NOTHING']]
        for action in ACTIONS.values():
            new_x = player_x + action[1]
            new_y = player_y + action[0]
            if 0 <= new_x < len(states_map[0]) and 0 <= new_y < len(states_map):
                new_state = states_map[new_y][new_x]
                if new_state != ENTITIES_STATES['wall'] and new_state != ENTITIES_STATES['cat']:
                    possible_actions.append(action)
        selected_action_index = randint(0, len(possible_actions) - 1)
        return possible_actions[selected_action_index]
