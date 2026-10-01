import pygame
from snake import Snake
from food import Food

class TheGame:
    def __init__(self):
        pygame.init()
        self.running = True
        self.w = 600
        self.h = 600
        self.add_w_for_menu = 360
        self.cell_size = 20
        self.pause = False
        self.screen = pygame.display.set_mode((self.w + self.add_w_for_menu, self.h))
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.screen, 100, 20, 20)
        self.food = Food(self.screen, self.cell_size, self.w, self.h)


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
                    elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                        print(f"{self.pause}")

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            """ ------ > RENDER YOUR GAME HERE""" 
            self.snake.draw_line(
                    "yellow",
                    (self.w, 0),
                    (self.w, self.h)
                )
            if not self.pause:
                self.snake.snake_head_update()
                if self.snake.snake_head_x == self.food.x and self.snake.snake_head_y == self.food.y:
                    # If snake head matches foods precise x and y position we make tail longer and generate new food
                    self.snake.tail.append((self.food.x, self.food.y))
                    self.food.generate_new_food(self.snake)

                self.snake.draw_snake_tail()
                # adding and deleting from tail helps snake move forward.
                self.snake.tail.append(
                        (self.snake.snake_head_x, self.snake.snake_head_y)
                    )
                
                self.snake.snake_head_draw()
                del self.snake.tail[0]
                self.food.draw()
            else:
                self.snake.draw_snake_tail()
                self.snake.snake_head_draw()
                self.food.draw()
                self.render_text(100, "PAUSE", "#6464ff80", self.w / 2 - 100, self.h / 2 - 20)

            # render some menu text
            self.render_text(50, "SNAKE GAME!", "white", self.w + 50, 10)
            # poins -> new game -> pause
            self.render_text(50, f"points: {len(self.snake.tail)}", "red", self.w + 50, 40)
            self.render_text(50, "NEW GAME TODO", "white", self.w + 50, 70)
            self.render_text(50, f"PAUSE? {'YES' if self.pause else 'NO' }", "white", self.w + 50, 100)

            pygame.display.flip()

            self.clock.tick(4)  # limits FPS to 60

        pygame.quit()

    def render_text(self, font_size, text, color, x, y):
        the_font = pygame.font.SysFont(None, font_size)
        img = the_font.render(text, True, color)
        self.screen.blit(img, (x, y))
