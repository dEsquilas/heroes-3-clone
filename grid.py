import constrains
import pygame
import time


class Hexagon:
    def __init__(self, origin, hid):
        self.origin = origin
        self.id = hid
        self.color = (61, 180, 50)
        self.fill_color = (100, 100, 250, 128)
        self.vertex = self.calculate_vertex()
        self.clicked = False
        self.occupied = False

        self.neighbours = {
            'top_left': None,
            'top_right': None,
            'left': None,
            'right': None,
            'bottom_left': None,
            'bottom_right': None
        }

    def set_neighbours(self, grid, row, col):

        if row % 2 == 0:
            distance = grid.width - 1

            if row != 0:
                self.neighbours['top_left'] = self.id - distance - 1
                self.neighbours['top_right'] = self.id - distance

            if row != grid.height - 1:
                self.neighbours['bottom_left'] = self.id + distance
                self.neighbours['bottom_right'] = self.id + distance + 1

        else:
            distance = grid.width

            if col != 0:
                self.neighbours['top_left'] = self.id - distance
                self.neighbours['bottom_left'] = self.id + distance - 1
            if col != distance - 1:
                self.neighbours['top_right'] = self.id - distance + 1
                self.neighbours['bottom_right'] = self.id + distance

        if col != 0:
            self.neighbours['left'] = self.id - 1

        if col != distance - 1:
            self.neighbours['right'] = self.id + 1

    def calculate_vertex(self):
        vertex = []
        # 54, 26
        v = [
            (constrains.HW/2, - constrains.HMH),
            (constrains.HW, 0),
            (constrains.HW, constrains.HH),
            (constrains.HW/2, constrains.HH + constrains.HMH),
            (0, constrains.HH)
        ]

        vertex.append(self.origin)

        for i in range(len(v)):
            t = (self.origin[0] + v[i][0], self.origin[1] + v[i][1])
            vertex.append(t)

        return vertex

    def point_inside(self, x, y):
        # check if the coordinates are inside the polygon
        n = len(self.vertex)
        inside = False
        p1x, p1y = self.vertex[0]
        for i in range(n + 1):
            p2x, p2y = self.vertex[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def draw(self, screen, alpha_layer):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.point_inside(mouse_x, mouse_y):
            pygame.draw.polygon(alpha_layer, self.fill_color, self.vertex)
            screen.blit(alpha_layer, (0, 0))
            alpha_layer.fill((0, 0, 0, 0))

        pygame.draw.polygon(screen, self.color, self.vertex, 1)



class Grid:
    def __init__(self, width, height):
        self.hexagons = []
        self.width = width
        self.height = height

        self.last_click_time = None
        self.clicked_id = None
        self.over_id = None
        self.cursor_direction = None
        self.cursor_position = None
        self.neighbour_direction = None

        current_id = 0
        current_py = 0
        current_px = 0
        MAIN_Y_OFFSET = 60

        total_grid_width = constrains.HW * self.width
        total_grid_height = (constrains.HH + constrains.HMH) * self.height

        initial_x_position = (constrains.WIDTH - total_grid_width) / 2
        initial_y_position = (constrains.HEIGHT - total_grid_height) / 2 + MAIN_Y_OFFSET

        for i in range(self.height):

            if i == 0:
                current_py = initial_y_position
            else:
                current_py += constrains.HW - constrains.HD if not i % 2 == 0 else constrains.HH + constrains.HMH

            current_px = initial_x_position if not i % 2 == 0 else initial_x_position + constrains.HW / 2

            limit = self.width + 1 if not i % 2 == 0 else self.width

            for j in range(0, limit - 1):
                self.hexagons.append(Hexagon((current_px + j * constrains.HW, current_py), current_id))
                self.hexagons[current_id].set_neighbours(self, i, j)
                current_id += 1

    def draw(self, screen, alpha_layer):

        for h in self.hexagons:
            h.draw(screen, alpha_layer)

    def update(self):
        if self.last_click_time and time.time() - self.last_click_time > 0.2:
            self.last_click_time = None

        state = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        clicked_found = False
        self.over_id = None

        for h in self.hexagons:
            if h.point_inside(mouse_position[0], mouse_position[1]):
                if state[0] and self.last_click_time is None:
                    self.last_click_time = time.time()
                    self.clicked_id = h.id
                    clicked_found = True
                else:
                    self.over_id = h.id

        if not clicked_found:
            self.clicked_id = None

        if self.over_id is not None:

            current_hexagon = self.hexagons[self.over_id]

            distance_x = current_hexagon.vertex[0][1] - current_hexagon.vertex[2][1]
            distance_x_cursor = mouse_position[0] - current_hexagon.vertex[1][0]

            margin = 17

            if distance_x_cursor < distance_x / 2:
                self.cursor_direction = -1
            else:
                self.cursor_direction = 1

            if mouse_position[1] < current_hexagon.vertex[1][1] + margin:
                self.cursor_position = 0
            elif mouse_position[1] > current_hexagon.vertex[5][1] - margin:
                self.cursor_position = 2
            else:
                self.cursor_position = 1

            if self.cursor_direction == -1:
                if self.cursor_position == 0:
                    self.neighbour_direction = 'top_left'
                elif self.cursor_position == 1:
                    self.neighbour_direction = 'left'
                else:
                    self.neighbour_direction = 'bottom_left'
            else:
                if self.cursor_position == 0:
                    self.neighbour_direction = 'top_right'
                elif self.cursor_position == 1:
                    self.neighbour_direction = 'right'
                else:
                    self.neighbour_direction = 'bottom_right'

    def reset(self):
        self.clicked_id = None
