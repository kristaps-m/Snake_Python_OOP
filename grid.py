import pygame
from constants import *

class Grid:
    def __init__(self, w, h, cell_size, surface):
        self.w = w
        self.h = h
        self.cell_size = cell_size
        self.surface = surface

    def draw_line(self, color, start_pos, end_pos, line_width = 1):
        pygame.draw.line(self.surface, color, start_pos, end_pos, width=line_width)

    def draw_grid_on_game_field(self):
        # Horizontal
        for i in range(1, self.w // self.cell_size):
            self.draw_line(GRID_LINE_COLOR, (0, i * self.cell_size), (self.w, i * self.cell_size))

        # vertical
        for j in range(1, self.w // self.cell_size):
            self.draw_line(GRID_LINE_COLOR, (j * self.cell_size, 0), (j * self.cell_size, self.h))
