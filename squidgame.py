import pygame
import random
import time
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 200, 0)
SAND = (194, 178, 128)
PLAYER_COLOR = (50, 50, 200)

START = 0
PLAYING = 1
GAMEOVER = 2
HELP = 3

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Red Light, Green Light")
        self.clock = pygame.time.Clock()
        
        self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 32)
        
        self.help_btn_rect = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 40)
        
        self.state = START
        self.reset_game()

    def reset_game(self):
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50]
        self.player_speed = 1.5
        self.finish_line_y = 80
        self.light_state = "GREEN"
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, random.randint(2000, 4000))
        
        self.game_result = ""
        self.limit_time = 15
        self.start_time = time.time()
        
        self.enemies = []
        for _ in range(8):
            ex = random.randint(50, SCREEN_WIDTH - 50)
            ey = random.randint(150, SCREEN_HEIGHT - 150)
            self.enemies.append(pygame.Rect(ex, ey, 40, 40))

    def draw_player(self, x, y):
        pygame.draw.rect(self.screen, PLAYER_COLOR, (x - 15, y - 15, 30, 30))
        pygame.draw.circle(self.screen, (200, 150, 120), (x, y - 25), 12)

    def draw_doll(self, state):
        if state == "GREEN": color = GREEN
        elif state == "YELLOW": color = YELLOW
        else: color = RED
        pygame.draw.circle(self.screen, color, (SCREEN_WIDTH // 2, 40), 30)
        pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH // 2 - 10, 35), 4)
        pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH // 2 + 10, 35), 4)

    def draw_text(self, text, font, color, x_off, y_off):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(SCREEN_WIDTH // 2 + x_off, SCREEN_HEIGHT // 2 + y_off))
        self.screen.blit(img, rect)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == START and self.help_btn_rect.collidepoint(event.pos):
                        self.state = HELP
                    elif self.state == HELP:
                        self.state = START

                if event.type == pygame.KEYDOWN:
                    if (self.state == START or self.state == GAMEOVER) and event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.start_time = time.time()
                        self.state = PLAYING

                if event.type == self.timer_event and self.state == PLAYING:
                    if self.light_state == "GREEN":
                        self.light_state = "YELLOW"
                        pygame.time.set_timer(self.timer_event, 800)
                    elif self.light_state == "YELLOW":
                        self.light_state = "RED"
                        pygame.time.set_timer(self.timer_event, random.randint(1500, 3000))
                    else:
                        self.light_state = "GREEN"
                        pygame.time.set_timer(self.timer_event, random.randint(2000, 4000))

            if self.state == PLAYING:
                keys = pygame.key.get_pressed()
                moving = False
                if keys[pygame.K_UP]: self.player_pos[1] -= self.player_speed; moving = True
                if keys[pygame.K_DOWN]: self.player_pos[1] += self.player_speed; moving = True
                if keys[pygame.K_LEFT]: self.player_pos[0] -= self.player_speed; moving = True
                if keys[pygame.K_RIGHT]: self.player_pos[0] += self.player_speed; moving = True

                player_rect = pygame.Rect(self.player_pos[0]-15, self.player_pos[1]-15, 30, 30)
                for enemy in self.enemies:
                    enemy.y += 2
                    if enemy.y > SCREEN_HEIGHT:
                        enemy.y = 0
                        enemy.x = random.randint(50, SCREEN_WIDTH - 50)
                    if player_rect.colliderect(enemy):
                        self.state = GAMEOVER
                        self.game_result = "HIT BY ENEMY!"

                if self.light_state == "RED" and moving:
                    self.state = GAMEOVER
                    self.game_result = "ELIMINATED!"
                
                if self.player_pos[1] <= self.finish_line_y:
                    self.state = GAMEOVER
                    self.game_result = "SURVIVED!"
                
                elapsed = time.time() - self.start_time
                if elapsed >= self.limit_time:
                    self.state = GAMEOVER
                    self.game_result = "TIME UP!"

            self.screen.fill(SAND)
            
            if self.state == START:
                self.draw_text("RED LIGHT, GREEN LIGHT", self.font_large, RED, 0, -50)
                self.draw_text("Press SPACE to Start", self.font_small, BLACK, 0, 50)
                pygame.draw.rect(self.screen, BLACK, self.help_btn_rect, 2)
                self.draw_text("           HELP", self.font_small, BLACK, 290, -270)

            elif self.state == PLAYING:
                pygame.draw.line(self.screen, BLACK, (0, self.finish_line_y), (SCREEN_WIDTH, self.finish_line_y), 5)
                timer_val = max(0, int(self.limit_time - (time.time() - self.start_time)))
                self.draw_text(f"Time: {timer_val}s", self.font_small, BLACK, -300, -260)
                
                l_color = GREEN if self.light_state == "GREEN" else YELLOW if self.light_state == "YELLOW" else RED
                self.draw_text(self.light_state, self.font_large, l_color, 0, 150)

                for enemy in self.enemies:
                    pygame.draw.rect(self.screen, (100, 0, 0), enemy)
                    pygame.draw.rect(self.screen, RED, enemy, 3)
                
                self.draw_doll(self.light_state)
                self.draw_player(self.player_pos[0], self.player_pos[1])

            elif self.state == GAMEOVER:
                res_color = GREEN if self.game_result == "SURVIVED!" else RED
                self.draw_text(self.game_result, self.font_large, res_color, 0, -50)
                self.draw_text("Press SPACE to Try Again", self.font_small, BLACK, 0, 50)

            elif self.state == HELP:
                self.draw_text("HOW TO PLAY", self.font_large, BLACK, 0, -100)
                self.draw_text("Stop: When RED LIGHT appears", self.font_small, BLACK, 0, -20)
                self.draw_text("Be Aware: When YELLOW LIGHT appears", self.font_small, BLACK, 0, 30)
                self.draw_text("Avoid: Red Squares (Enemy)", self.font_small, BLACK, 0, 80)
                self.draw_text("Click to return", self.font_small, (100, 100, 100), 0, 180)

            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    Game().run()