import pygame
from snake import Snake

class TheGame:
    def __init__(self):
        self.running = True
        self.w = 700
        self.h = 700
        self.add_w_for_menu = 350
        self.cell_size = 20
        self.screen = pygame.display.set_mode((self.w + self.add_w_for_menu, self.h))
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.screen, 100, 20, 20)

    def play_game(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


                # Keyboard events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.snake.direction = "s"
                    elif event.key == pygame.K_w:
                        self.snake.direction = "n"
                    elif event.key == pygame.K_a:
                        self.snake.direction = "w"
                    elif event.key == pygame.K_d:
                        self.snake.direction = "a"

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            """ ------ > RENDER YOUR GAME HERE""" 
            # self.snake.draw_line("yellow", (10, 10), (200,200))
            self.snake.snake_head_update()
            self.snake.draw_snake_tail()
            self.snake.snake_head_draw()

            pygame.display.flip()

            self.clock.tick(4)  # limits FPS to 60

        pygame.quit()
