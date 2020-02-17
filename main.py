from time import time
from copy import deepcopy
import yaml
import importlib

import pygame

from utils.world_drawer import Drawer
from utils.world_generator import WorldGenerator
from utils.world_updater import update_field, update_entity, GAME_RESULTS
from game_objects import DynamicEntity, ENTITIES_STATES
from utils.result_table_calculator import calculate_result_rating, sort_calculated_results_table

cat_models = []
mouse_models = []

with open('models.yaml') as models_file:
    models = yaml.safe_load(models_file)

for file_name, [cat_class_name, mouse_class_name] in models.items():
    file_name = file_name.replace('/', '.').replace('\\', '.')
    file_name = file_name.replace('.py', '')

    if not file_name.startswith('models'):
        file_name = 'models.' + file_name

    catClass = getattr(
        importlib.import_module(file_name), cat_class_name
    )
    mouseClass = getattr(
        importlib.import_module(file_name), mouse_class_name
    )
    cat_models.append(catClass())
    mouse_models.append(mouseClass())

with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

config['MAX_ACTIONS_NUMBER_ACHIEVED_GAME_RESULT'] = \
    config['MAX_ACTIONS_NUMBER_ACHIEVED_GAME_RESULT']

soil_rand = time()

pygame.init()
pygame.display.set_caption(config['APP_CAPTION'])

if config['FULLSCREEN_MODE']:
    screen = pygame.display.set_mode(
        (config['SCREEN_WIDTH'], config['SCREEN_HEIGHT']), pygame.FULLSCREEN
    )
else:
    screen = pygame.display.set_mode(
        (config['SCREEN_WIDTH'], config['SCREEN_HEIGHT'])
    )

is_game_over = False
ending_game_reason = ''

drawer = Drawer(
    screen_width=config['SCREEN_WIDTH'],
    screen_height=int(config['SCREEN_HEIGHT'] * 0.94),
    field_line_size=4,
    scale_rate=config['SCALE_RATE'],
    font_name='fonts/font.otf', font_size=30,
    world_width=config['WORLD_WIDTH'], world_height=config['WORLD_HEIGHT']
)
world_generator = WorldGenerator()

all_replays_results = []

for replay in range(config['REPLAYS_NUM']):
    replay_results = []

    generated_field = world_generator.generate_field(
        walls_number=config['WALLS_NUMBER'], cheese_number=config['CHEESE_NUMBER'],
        world_width=config['WORLD_WIDTH'], world_height=config['WORLD_HEIGHT']
    )
    generated_holes = world_generator.generate_and_add_holes_on_filed(
        generated_field, config['HOLES_NUMBER']
    )

    mouse = DynamicEntity(config['WORLD_WIDTH'] - 1, 0, ENTITIES_STATES['mouse'])
    cat = DynamicEntity(0, config['WORLD_HEIGHT'] - 1, ENTITIES_STATES['cat'])

    replay_results.append([])
    replay_results[0].append('')

    for cat_model in cat_models:
        replay_results[0].append(cat_model.get_name())

    for mouse_model_index in range(len(mouse_models)):
        replay_results.append(list([mouse_models[mouse_model_index].get_name()]))
        for cat_model_index in range(len(cat_models)):
            if mouse_model_index == cat_model_index:
                replay_results[mouse_model_index + 1].append(
                    [GAME_RESULTS['NOTHING'], '0', '0']
                )
                continue
            field = deepcopy(generated_field)
            holes = deepcopy(generated_holes)

            mouse.reset_do_nothing_actions_counter()
            mouse.reset_score()

            cat.reset_do_nothing_actions_counter()
            cat.reset_score()

            mouse.set_x(config['WORLD_WIDTH'] - 1)
            mouse.set_y(0)

            cat.set_x(0)
            cat.set_y(config['WORLD_HEIGHT'] - 1)

            # for honest game
            if config['HONEST_MODE']:
                random.seed(soil_rand)

            mouse_model = mouse_models[mouse_model_index]
            cat_model = cat_models[cat_model_index]

            mouse.set_model(mouse_model)
            cat.set_model(cat_model)

            game_result = GAME_RESULTS['NOTHING']
            game_state_description = ''

            actions_counter = 0

            world_generator.clear_dynamic_entities(field)
            world_generator.add_characters(field, mouse=mouse, cat=cat)

            drawer.draw_world(screen, cat, mouse, field, '', False, False)
            pygame.time.delay(config['GAME_DELAY'])

            while game_result == GAME_RESULTS['NOTHING'] and not is_game_over:
                # checking if ESC key pressed and
                # if true, then it is necessary to stop the game
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.display.quit()
                            pygame.quit()
                            exit()

                mouse_action_begin_time = time()

                mouse_action = mouse.act(field)
                game_result, game_state_description = update_field(
                    field, mouse, mouse_action, world_generator, holes,
                    amount_of_cheese_to_win=config['CHEESE_NUMBER'],
                    amount_of_do_nothing_actions_to_loose=config['MAX_DO_NOTHING_ACTIONS_NUMBER'],
                    field_width=config['WORLD_WIDTH'],
                    field_height=config['WORLD_HEIGHT']
                )

                update_entity(
                    mouse, mouse_action,
                    field_width=config['WORLD_WIDTH'],
                    field_height=config['WORLD_HEIGHT']
                )
                actions_counter += 1
                drawer.draw_world(
                    screen, cat, mouse, field, actions_counter, True, False,
                    game_state_description
                )
                if game_result != GAME_RESULTS['NOTHING']:
                    break

                mouse.set_game_result(game_result)

                pygame.time.delay(
                    config['GAME_DELAY'] -
                    int((time() - mouse_action_begin_time) * 1000) +
                    config['GAME_STATE_COMMENT_PRINTED_DELAY'] *
                    int(len(game_state_description) > 0)
                )

                cat_action_begin_time = time()

                cat_action = cat.act(field)
                game_result, game_state_description = update_field(
                    field, cat, cat_action, world_generator, holes,
                    field_width=config['WORLD_WIDTH'],
                    field_height=config['WORLD_HEIGHT']
                )

                update_entity(
                    cat, cat_action,
                    field_width=config['WORLD_WIDTH'],
                    field_height=config['WORLD_HEIGHT']
                )
                actions_counter += 1
                drawer.draw_world(
                    screen, cat, mouse, field, actions_counter, False, True,
                    game_state_description
                )

                if game_result == GAME_RESULTS['MOUSE_WON']:
                    break
                elif game_result == GAME_RESULTS['CAT_WON']:
                    break
                elif actions_counter == config['MAX_ACTIONS_NUMBER']:
                    game_result = GAME_RESULTS[config['MAX_ACTIONS_NUMBER_ACHIEVED_GAME_RESULT']]
                    game_state_description = 'Max actions\nnumber achieved'
                    break

                cat.set_game_result(game_result)

                pygame.time.delay(
                    config['GAME_DELAY'] -
                    int((time() - cat_action_begin_time) * 1000) +
                    config['GAME_STATE_COMMENT_PRINTED_DELAY'] *
                    int(len(game_state_description) > 0)
                )

            replay_results[mouse_model_index + 1].append(
                [game_result, actions_counter, mouse.get_score()]
            )

            cat.set_game_result(game_result)
            mouse.set_game_result(game_result)

            if game_result != GAME_RESULTS['NOTHING']:
                won_entity = cat if game_result == GAME_RESULTS['CAT_WON'] else mouse
                drawer.draw_world(
                    screen, cat, mouse, field, actions_counter, True, True
                )
                drawer.draw_winner(screen, won_entity, game_state_description)
                pygame.display.update()
                pygame.time.delay(config['WINNER_PRINTED_DELAY'])
            else:
                drawer.draw_world(
                    screen, cat, mouse, field, actions_counter, True, True
                )
                drawer.draw_no_winner(screen, game_state_description)
                drawer.draw_no_winner(screen, game_state_description)
                pygame.display.update()
                pygame.time.delay(config['WINNER_PRINTED_DELAY'])
            print('--------------------------')

    # processing results
    calculate_result_rating(replay_results, cat_models, mouse_models)
    sort_calculated_results_table(replay_results)

    all_replays_results.append(replay_results)

    drawer.draw_result_table(screen, replay_results)
    pygame.display.update()

    waiting_start_time = time()
    remaining_waiting_time = config['RESULT_TABLE_WINDOW_DELAY']
    is_exit_key_pressed = False
    while remaining_waiting_time != 0 and not is_exit_key_pressed:
        if remaining_waiting_time != -1:
            remaining_waiting_time -= time() - waiting_start_time
            remaining_waiting_time = max(remaining_waiting_time, 0)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_exit_key_pressed = True
                    break

pygame.display.quit()
pygame.quit()
exit()
