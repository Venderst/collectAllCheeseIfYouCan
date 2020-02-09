from random import choice
from copy import copy

from game_objects import ENTITIES_STATES, Entity, DynamicEntity


class WorldGenerator:

    def generate_field(self, walls_number, cheese_number,
                       world_width=9, world_height=9, mouse=None, cat=None):
        field = [
            [Entity(j, i, ENTITIES_STATES['empty']) for j in range(world_width)]
            for i in range(world_height)
        ]

        self.add_characters(field, mouse, cat)

        self.generate_and_add_entities_on_field(
            field, walls_number, ENTITIES_STATES['wall']
        )
        self.generate_and_add_entities_on_field(
            field, cheese_number, ENTITIES_STATES['cheese']
        )

        return field

    @staticmethod
    def clear_dynamic_entities(field: list):
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i][j] is DynamicEntity:
                    print(field[i][j])
                field[i][j] = Entity(j, i, ENTITIES_STATES['empty']) \
                    if field[i][j] is DynamicEntity else field[i][j]

    @staticmethod
    def add_characters(field, mouse=None, cat=None):
        if not (mouse is None):
            assert isinstance(mouse, DynamicEntity), \
                'Mouse must be instance of DynamicEntity!'
            field[mouse.get_y()][mouse.get_x()] = copy(mouse)
        if not (cat is None):
            assert isinstance(cat, DynamicEntity), \
                'Cat must be instance of DynamicEntity!'
            field[cat.get_y()][cat.get_x()] = copy(cat)

    @staticmethod
    def generate_and_add_entities_on_field(field, entities_count, entities_state):
        available_positions = []
        for i in range(1, len(field) - 1):
            for j in range(1, len(field[i]) - 1):
                if field[i][j].get_state() == ENTITIES_STATES['empty']:
                    available_positions.append((i, j))
        counter = 0
        while counter < entities_count and counter < len(available_positions):
            counter += 1
            random_position = choice(available_positions)
            field[random_position[0]][random_position[1]] = Entity(
                random_position[1], random_position[0], entities_state
            )
            available_positions.remove(random_position)

    @staticmethod
    def generate_and_add_holes_on_filed(field, holes_count=2, min_hole_distance=5):
        available_positions = []
        for i in range(1, len(field) - 1):
            for j in range(1, len(field[i]) - 1):
                if field[i][j].get_state() == ENTITIES_STATES['empty']:
                    available_positions.append((i, j))

        holes = []
        counter = 0
        while counter < holes_count and counter < len(available_positions):
            counter += 1
            random_position = copy(choice(available_positions))
            new_hole = Entity(
                random_position[1], random_position[0], ENTITIES_STATES['hole']
            )
            holes.append(new_hole)
            field[random_position[0]][random_position[1]] = new_hole
            # remove all holes whose distance from the selected position
            # is less than the minimum
            for available_position in available_positions[:-1]:
                distance = abs(available_position[0] - random_position[0]) + \
                           abs(available_position[1] - random_position[1])
                if distance < min_hole_distance:
                    available_positions.remove(available_position)

        return holes
