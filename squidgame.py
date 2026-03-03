import pygame
import random
import time

# --- Configuration & Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
SAND = (194, 178, 128)
PLAYER_COLOR = (50, 50, 200)

# Game States
START = 0
PLAYING = 1
GAMEOVER = 2

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Red Light, Green Light")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 32)

        self.state = START
        self.reset_game()

    def reset_game(self):
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50]
        self.player_speed = 4
        self.finish_line_y = 80

        self.is_green_light = True
        self.timer_event = pygame.USEREVENT + 1
        self.phase_duration = random.randint(2000, 4000)
        pygame.time.set_timer(self.timer_event, self.phase_duration)

        self.game_result = ""
        self.start_time = time.time()
        self.limit_time = 30

    def draw_player(self, x, y):
        # Character Body
        pygame.draw.rect(self.screen, PLAYER_COLOR, (x - 15, y - 15, 30, 30))
        # Head
        pygame.draw.circle(self.screen, (200, 150, 120), (x, y - 25), 12)

    def draw_doll(self, is_green):
        color = GREEN if is_green else RED
        # Simple Doll Head
        pygame.draw.circle(self.screen, color, (SCREEN_WIDTH // 2, 40), 30)
        # Eyes
        pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH // 2 - 10, 35), 4)
        pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH // 2 + 10, 35), 4)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            # 1. EVENT HANDLING
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if (self.state == START or self.state == GAMEOVER) and event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = PLAYING

                if event.type == self.timer_event and self.state == PLAYING:
                    self.is_green_light = not self.is_green_light
                    self.phase_duration = random.randint(1000, 3500)
                    pygame.time.set_timer(self.timer_event, self.phase_duration)

            # 2. GAME LOGIC
            if self.state == PLAYING:
                keys = pygame.key.get_pressed()
                moving = False
                
                # Check movement
                if keys[pygame.K_UP]:
                    self.player_pos[1] -= self.player_speed
                    moving = True
                if keys[pygame.K_DOWN]:
                    self.player_pos[1] += self.player_speed
                    moving = True
                if keys[pygame.K_LEFT]:
                    self.player_pos[0] -= self.player_speed
                    moving = True
                if keys[pygame.K_RIGHT]:
                    self.player_pos[0] += self.player_speed
                    moving = True

                # Rule Check: Movement during Red Light
                if not self.is_green_light and moving:
                    self.state = GAMEOVER
                    self.game_result = "ELIMINATED!"

                # Win Condition
                if self.player_pos[1] <= self.finish_line_y:
                    self.state = GAMEOVER
                    self.game_result = "SURVIVED!"

                # Timer Check
                elapsed = time.time() - self.start_time
                if elapsed >= self.limit_time:
                    self.state = GAMEOVER
                    self.game_result = "TIME UP!"

            # 3. RENDERING
            self.screen.fill(SAND)

            if self.state == START:
                self.draw_text("RED LIGHT, GREEN LIGHT", self.font_large, RED, 0, -50)
                self.draw_text("Press SPACE to Start", self.font_small, BLACK, 0, 50)
            
            elif self.state == PLAYING:
                pygame.draw.line(self.screen, BLACK, (0, self.finish_line_y), (SCREEN_WIDTH, self.finish_line_y), 5)
                
                timer_val = max(0, int(self.limit_time - (time.time() - self.start_time)))
                self.draw_text(f"Time Left: {timer_val}s", self.font_small, BLACK, -300, -260)
                
                light_text = "GREEN LIGHT" if self.is_green_light else "RED LIGHT"
                light_color = GREEN if self.is_green_light else RED
                self.draw_text(light_text, self.font_large, light_color, 0, 150)
                
                self.draw_doll(self.is_green_light)
                self.draw_player(self.player_pos[0], self.player_pos[1])

            elif self.state == GAMEOVER:
                res_color = GREEN if self.game_result == "SURVIVED!" else RED
                self.draw_text(self.game_result, self.font_large, res_color, 0, -50)
                self.draw_text("Press SPACE to Try Again", self.font_small, BLACK, 0, 50)

            pygame.display.flip()

        pygame.quit()

    def draw_text(self, text, font, color, x_off, y_off):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(SCREEN_WIDTH // 2 + x_off, SCREEN_HEIGHT // 2 + y_off))
        self.screen.blit(img, rect)

if __name__ == "__main__":
    Game().run()