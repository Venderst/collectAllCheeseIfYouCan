from time import time
from copy import deepcopy

import pygame

from world_drawer import Drawer
from world_generator import WorldGenerator
from world_updater import update_field, update_entity, GAME_RESULTS
from game_objects import DynamicEntity, ENTITIES_STATES
from result_table_calculator import calculate_result_rating, sort_calculated_results_table

from models.random_models import RandomCat, RandomMouse
from models.simple_clever_models import SimpleCleverCat, SimpleCleverMouse

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

ENTITY_SIZE = 112

GAME_DELAY = 500
GAME_STATE_COMMENT_PRINTED_DELAY = 500
WINNER_PRINTED_DELAY = 4000
NO_WINNER_PRINTED_DELAY = 2000

MAX_ACTIONS_NUMBER = 216

# this value will be passed as a result of the game when the maximum number of actions is reached
MAX_ACTIONS_NUMBER_ACHIEVED_GAME_RESULT = GAME_RESULTS['CAT_WON']

soil_rand = time()

pygame.init()
pygame.display.set_caption('Collect cheese if you can')

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
)
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

is_game_over = False
ending_game_reason = ''

drawer = Drawer()
world_generator = WorldGenerator()

cat_models = [SimpleCleverCat(), RandomCat()]
mouse_models = [SimpleCleverMouse(), RandomMouse()]

game_results = []

generated_field = world_generator.generate_field(
    walls_count=9, cheese_count=5
)
generated_holes = world_generator.generate_and_add_holes_on_filed(generated_field, 2)

mouse = DynamicEntity(8, 0, ENTITIES_STATES['mouse'])
cat = DynamicEntity(0, 8, ENTITIES_STATES['cat'])

game_results.append([])
game_results[0].append('')

for cat_model in cat_models:
    game_results[0].append(cat_model.get_name())

for mouse_model_index in range(len(mouse_models)):
    game_results.append(list([mouse_models[mouse_model_index].get_name()]))
    for cat_model_index in range(len(cat_models)):
        if mouse_model_index == cat_model_index:
            game_results[mouse_model_index + 1].append([GAME_RESULTS['NOTHING'], '0', '0'])
            continue
        field = deepcopy(generated_field)
        holes = deepcopy(generated_holes)

        mouse.reset_do_nothing_actions_counter()
        mouse.reset_score()

        cat.reset_do_nothing_actions_counter()
        cat.reset_score()

        mouse.set_x(8)
        mouse.set_y(0)

        cat.set_x(0)
        cat.set_y(8)

        # for honest game
        # random.seed(soil_rand)

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
        pygame.time.delay(GAME_DELAY)

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
                field, mouse, mouse_action, world_generator, holes
            )
            update_entity(mouse, mouse_action)
            actions_counter += 1
            drawer.draw_world(
                screen, cat, mouse, field, actions_counter, True, False, game_state_description
            )
            if game_result != GAME_RESULTS['NOTHING']:
                break

            pygame.time.delay(
                GAME_DELAY - int((time() - mouse_action_begin_time) * 1000) +
                GAME_STATE_COMMENT_PRINTED_DELAY * int(len(game_state_description) > 0)
            )

            cat_action_begin_time = time()

            cat_action = cat.act(field)
            game_result, game_state_description = update_field(
                field, cat, cat_action, world_generator, holes
            )
            update_entity(cat, cat_action)
            actions_counter += 1
            drawer.draw_world(
                screen, cat, mouse, field, actions_counter, False, True, game_state_description
            )

            if game_result == GAME_RESULTS['MOUSE_WON']:
                break
            elif game_result == GAME_RESULTS['CAT_WON']:
                break
            elif actions_counter == MAX_ACTIONS_NUMBER:
                game_result = MAX_ACTIONS_NUMBER_ACHIEVED_GAME_RESULT
                game_state_description = 'Max actions\nnumber achieved'
                break

            pygame.time.delay(
                GAME_DELAY - int((time() - cat_action_begin_time) * 1000) +
                GAME_STATE_COMMENT_PRINTED_DELAY * int(len(game_state_description) > 0)
            )

        mouse.set_game_result(game_result)
        cat.set_game_result(game_result)

        game_results[mouse_model_index + 1].append([game_result, actions_counter, mouse.get_score()])

        if game_result != GAME_RESULTS['NOTHING']:
            won_entity = cat if game_result == GAME_RESULTS['CAT_WON'] else mouse
            drawer.draw_world(
                screen, cat, mouse, field, actions_counter, True, True
            )
            drawer.draw_winner(screen, won_entity, game_state_description)
            pygame.display.update()
            pygame.time.delay(WINNER_PRINTED_DELAY)
        else:
            drawer.draw_world(
                screen, cat, mouse, field, actions_counter, True, True
            )
            drawer.draw_no_winner(screen, game_state_description)
            drawer.draw_no_winner(screen, game_state_description)
            pygame.display.update()
            pygame.time.delay(NO_WINNER_PRINTED_DELAY)
        print('--------------------------')

# processing results
calculate_result_rating(game_results, cat_models, mouse_models)
sort_calculated_results_table(game_results)

drawer.draw_result_table(screen, game_results)
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
                exit()
