import pygame

from game_objects import ENTITIES_STATES, ACTIONS
from world_updater import GAME_RESULTS


class Drawer:

    def __init__(self, screen_width=1920, screen_height=1080, entity_size=104, field_line_size=4, scale_rate=1,
                 font_name='font.otf', font_size=30):
        entity_size = int(entity_size / scale_rate)

        self.args = dict()

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.entity_size = entity_size

        self.field_line_size = field_line_size

        self.cell_size = self.entity_size + self.field_line_size * 2

        self.field_line_len = self.cell_size * 9

        self.offset_left = self.screen_width // 2 - self.field_line_len // 2
        self.offset_right = self.offset_left + self.field_line_len
        self.offset_top = self.screen_height // 2 - self.field_line_len // 2 + font_size
        self.offset_bottom = self.offset_top + self.field_line_len

        self.sprites = [
            self.get_scaled_sprite('images/wall.png'),
            self.get_scaled_sprite('images/hole.png'),
            self.get_scaled_sprite('images/cheese.png'),
            self.get_scaled_sprite('images/mouse.png'),
            self.get_scaled_sprite('images/cat.jpg')
        ]

        self.direction_sprites = [
            self.get_scaled_sprite('images/up.png'),
            self.get_scaled_sprite('images/up_right.png'),
            self.get_scaled_sprite('images/right.png'),
            self.get_scaled_sprite('images/down_right.png'),
            self.get_scaled_sprite('images/down.png'),
            self.get_scaled_sprite('images/down_left.png'),
            self.get_scaled_sprite('images/left.png'),
            self.get_scaled_sprite('images/up_left.png'),
            self.get_scaled_sprite('images/do_nothing.png')
        ]

        self._font = pygame.font.Font(font_name, font_size)

    def get_scaled_sprite(self, image_path):
        sprite = pygame.image.load(image_path)
        # width, height
        aspect_ratio = sprite.get_size()[0] / sprite.get_size()[1]
        if aspect_ratio > 1:
            sprite = pygame.transform.scale(
                sprite, (
                    self.entity_size, sprite.get_size()[1] * self.entity_size // sprite.get_size()[0]
                )
            )
        elif aspect_ratio < 1:
            sprite = pygame.transform.scale(
                sprite, (
                    self.entity_size, sprite.get_rect().size[1] * self.entity_size // self.entity_size
                )
            )
        else:
            sprite = pygame.transform.scale(
                sprite, (
                    self.entity_size, self.entity_size
                )
            )
        return sprite

    def _draw_ending_game_reason(self, screen, won_entity=None, ending_game_reason='', font_color=(0, 0, 0)):
        text_rows = ending_game_reason.split('\n')
        start_y_position = self.field_line_len - self._font.get_height() * (len(text_rows) - 1)

        for row_index in range(len(text_rows)):
            text_surface = self._font.render(
                text_rows[row_index], True, font_color
            )
            if won_entity is None or won_entity.get_state() == ENTITIES_STATES['cat']:
                x = (self.screen_width + self.offset_right) // 2 - text_surface.get_width() // 2
                screen.blit(
                    text_surface,
                    (x, start_y_position + text_surface.get_height() * row_index)
                )
            if won_entity is None or won_entity.get_state() == ENTITIES_STATES['mouse']:
                x = self.offset_left // 2 - text_surface.get_width() // 2
                screen.blit(
                    text_surface,
                    (x, start_y_position + text_surface.get_height() * row_index)
                )

    def _draw_player_name(self, screen, text: str, font_color: tuple, entity_pos_x, pos_y):
        text_surface = self._font.render(text, True, font_color)
        # center text alignment
        delta_width = text_surface.get_width() - self.entity_size
        new_pos_x = entity_pos_x - delta_width // 2
        screen.blit(text_surface, (new_pos_x, pos_y))

    def _draw_counter(self, screen, counter_text: str, font_color):
        text_surface = self._font.render(counter_text, True, font_color)
        # center text alignment
        x = self.screen_width // 2 - text_surface.get_width() // 2
        screen.blit(text_surface, (x, 10))

    def draw_winner(self, screen, won_entity, ending_game_reason):
        if won_entity.get_state() == ENTITIES_STATES['cat']:
            x = self.offset_left // 2 - self.sprites[ENTITIES_STATES['cat']].get_size()[0] // 2
        else:
            x = self.offset_left + self.field_line_len + self.field_line_size
            x = (x + self.screen_width) // 2
            x = x - self.sprites[ENTITIES_STATES['mouse']].get_size()[0] // 2
        y = self.offset_top + self.entity_size * 2 + self._font.get_height() * 6
        self._draw_player_name(screen, 'winner', (0, 0, 0), x, y)
        self._draw_ending_game_reason(screen, won_entity, ending_game_reason, (0, 0, 0))

    def draw_no_winner(self, screen, ending_game_reason):
        cat_x = self.offset_left // 2 - self.sprites[ENTITIES_STATES['cat']].get_size()[0] // 2
        mouse_x = self.offset_left + self.field_line_len + self.field_line_size
        mouse_x = (mouse_x + self.screen_width) // 2
        mouse_x = mouse_x - self.sprites[ENTITIES_STATES['mouse']].get_size()[0] // 2
        y = self.offset_top + self.entity_size * 2 + self._font.get_height() * 6
        self._draw_player_name(screen, 'draw', (0, 0, 0), cat_x, y)
        self._draw_player_name(screen, 'draw', (0, 0, 0), mouse_x, y)
        self._draw_ending_game_reason(screen, ending_game_reason=ending_game_reason)
        self._draw_ending_game_reason(screen, ending_game_reason=ending_game_reason)

    def _draw_field(self, screen):
        for i in range(10):
            x = self.offset_left + self.cell_size * i - 1
            pygame.draw.line(screen, (0, 0, 0), (x, self.offset_top), (x, self.offset_bottom), self.field_line_size)

        for i in range(10):
            y = self.offset_top + self.cell_size * i - 1
            pygame.draw.line(screen, (0, 0, 0), (self.offset_left, y), (self.offset_right, y), self.field_line_size)

    def _draw_entities(self, screen, field):
        for row in field:
            for entity in row:
                if entity.get_state() != ENTITIES_STATES['empty']:
                    x = self.offset_left + self.cell_size * entity.get_x() + 4
                    y = self.offset_top + self.cell_size * entity.get_y() + 4
                    screen.blit(self.sprites[entity.get_state()], (x, y))

    def _draw_cat_player(self, screen, cat, draw_action):
        x = self.offset_left // 2 - self.sprites[ENTITIES_STATES['cat']].get_size()[0] // 2
        screen.blit(self.sprites[ENTITIES_STATES['cat']], (x, self.offset_top))
        if draw_action:
            self._draw_entity_last_action(screen, cat.get_last_action(), x)
        name_y = self.offset_top + self.entity_size * 2 + self._font.get_height() * 2
        self._draw_player_name(screen, cat.get_name(), (0, 0, 0), x, name_y)

    def _draw_mouse_player(self, screen, mouse, draw_action):
        x = self.offset_left + self.field_line_len + self.field_line_size
        x = (x + self.screen_width) // 2
        x = x - self.sprites[ENTITIES_STATES['mouse']].get_size()[0] // 2
        screen.blit(self.sprites[ENTITIES_STATES['mouse']], (x, self.offset_top))
        if draw_action:
            self._draw_entity_last_action(screen, mouse.get_last_action(), x)
        name_y = self.offset_top + self.entity_size * 2 + self._font.get_height() * 2
        score_y = name_y + self._font.get_height() * 2
        self._draw_player_name(screen, mouse.get_name(), (0, 0, 0), x, name_y)
        self._draw_player_name(screen, f'score: {mouse.get_score()}', (0, 0, 0), x, score_y)

    def _draw_entity_last_action(self, screen, action, position_x):
        sprite_action_index = len(ACTIONS.keys()) - 1
        for i in range(len(ACTIONS.values()) - 1):
            if action == list(ACTIONS.values())[i]:
                sprite_action_index = i
                break
        y = self.offset_top + self.entity_size * 1.5
        screen.blit(self.direction_sprites[sprite_action_index], (position_x, y))

    def draw_world(self, screen, cat, mouse, field, actions_counter, draw_mouse_action, draw_cat_action,
                   game_state_description=''):
        screen.fill((255, 255, 255))

        self._draw_field(screen)
        self._draw_entities(screen, field)
        self._draw_cat_player(screen, cat, draw_cat_action)
        self._draw_mouse_player(screen, mouse, draw_mouse_action)
        self._draw_counter(screen, str(actions_counter), (0, 0, 0))
        self._draw_ending_game_reason(screen, ending_game_reason=game_state_description)
        self._draw_ending_game_reason(screen, ending_game_reason=game_state_description)

        pygame.display.update()

    def draw_result_table(self, screen, game_results: list, font_name='font.otf', font_color=(0, 0, 0)):
        screen.fill((255, 255, 255))
        font = pygame.font.Font(font_name, 30)
        mouse_text_surfaces = []
        cat_text_surfaces = []
        max_mouse_text_surface_len = 0
        max_cat_text_surface_len = 0
        for mouse_model_index in range(1, len(game_results) - 1):
            text_surface = font.render(game_results[mouse_model_index][0], True, font_color)
            if max_mouse_text_surface_len < text_surface.get_width():
                max_mouse_text_surface_len = text_surface.get_width()
            mouse_text_surfaces.append(text_surface)

        for cat_model_index in range(1, len(game_results[0])):
            text_surface = font.render(game_results[0][cat_model_index], True, font_color)
            if max_cat_text_surface_len < text_surface.get_width():
                max_cat_text_surface_len = text_surface.get_width()
            text_surface = pygame.transform.rotate(text_surface, 90)
            cat_text_surfaces.append(text_surface)

        cell_width = (self.screen_width - max_mouse_text_surface_len) // (len(game_results))
        cell_height = (self.screen_height - max_cat_text_surface_len) // (len(game_results[0]) + 1)

        offset_horizontal = int(cell_width * 0.5)
        offset_vertical = int(cell_height * 0.5)

        for y in range(max_cat_text_surface_len + offset_vertical, self.screen_height - offset_vertical - cell_height,
                       cell_height):
            pygame.draw.line(screen, (0, 0, 0), (offset_horizontal, y), (self.screen_width - offset_horizontal, y),
                             self.field_line_size)

        for x in range(max_mouse_text_surface_len + offset_horizontal,
                       self.screen_width - offset_horizontal - cell_width, cell_width):
            pygame.draw.line(screen, (0, 0, 0), (x, offset_vertical), (x, self.screen_height - offset_vertical),
                             self.field_line_size)

        pygame.draw.rect(
            screen, (127, 127, 127), pygame.Rect(offset_horizontal, offset_vertical, max_mouse_text_surface_len - 1,
                                                 max_cat_text_surface_len - 1)
        )
        pygame.draw.rect(
            screen, (127, 127, 127), pygame.Rect(
                offset_horizontal, self.screen_height - offset_vertical - cell_height,
                max_mouse_text_surface_len - 1, cell_height + 1
            )
        )
        pygame.draw.rect(
            screen, (127, 127, 127), pygame.Rect(
                self.screen_width - offset_horizontal - cell_width - 1, offset_vertical,
                cell_width + 2, max_cat_text_surface_len - 1
            )
        )
        pygame.draw.rect(
            screen, (127, 127, 127), pygame.Rect(
                self.screen_width - offset_horizontal - cell_width - 1,
                self.screen_height - offset_vertical - cell_height,
                cell_width + 2, cell_height + 1
            )
        )

        for mouse_text_surface_index in range(len(mouse_text_surfaces)):
            x = offset_horizontal + max_mouse_text_surface_len // 2 - mouse_text_surfaces[
                mouse_text_surface_index].get_width() // 2
            y = offset_vertical + max_cat_text_surface_len + mouse_text_surface_index * cell_height
            y += cell_height // 2 - mouse_text_surfaces[mouse_text_surface_index].get_height() // 2

            screen.blit(mouse_text_surfaces[mouse_text_surface_index], (x, y))

        for cat_text_surface_index in range(len(cat_text_surfaces)):
            x = offset_horizontal + max_mouse_text_surface_len + cat_text_surface_index * cell_width
            x += cell_width // 2 - cat_text_surfaces[cat_text_surface_index].get_width() // 2
            y = offset_vertical + max_cat_text_surface_len // 2 - cat_text_surfaces[
                cat_text_surface_index].get_height() // 2

            screen.blit(cat_text_surfaces[cat_text_surface_index], (x, y))

        sprite_size = min(cell_width, cell_height)
        sprite_size //= 2
        if sprite_size > 128:
            sprite_size = 128
        mouse_sprite = pygame.transform.scale(self.sprites[ENTITIES_STATES['mouse']], (sprite_size, sprite_size))
        cat_sprite = pygame.transform.scale(self.sprites[ENTITIES_STATES['cat']], (sprite_size, sprite_size))

        font = pygame.font.Font(font_name, 15)

        for mouse_index in range(1, len(game_results) - 1):
            for cat_index in range(1, len(game_results[0])):

                x = offset_horizontal + max_mouse_text_surface_len + (cat_index - 1) * cell_width
                y = offset_vertical + max_cat_text_surface_len + (mouse_index - 1) * cell_height

                if game_results[mouse_index][cat_index] == [0, '0', '0']:
                    pygame.draw.rect(screen, (127, 127, 127),
                                     pygame.Rect(x + 3, y + 3, cell_width - 4, cell_height - 4))
                else:
                    text_surface = font.render(
                        '  ' + str(game_results[mouse_index][cat_index][1]) + '  ' + str(
                            game_results[mouse_index][cat_index][2]),
                        True, font_color
                    )

                    x += cell_width // 2 - (sprite_size + text_surface.get_width()) // 2
                    y += cell_height // 2

                    if game_results[mouse_index][cat_index][0] == GAME_RESULTS['MOUSE_WON']:
                        screen.blit(mouse_sprite, (x, y - sprite_size // 2))
                    elif game_results[mouse_index][cat_index][0] == GAME_RESULTS['CAT_WON']:
                        screen.blit(cat_sprite, (x, y - sprite_size // 2))
                    screen.blit(text_surface, (x + sprite_size, y - text_surface.get_height() // 2))

        for mouse_index in range(1, len(game_results) - 1):
            mouse_score = game_results[mouse_index][-1]
            text_surface = font.render(str(mouse_score), True, font_color)
            round_digit = 9
            while text_surface.get_width() > cell_width - font.size('1')[0] and round_digit > 0:
                mouse_score = round(mouse_score, round_digit)
                text_surface = font.render(str(mouse_score), True, font_color)
                round_digit -= 1

            screen.blit(
                text_surface,
                (
                    self.screen_width - offset_horizontal - cell_width // 2 - text_surface.get_width() // 2,
                    offset_vertical + max_cat_text_surface_len + cell_height * (mouse_index - 1) + cell_height // 2 -
                    text_surface.get_height() // 2
                )
            )

        for cat_index in range(1, len(game_results[-1])):
            cat_score = game_results[-1][cat_index]
            text_surface = font.render(str(cat_score), True, font_color)
            round_digit = 9
            while text_surface.get_width() > cell_width - font.size('1')[0] and round_digit > 0:
                cat_score = round(cat_score, round_digit)
                text_surface = font.render(str(cat_score), True, font_color)
                round_digit -= 1

            screen.blit(
                text_surface,
                (
                    offset_horizontal + max_mouse_text_surface_len + cell_width *
                    (cat_index - 1) + cell_width // 2 - text_surface.get_width() // 2,
                    self.screen_height - offset_vertical - cell_height // 2 - text_surface.get_height() // 2
                )
            )
