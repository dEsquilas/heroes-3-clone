import constrains
import fps
import grid
import mobs
import os
import pygame
import sys

x = 100
y = 45
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

pygame.init()
screen = pygame.display.set_mode((constrains.WIDTH, constrains.HEIGHT))
pygame.display.set_caption("H3")

g = grid.Grid(14, 11)


mobs_sprites_group = pygame.sprite.Group()
m = mobs.BlueDragon()
m.set_position(0, g)
mobs_sprites_group.add(m)
b = mobs.Bandit(-1)
b.set_position(12, g)
mobs_sprites_group.add(b)

scenario_img = pygame.image.load("assets/scenarios/CmBkGrMt.png").convert()
scenario = pygame.transform.scale(scenario_img, (constrains.WIDTH, constrains.HEIGHT))

alpha_layer = pygame.Surface((constrains.WIDTH, constrains.HEIGHT), pygame.SRCALPHA)


cursor_image = pygame.image.load("assets/cursor.png").subsurface(
        250, 0, 40, 40
        ).convert_alpha()
pygame.mouse.set_visible(False)

number = 10

running = True
clock = pygame.time.Clock()

while running:

    change_cursor = False
    pygame.mouse.set_visible(True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                number += 1
                m.update_count(number)

    # Updates

    mouse_pos = pygame.mouse.get_pos()

    g.update()
    if g.clicked_id is not None and not g.hexagons[g.clicked_id].occupied:
        m.set_position(g.clicked_id, g)

    if g.over_id is not None and g.hexagons[g.over_id].occupied:
        change_cursor = True

    mobs_sprites_group.update()

    # Drawings

    screen.blit(scenario, (0, 0))
    g.draw(screen, alpha_layer)
    mobs_sprites_group.draw(screen)

    fps.draw_fps_counter(screen, clock)

    if change_cursor:
        pygame.mouse.set_visible(False)
        cursor_image_tmp = cursor_image

        mouse_dest = (mouse_pos[0] - 30, mouse_pos[1] - 10)

        if g.cursor_direction == -1 and g.cursor_position == 0:
            mouse_dest = (mouse_pos[0] - 40, mouse_pos[1] - 30)
        elif g.cursor_direction == 1 and g.cursor_position == 2:
            mouse_dest = (mouse_pos[0] - 20, mouse_pos[1] - 10)
        elif g.cursor_direction == 1 and g.cursor_position == 1:
            mouse_dest = (mouse_pos[0] - 10, mouse_pos[1] - 10)
        elif g.cursor_direction == 1 and g.cursor_position == 0:
            mouse_dest = (mouse_pos[0] - 10, mouse_pos[1] - 30)

        if g.cursor_position == 0:
            cursor_image_tmp = pygame.transform.rotate(cursor_image_tmp, -45)
        elif g.cursor_position == 2:
            cursor_image_tmp = pygame.transform.rotate(cursor_image_tmp, 45)

        if g.cursor_direction == 1:
            cursor_image_tmp = pygame.transform.flip(cursor_image_tmp, True, False)

        screen.blit(cursor_image_tmp, mouse_dest)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()