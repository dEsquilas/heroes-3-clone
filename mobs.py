import constrains
import pygame


class Mob(pygame.sprite.Sprite):
    def __init__(self, image_path, position, count, direction=1):
        super().__init__()

        self.count_distance_to_sprite = 10
        self.count_width = 35
        self.count_height = 15
        self.direction = direction
        self.current_position = -1

        #mob attributes

        self.attack_min = 0
        self.attack_max = 0
        self.hp = 0
        self.current_hp = 0
        self.speed = 0
        self.is_ranged = 0
        self.count = count

        self.sprite_image = pygame.image.load(image_path).subsurface(
            position[0], position[1], position[2], position[3]
        ).convert_alpha()
        self.image = pygame.Surface(
            (self.sprite_image.get_width() + (self.count_width + self.count_distance_to_sprite),
             self.sprite_image.get_height()),
            pygame.SRCALPHA)

        count_offset_x = self.sprite_image.get_rect().width + self.count_distance_to_sprite
        count_offset_y = self.sprite_image.get_rect().height - self.count_height * 2

        if self.direction == -1:
            self.sprite_image = pygame.transform.flip(self.sprite_image, True, False)
            self.image.blit(self.sprite_image, (self.count_width + self.count_distance_to_sprite, 0))
            count_offset_x = 0
        else:
            self.image.blit(self.sprite_image, (0, 0))

        self.count_offset = (count_offset_x, count_offset_y)

        self.font = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 11)
        self.count_surface = self.font.render(self.count, True, (255, 255, 255))
        self.count_position = (count_offset_x + self.count_width / 2, count_offset_y + self.count_height / 2 - 1)
        self.count_rect = self.count_surface.get_rect(center=self.count_position)

        self.update_count(10)

        self.rect = self.image.get_rect()

    def set_mob_attr(self, attack_min, attack_max, hp, speed, is_ranged):
        self.attack_min = attack_min
        self.attack_max = attack_max
        self.hp = hp
        self.current_hp = hp * self.count
        self.speed = speed
        self.is_ranged = is_ranged

    def update_count(self, number):
        pygame.draw.rect(self.image, (80, 50, 190),
                         (self.count_offset[0], self.count_offset[1], self.count_width, self.count_height))
        pygame.draw.rect(self.image, (190, 165, 50),
                         (self.count_offset[0], self.count_offset[1], self.count_width, self.count_height), 1)
        self.count_surface = self.font.render(str(number), True, (255, 255, 255))
        self.count_rect = self.count_surface.get_rect(center=self.count_position)
        self.image.blit(self.count_surface, self.count_rect)

    def set_position(self, hex_id, grid, managed=True):

        position = grid.hexagons[hex_id].origin
        if self.current_position != -1:
            grid.hexagons[self.current_position].occupied = False
        self.current_position = hex_id
        grid.hexagons[hex_id].occupied = True

        if managed:
            position = self.get_mob_on_tile_position(position)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def get_mob_on_tile_position(self, tile):
        y_position = tile[1] + constrains.HH - self.sprite_image.get_rect().size[1]
        x_position = tile[0] + constrains.HW / 2 - self.sprite_image.get_rect().size[0] / 2
        if self.direction == -1:
            x_position = tile[0] + constrains.HW / 2 - self.sprite_image.get_rect().size[0] / 2 - (self.count_width + self.count_distance_to_sprite)

        return x_position, y_position


class BlueDragon(Mob):
    def __init__(self, direction=1):
        super().__init__("assets/dragon.png", [43, 21, 90, 111], direction)
        self.set_mob_attr(40, 50, 250, 10, False)


class Bandit(Mob):
    def __init__(self, direction=1):
        super().__init__("assets/bandit.png", [27, 32, 46, 97], direction)
        self.set_mob_attr(5, 5, 10, 10, 0)
