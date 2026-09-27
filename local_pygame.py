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
        self.snake = Snake(self.screen, 20, 80, 20)

    def play_game(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


                # Keyboard events:
                # if event.type == pygame.KEYUP:
                    # if event.key == pygame.K_F11:
                    #     print("K F11 pressed")


            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            """ ------ > RENDER YOUR GAME HERE""" 
            self.snake.draw_line("yellow", (10, 10), (200,200))
            self.snake.snake_head_update()
            self.snake.snake_head_draw()

            pygame.display.flip()

            self.clock.tick(4)  # limits FPS to 60

        pygame.quit()
