import pygame

def draw_fps_counter(screen, clock):
    font = pygame.font.Font(None, 15)
    fps = str(int(clock.get_fps()))
    fps_text = font.render("fps: " + fps, True, (255, 255, 255))
    bg_rect = pygame.Rect(0, 0, fps_text.get_width() + 10, fps_text.get_height() + 10)
    pygame.draw.rect(screen, (0, 0, 0), bg_rect)
    screen.blit(fps_text, (5, 5))