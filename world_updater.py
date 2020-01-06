from random import choice

from game_objects import ENTITIES_STATES, ACTIONS, Entity, DynamicEntity

GAME_RESULTS = {
    'NOTHING': 0,
    'MOUSE_WON': 1,
    'CAT_WON': 2,
    'DRAW': 3
}


def update_entity(entity: DynamicEntity, action):
    new_y = entity.get_y() + action[0]
    new_x = entity.get_x() + action[1]

    if 0 <= new_y < 9 and 0 <= new_x < 9:
        entity.set_x(new_x)
        entity.set_y(new_y)


def process_mouse_transition_in_hole(field, mouse, holes: list, mouse_next_x, mouse_next_y):
    field[mouse.get_y()][mouse.get_x()] = Entity(mouse.get_x(), mouse.get_y(), ENTITIES_STATES['empty'])
    # finding and removing hole in current position
    current_hole_index = 0
    for i in range(1, len(holes)):
        hole = holes[i]
        if hole.get_x() == mouse_next_x and hole.get_y() == mouse_next_y:
            current_hole_index = i
    del holes[current_hole_index]
    field[mouse_next_y][mouse_next_x] = Entity(mouse.get_x(), mouse.get_y(), ENTITIES_STATES['empty'])
    # mouse transition
    next_hole = choice(holes)
    field[next_hole.get_y()][next_hole.get_x()] = mouse
    mouse.set_x(next_hole.get_x())
    mouse.set_y(next_hole.get_y())
    mouse.set_last_action(ACTIONS['DO_NOTHING'])


def update_field(field, entity: DynamicEntity, action: tuple, world_generator, holes, amount_of_cheese_to_win=5,
                 amount_of_do_nothing_actions_to_loose=3) -> tuple:
    if action == ACTIONS['DO_NOTHING']:
        entity.increase_do_nothing_actions_counter()
        if entity.get_do_nothing_actions_counter() > amount_of_do_nothing_actions_to_loose:
            return \
                GAME_RESULTS['CAT_WON'] if entity.get_state() == ENTITIES_STATES['mouse'] \
                else GAME_RESULTS['MOUSE_WON'], \
                'Max do nothing\nactions number achieved'
    else:
        entity.reset_do_nothing_actions_counter()

    new_y = entity.get_y() + action[0]
    new_x = entity.get_x() + action[1]

    if 0 <= new_y < 9 and 0 <= new_x < 9:
        new_state = field[new_y][new_x].get_state()
        if new_state == ENTITIES_STATES['wall']:
            if entity.get_state() == ENTITIES_STATES['cat']:
                return GAME_RESULTS['MOUSE_WON'], 'Cat crashed into the wall'
            else:
                return GAME_RESULTS['CAT_WON'], 'Mouse crashed into the wall'
        else:
            if entity.get_state() == ENTITIES_STATES['mouse']:
                if new_state == ENTITIES_STATES['cheese']:
                    entity.increase_score()
                    if entity.get_score() == amount_of_cheese_to_win:
                        result = GAME_RESULTS['MOUSE_WON'], 'All the cheeses are collected'
                    else:
                        result = GAME_RESULTS['NOTHING'], ''
                elif new_state == ENTITIES_STATES['cat']:
                    result = GAME_RESULTS['CAT_WON'], 'Mouse caught by a cat'
                elif new_state == ENTITIES_STATES['hole']:
                    process_mouse_transition_in_hole(field, entity, holes, new_x, new_y)
                    return GAME_RESULTS['NOTHING'], ''
                else:
                    result = GAME_RESULTS['NOTHING'], ''
            else:
                if new_state == ENTITIES_STATES['mouse']:
                    result = GAME_RESULTS['CAT_WON'], 'The cat caught the mouse'
                elif new_state == ENTITIES_STATES['cheese']:
                    world_generator.generate_and_add_entities_on_field(field, 1, ENTITIES_STATES['cheese'])
                    result = GAME_RESULTS['NOTHING'], 'The cat ate the cheese'
                elif new_state == ENTITIES_STATES['hole']:
                    return GAME_RESULTS['MOUSE_WON'], 'The cat was lost in the hole'
                else:
                    result = GAME_RESULTS['NOTHING'], ''

            field[entity.get_y()][entity.get_x()] = Entity(entity.get_x(), entity.get_y(), ENTITIES_STATES['empty'])
            field[new_y][new_x] = entity

            return result
    else:
        if entity.get_state() == ENTITIES_STATES['cat']:
            return GAME_RESULTS['MOUSE_WON'], 'The cat went out of bounds'
        else:
            return GAME_RESULTS['CAT_WON'], 'The mouse went out of bounds'
