import pygame

# surface = screen / screen = surface :)

class Snake:
    def __init__(self, surface, head_x, head_y, cell_size):
        self.surface = surface
        self.snake_head_x = head_x
        self.snake_head_y = head_y
        self.cell_size = cell_size
        self.direction = "a" # n a s w -> up, right, down, left

    def draw_line(self, color, start_pos, end_pos):
        pygame.draw.line(self.surface, color, start_pos, end_pos)

    def snake_head_update(self):
        if self.direction == "a":
            self.snake_head_x += self.cell_size
        elif self.direction == "w":
            self.snake_head_x -= self.cell_size
        elif self.direction == "n":
            self.snake_head_y -= self.cell_size
        elif self.direction == "s":
            self.snake_head_y += self.cell_size


    def snake_head_draw(self):
        pygame.draw.rect(self.surface,
                          "#93f59d",
                           self.p_rect(self.snake_head_x, self.snake_head_y, self.cell_size, self.cell_size)
                        )

    def p_rect(self, x, y, w, h):
        return pygame.Rect(x, y, w, h)
