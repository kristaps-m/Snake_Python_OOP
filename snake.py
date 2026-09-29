import pygame

# surface = screen / screen = surface :)

class Snake:
    def __init__(self, surface, head_x, head_y, cell_size):
        self.surface = surface
        self.snake_head_x = head_x
        self.snake_head_y = head_y
        self.cell_size = cell_size
        self.direction = "a" # n a s w -> up, right, down, left
        self.tail = [
                (self.snake_head_x - self.cell_size * 3, self.snake_head_y),
                (self.snake_head_x - self.cell_size * 2, self.snake_head_y),
                (self.snake_head_x - self.cell_size, self.snake_head_y)
            ]

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
                           self.p_rect(self.snake_head_x, self.snake_head_y, self.cell_size, self.cell_size),
                           width=2
                        )

    def draw_snake_tail(self):
        for t in self.tail:
            pygame.draw.rect(self.surface,
                             "#caf7ce",
                             self.p_rect(t[0], t[1], self.cell_size, self.cell_size))

    def p_rect(self, x, y, w, h):
        return pygame.Rect(x, y, w, h)
