import pygame
import os
import random

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("my first game")
pygame.init()
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
BULLET_VEL = 7 # bullet velocity
MAX_BULLETS = 3 
ENEMY_VEL = 2  # enemy velocity
SCORE = 0
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP = pygame.image.load('assignment5/player.png')
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SPACESHIP = pygame.image.load('assignment5/bomb.png') 
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
font = pygame.font.Font(None, 36)
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.vel = ENEMY_VEL
    
    def update(self):
        # move enemy from right to left
        self.rect.x -= self.vel
        
    def draw(self, window):
        window.blit(RED_SPACESHIP, (self.rect.x, self.rect.y))
    
    def is_off_screen(self):
        # check if enemy has moved off the left side of the screen
        return self.rect.x < -SPACESHIP_WIDTH

def draw_window(yellow, yellow_bullets, enemies, score):
    WIN.fill(WHITE) 
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for enemy in enemies:
        enemy.draw(WIN)
    
    # Draw the score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # Changed text color to black for visibility
    WIN.blit(score_text, (10, 10))
    
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.width < WIDTH: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HEIGHT: # DOWN
        yellow.y += VEL

def handle_bullets(yellow_bullets, enemies):
    global SCORE
    for bullet in yellow_bullets[:]:  # use a copy of the list to safely modify during iteration
        bullet.x += BULLET_VEL
        # remove bullet once it is off-screen
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            continue
        
        # check collisions with enemies
        for enemy in enemies[:]:
            if bullet.colliderect(enemy.rect): # pygame's collision detection between two rects
                yellow_bullets.remove(bullet)
                enemies.remove(enemy)
                SCORE += 1
                break # exit loop after collision is detected


def main():
    # initialize a Rect to store yellow ship's values
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = [] # a list to store bullets
    enemies = [] # a list to store enemies

    # enemy timing variables
    enemy_spawn_timer = 0
    enemy_spawn_delay = 120  # create a new enemy every 2 seconds (60 FPS * 2)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN: # ensure bullets happen with press
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
        
        # enemy spawning logic
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_delay:
            new_enemy = Enemy(WIDTH, random.randint(50, HEIGHT - SPACESHIP_HEIGHT - 50))
            enemies.append(new_enemy)
            enemy_spawn_timer = 0

        # update enemies
        for enemy in enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                enemies.remove(enemy)
        


        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        handle_bullets(yellow_bullets, enemies)
        score_text = font.render(f"Score: {SCORE}", True, (255, 255, 255))
        draw_window(yellow, yellow_bullets, enemies, SCORE)
        WIN.blit(score_text, (10, 10))
        
    pygame.quit() 

if __name__ == "__main__": 
    main()