ENTITIES_STATES = {
    'empty': -1,
    'wall': 0,
    'hole': 1,
    'cheese': 2,
    'mouse': 3,
    'cat': 4
}

# y, x
ACTIONS = {
    'MOVE_UP': (-1, 0),
    'MOVE_UP_RIGHT': (-1, 1),
    'MOVE_RIGHT': (0, 1),
    'MOVE_DOWN_RIGHT': (1, 1),
    'MOVE_DOWN': (1, 0),
    'MOVE_DOWN_LEFT': (1, -1),
    'MOVE_LEFT': (0, -1),
    'MOVE_UP_LEFT': (-1, -1),
    'DO_NOTHING': (0, 0)
}


class Model:

    def __init__(self):
        self._name = 'The name is not specified'

        self._game_results = {
            'NOTHING': 0,
            'MOUSE_WON': 1,
            'CAT_WON': 2,
            'DRAW': 3
        }

    def act(self, states_map, player_x, player_y):
        return ACTIONS['DO_NOTHING']

    def get_name(self):
        return self._name

    def set_game_result(self, game_result):
        result = list(self._game_results.keys())
        result = result[list(self._game_results.values()).index(game_result)]
        print(f'{self._name}: {result}')


class Entity:

    def __init__(self, world_map_x, world_map_y, state):
        self._world_map_x = world_map_x
        self._world_map_y = world_map_y

        self._state = state
        self.score = 0

    def increase_score(self):
        self.score += 1

    def reset_score(self):
        self.score = 0

    def get_x(self) -> int:
        return self._world_map_x

    def get_y(self) -> int:
        return self._world_map_y

    def get_state(self):
        return self._state

    def set_state(self, new_state):
        self._state = new_state

    def get_score(self):
        return self.score

    # correct direction is tuple (x, y)
    def move(self, correct_direction: tuple):
        self._world_map_x = correct_direction[0]
        self._world_map_y = correct_direction[1]


class DynamicEntity(Entity):

    def __init__(self, world_map_x, world_map_y, state, model=None):
        super().__init__(world_map_x, world_map_y, state)
        self._model = model

        self._state = state
        self._last_action = ACTIONS['DO_NOTHING']
        self._do_nothing_actions_counter = 0

    def set_model(self, model):
        self._model = model

    def get_last_action(self):
        return self._last_action

    def set_last_action(self, action):
        self._last_action = action

    def increase_do_nothing_actions_counter(self):
        self._do_nothing_actions_counter += 1

    def reset_do_nothing_actions_counter(self):
        self._do_nothing_actions_counter = 0

    def get_do_nothing_actions_counter(self):
        return self._do_nothing_actions_counter

    def set_x(self, x):
        self._world_map_x = x

    def set_y(self, y):
        self._world_map_y = y

    def get_name(self):
        return self._model.get_name()

    def act(self, field) -> tuple:
        """
        Calls the model's method to make a move

        Args:
            field (list): The matrix of Entity elements
                represents current field state

        Returns:
            tuple: one of ACTIONS
        """
        states_map = [
            [field[i][j].get_state() for j in range(len(field[i]))]
            for i in range(len(field))
        ]
        self._update_position(states_map)
        action = self._model.act(
            states_map, self._world_map_x, self._world_map_y
        )
        self._last_action = action

        return action

    def _update_position(self, field):
        for y in range(len(field)):
            for x in range(len(field[y])):
                if field[y][x] == self._state:
                    self._world_map_x = x
                    self._world_map_y = y
                    return

    def set_game_result(self, game_result):
        self._model.set_game_result(game_result)
