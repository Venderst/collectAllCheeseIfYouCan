import pygame

from world_drawer import Drawer
from world_generator import WorldGenerator
from world_updater import update_field, update_entity, GAME_RESULTS
from game_objects import DynamicEntity, ENTITIES_STATES

from random_models import RandomCat, RandomMouse
from simple_clever_models import SimpleCleverCat, SimpleCleverMouse

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

ENTITY_SIZE = 112

GAME_DELAY = 250

MAX_ACTIONS_NUMBER = 216

pygame.init()
pygame.display.set_caption('Collect cheese if you can')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

is_game_over = False

drawer = Drawer()
world_generator = WorldGenerator()

mouse_model = SimpleCleverMouse()
cat_model = SimpleCleverCat()

for i in range(100):
    mouse = DynamicEntity(8, 0, mouse_model, ENTITIES_STATES['mouse'])
    cat = DynamicEntity(0, 8, cat_model, ENTITIES_STATES['cat'])

    field = world_generator.generate_field(walls_count=9, cheese_count=5, mouse=mouse, cat=cat)

    holes = world_generator.generate_and_add_holes_on_filed(field, 2)

    game_result = GAME_RESULTS['NOTHING']

    actions_counter = 0

    drawer.draw_world(screen, cat, mouse, field, '', False, False)
    pygame.time.delay(GAME_DELAY * 3)

    while game_result == GAME_RESULTS['NOTHING'] and not is_game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_game_over = True
                    break

        mouse_action = mouse.act(field)
        game_result = update_field(field, mouse, mouse_action, world_generator, holes)
        update_entity(mouse, mouse_action)
        actions_counter += 1
        drawer.draw_world(screen, cat, mouse, field, actions_counter, True, False)
        if game_result == GAME_RESULTS['MOUSE_WON']:
            break
        elif game_result == GAME_RESULTS['CAT_WON']:
            break

        pygame.time.delay(GAME_DELAY)

        cat_action = cat.act(field)
        game_result = update_field(field, cat, cat_action, world_generator, holes)
        update_entity(cat, cat_action)
        actions_counter += 1
        drawer.draw_world(screen, cat, mouse, field, actions_counter, False, True)

        if game_result == GAME_RESULTS['MOUSE_WON']:
            break
        elif game_result == GAME_RESULTS['CAT_WON']:
            break
        elif actions_counter == MAX_ACTIONS_NUMBER:
            break

        pygame.time.delay(GAME_DELAY)

    mouse.set_game_result(game_result)
    cat.set_game_result(game_result)

    if game_result != GAME_RESULTS['NOTHING']:
        won_entity = cat if game_result == GAME_RESULTS['CAT_WON'] else mouse
        drawer.draw_world(screen, cat, mouse, field, actions_counter, True, True)
        drawer.draw_winner(screen, won_entity)
        pygame.display.update()
        pygame.time.delay(5000)
    else:
        drawer.draw_world(screen, cat, mouse, field, actions_counter, True, True)
        drawer.draw_no_winner(screen)
        pygame.display.update()
        pygame.time.delay(3000)
    if game_result == GAME_RESULTS['NOTHING']:
        break
    print('--------------------------')

pygame.quit()
