import pygame

from game_objects import ENTITIES_STATES, ACTIONS


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

    def draw_winner(self, screen, won_entity):
        if won_entity.get_state() == ENTITIES_STATES['cat']:
            x = self.offset_left // 2 - self.sprites[ENTITIES_STATES['cat']].get_size()[0] // 2
        else:
            x = self.offset_left + self.field_line_len + self.field_line_size
            x = (x + self.screen_width) // 2
            x = x - self.sprites[ENTITIES_STATES['mouse']].get_size()[0] // 2
        y = self.offset_top + self.entity_size * 2 + self._font.get_height() * 6
        self._draw_player_name(screen, 'winner', (0, 0, 0), x, y)

    def draw_no_winner(self, screen):
        cat_x = self.offset_left // 2 - self.sprites[ENTITIES_STATES['cat']].get_size()[0] // 2
        mouse_x = self.offset_left + self.field_line_len + self.field_line_size
        mouse_x = (mouse_x + self.screen_width) // 2
        mouse_x = mouse_x - self.sprites[ENTITIES_STATES['mouse']].get_size()[0] // 2
        y = self.offset_top + self.entity_size * 2 + self._font.get_height() * 6
        self._draw_player_name(screen, 'draw', (0, 0, 0), cat_x, y)
        self._draw_player_name(screen, 'draw', (0, 0, 0), mouse_x, y)

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

    def draw_world(self, screen, cat, mouse, field, actions_counter, draw_mouse_action, draw_cat_action):
        screen.fill((255, 255, 255))

        self._draw_field(screen)
        self._draw_entities(screen, field)
        self._draw_cat_player(screen, cat, draw_cat_action)
        self._draw_mouse_player(screen, mouse, draw_mouse_action)
        self._draw_counter(screen, str(actions_counter), (0, 0, 0))

        pygame.display.update()
