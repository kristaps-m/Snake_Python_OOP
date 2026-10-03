import pygame
import random

class Food:
    def __init__(self, surface, cell_size, w, h):
        self.surface = surface
        self.cell_size = cell_size
        self.w = w
        self.h = h
        self.x = cell_size * 4
        self.y = cell_size * 2

    def draw(self):
        pygame.draw.rect(self.surface,
                          "#ff0000",
                           self.p_rect(self.x, self.y, self.cell_size, self.cell_size)
                        )

    def generate_new_food(self, snake):
        new_x = random.randint(1, self.w // self.cell_size) * self.cell_size - self.cell_size
        new_y = random.randint(1, self.h // self.cell_size) * self.cell_size - self.cell_size

        while self.is_generated_food_in_snake(new_x, new_y, snake):
            print(self.is_generated_food_in_snake(new_x, new_y, snake))
            new_x = random.randint(1, self.w // self.cell_size) * self.cell_size - self.cell_size
            new_y = random.randint(1, self.h // self.cell_size) * self.cell_size - self.cell_size
        self.x = new_x
        self.y = new_y


    def is_generated_food_in_snake(self, new_x, new_y, snake):
        all_snake = snake.tail
        
        for t in all_snake:
            if t[0] == new_x and t[1] == new_y:
                return True
        return False


    def p_rect(self, x, y, w, h):
        return pygame.Rect(x, y, w, h)