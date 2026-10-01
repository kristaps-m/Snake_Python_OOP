import pygame
from snake import Snake
from food import Food

NEW_GAME_Y_POSITION = 110
VERSION_NUMBER_STRING = "v 1.0.0"

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
        self.new_game_button = self.snake.p_rect(self.w + 50, NEW_GAME_Y_POSITION, 200, 40)
        self.is_mouse_on_ngb = False # ngb = new game button
        self.is_game_over_bool = False


    def play_game(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Keyboard KEYDOWN events:
                if event.type == pygame.KEYDOWN:
                    self.movement_and_pause_keyboard_check(event)


                # If mouse inside new game button color it red else brown
                if self.new_game_button.collidepoint(mouse_pos): 
                    self.is_mouse_on_ngb = True
                else:
                    self.is_mouse_on_ngb = False
                # collision with mouse for new game buuton
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.new_game_button.collidepoint(mouse_pos):
                        self.new_game() 

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            """ ------ > RENDER YOUR GAME HERE""" 
            if not self.pause:
                self.update_and_draw_game_objects()
            else:
                self.snake.draw_snake_tail()
                self.snake.snake_head_draw()
                self.food.draw()
                if self.is_game_over_bool: 
                    self.render_text(100, "GAME OVER!!!", "#f309e780", self.w / 2 - 100, 50)
                self.render_text(100, "PAUSE", "#6464ff80", self.w / 2 - 100, self.h / 2 - 20)

            # render some menu text
            self.draw_right_side_menu_features()

            # Game field lines
            self.draw_game_field_lines()

            # version text :D
            self.render_text(19, VERSION_NUMBER_STRING, "white", self.w + self.add_w_for_menu - 50, self.h - 18)

            pygame.display.flip()

            self.clock.tick(6)  # limits FPS to 60

        pygame.quit()

    def render_text(self, font_size, text, color, x, y):
        the_font = pygame.font.SysFont(None, font_size)
        img = the_font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def new_game(self):
        self.snake = Snake(self.screen, 100, 20, 20)
        self.food = Food(self.screen, self.cell_size, self.w, self.h)
        if self.is_game_over_bool:
            self.pause = False
        self.is_game_over_bool = False

    def is_game_over(self): # have snake head run over yellow lines (walls)
        if self.snake.snake_head_x < 0:
            return True
        elif self.snake.snake_head_x >= self.w:
            return True
        elif self.snake.snake_head_y < 0:
            return True
        elif self.snake.snake_head_y >= self.h:
            return True

        return False

    def draw_game_field_lines(self):
        self.snake.draw_line("yellow",(self.w, 0),(self.w, self.h))
        self.snake.draw_line("yellow",(self.w, self.h - 1),(0, self.h - 1))
        self.snake.draw_line("yellow",(1, self.h),(1, 0))
        self.snake.draw_line("yellow",(0, 1),(self.w, 1), 2)

    def draw_right_side_menu_features(self):
        self.render_text(50, "SNAKE GAME!", "white", self.w + 50, 10)
        # poins (1) -> new game (2) -> pause (3)
        self.render_text(50, f"points: {len(self.snake.tail)}", "red", self.w + 50, 60) # 1
        
        pygame.draw.rect(self.screen, "brown" if not self.is_mouse_on_ngb else "red", self.new_game_button) # 2
        self.render_text(40, "NEW GAME", "white", self.w + 50 + 20, NEW_GAME_Y_POSITION + 9) # 2
        
        self.render_text(50, f"PAUSE? {'YES' if self.pause else 'NO' }", "white", self.w + 50, 160) # 3

    def movement_and_pause_keyboard_check(self, event):
        if event.key == pygame.K_s and self.snake.direction != "n":
            self.snake.direction = "s"
        elif event.key == pygame.K_w and self.snake.direction != "s":
            self.snake.direction = "n"
        elif event.key == pygame.K_a and self.snake.direction != "a":
            self.snake.direction = "w"
        elif event.key == pygame.K_d and self.snake.direction != "w":
            self.snake.direction = "a"
        elif (event.key == pygame.K_p or event.key == pygame.K_SPACE) and self.is_game_over_bool == False:
            self.pause = not self.pause

    
    def update_and_draw_game_objects(self):
        self.snake.snake_head_update()
        # check if game over -> have snake run over yellow lines
        if self.is_game_over():
            self.is_game_over_bool = True 
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
        if self.is_game_over_bool:
            self.pause = True