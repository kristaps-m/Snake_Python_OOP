import pygame
from pygame import mixer
from snake import Snake
from food import Food
from grid import Grid
from constants import *


class TheGame:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.running = True
        self.w = W
        self.h = H
        self.add_w_for_menu = ADD_W_FOR_MENU
        self.cell_size = CELL_SIZE
        self.pause = False
        self.is_game_over_bool = False
        self.is_game_won_bool = False # Is grid full so that new food can not be placed
        self.screen = pygame.display.set_mode((self.w + self.add_w_for_menu, self.h))
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.screen, self.cell_size * 4, self.cell_size, self.cell_size)
        self.food = Food(self.screen, self.cell_size, self.w, self.h)
        self.grid = Grid(self.w, self.h, self.cell_size, self.screen)
        self.sound = mixer.Sound("sounds/njam-[AudioTrimmer.com]_2.ogg")
        self.new_game_button = self.snake.p_rect(self.w + 50, NEW_GAME_Y_POSITION, 200, 40)
        self.sound_toggle_btn = self.snake.p_rect(self.w + 50, SOUND_BTN_Y_POSITION, 200, 40)
        self.is_mouse_on_ngb = False # ngb = new game button
        self.has_player_made_movement = False
        self.is_sound_on = True


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
                    if self.sound_toggle_btn.collidepoint(mouse_pos):
                        self.is_sound_on = not self.is_sound_on 

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

            self.has_player_made_movement = False # This variable prevents player from cheat in movement
            
            self.grid.draw_grid_on_game_field()

            if self.does_snake_cover_all_field():
                self.pause = True
                self.render_text(100, "Victory", "#0df30980", self.w / 2 - 100, 50)
                

            pygame.display.flip()

            self.clock.tick(6)  # limits FPS to 60

        pygame.quit()

    def render_text(self, font_size, text, color, x, y):
        the_font = pygame.font.SysFont(None, font_size)
        img = the_font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def new_game(self):
        self.snake = Snake(self.screen, self.cell_size * 4, self.cell_size, self.cell_size)
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


    def does_snake_cover_all_field(self):
        snake_tail_set = set(self.snake.tail)
        is_tail_set_len_long_as_game_field = len(snake_tail_set) == (self.w // self.cell_size) * (self.h // self.cell_size) - 2

        return is_tail_set_len_long_as_game_field
    

    def draw_game_field_lines(self):
        self.snake.draw_line("yellow",(self.w, 0),(self.w, self.h))
        self.snake.draw_line("yellow",(self.w, self.h - 1),(0, self.h - 1))
        self.snake.draw_line("yellow",(1, self.h),(1, 0))
        self.snake.draw_line("yellow",(0, 1),(self.w, 1), 2)

    def draw_right_side_menu_features(self):
        self.render_text(50, "SNAKE GAME!", "white", self.w + 50, 10)
        # poins (1) -> new game (2) -> pause (3) -> sound on/off (4)
        self.render_text(50, f"points: {len(self.snake.tail)}", "red", self.w + 50, 60) # 1
        
        pygame.draw.rect(self.screen, "brown" if not self.is_mouse_on_ngb else "red", self.new_game_button) # 2
        self.render_text(40, "NEW GAME", "white", self.w + 50 + 20, NEW_GAME_Y_POSITION + 9) # 2
        
        self.render_text(50, f"PAUSE? {'YES' if self.pause else 'NO' }", "white", self.w + 50, 160) # 3

        pygame.draw.rect(self.screen, "darkblue", self.sound_toggle_btn) # 4
        self.render_text(40, f"Sound {'On' if self.is_sound_on else 'off'}", "white", self.w + 50 + 20, SOUND_BTN_Y_POSITION + 9) # 4


    def movement_and_pause_keyboard_check(self, event):
        if not self.has_player_made_movement:
            if event.key == pygame.K_s and self.snake.direction != "n":
                self.snake.direction = "s"
                self.has_player_made_movement = True
            elif event.key == pygame.K_w and self.snake.direction != "s":
                self.snake.direction = "n"
                self.has_player_made_movement = True
            elif event.key == pygame.K_a and self.snake.direction != "a":
                self.snake.direction = "w"
                self.has_player_made_movement = True
            elif event.key == pygame.K_d and self.snake.direction != "w":
                self.snake.direction = "a"
                self.has_player_made_movement = True
        if (event.key == pygame.K_p or event.key == pygame.K_SPACE) and self.is_game_over_bool == False:
            self.pause = not self.pause
        # if event.key == pygame.K_l: # Sound tester when pressing L
        #     self.sound.play()

    
    def update_and_draw_game_objects(self):
        self.snake.snake_head_update()
        # check if game over -> have snake run over yellow lines
        if self.is_game_over():
            self.is_game_over_bool = True 
        if self.snake.snake_head_x == self.food.x and self.snake.snake_head_y == self.food.y:
            if self.is_sound_on:
                self.sound.play()
            # If snake head matches foods precise x and y position we make tail longer and generate new food
            self.snake.tail.append((self.food.x, self.food.y))
            self.food.generate_new_food(self.snake)

        self.snake.draw_snake_tail()
        # adding and deleting from tail helps snake move forward.
        self.snake.tail.append(
                (self.snake.snake_head_x, self.snake.snake_head_y)
            )
        
        del self.snake.tail[0]
        self.food.draw()
        self.snake.snake_head_draw()
        if self.is_game_over_bool:
            self.pause = True