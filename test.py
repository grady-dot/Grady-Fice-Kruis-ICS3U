
import pygame, os, time


def check_collision(player, floors):
    for floor in floors:
        if player.colliderect(floor) == True:
            return True
    return False


def jump_collision(player_jump_box, floors):
    for floor in floors:
        if player_jump_box.colliderect(floor) == True:
            return True
    return False

def enemy_1_collision(enemy_hitbox_1, player_jump_box):
    
    for e in enemies_hitbox_1:
        if e.colliderect(player_jump_box) == True:
            return e
        
    return None


def check_coin(player, coins):
    for coin in coins:
        if player.colliderect(coin):
            return coin

    return None


pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side Scroller")

# Set up the game
clock = pygame.time.Clock()
running = True
won = False
score = 0

# Set up colours
SKY_BLUE = (143, 203, 255)
GRASS_GREEN = (131, 252, 77)
WHITE = (255, 255, 255)
POWER1 = (252, 3, 53)
RED = (255, 0, 0)
GREEN = (91, 179, 59)
BLACK = (0, 0, 0)
PLAYER = (255, 76, 181)
ENEMY1 = (245, 141, 66)
GOLD = (252, 215, 6)

# Set up the player
player_x = 100
player_y = 650
player_size = 35
speed = 5

player_jump_x = player_x
player_jump_y = player_y + 35

# Set up triangle enemy
enemy_1_x = 800
enemy_1_y = 660
enemy_1_size = 40
enemy_1_speed = 3


jump = False
jump_speed = 0

# Create the maze walls
floors = [
    pygame.Rect(0, 700, 1500, 500),
    pygame.Rect(0, 500, 100, 500),
    pygame.Rect(900, 500, 100, 500),
    pygame.Rect(500, 500, 300, 50),
    pygame.Rect(500, 300, 300, 50),
    pygame.Rect(200, 600, 300, 50),
    pygame.Rect(200, 400, 300, 50),
]

coins = [
    pygame.Rect(638, 250, 25, 25),
    pygame.Rect(338, 350, 25, 25),
    pygame.Rect(638, 450, 25, 25),
    pygame.Rect(338, 550, 25, 25),
]

enemies_1 = [
    pygame.Rect(enemy_1_x, enemy_1_y, enemy_1_size, enemy_1_size),
    pygame.Rect(enemy_1_x - 100, enemy_1_y, enemy_1_size, enemy_1_size),
    ]

enemies_hitbox_1 = [
    pygame.Rect(enemy_1_x, enemy_1_y - 3, enemy_1_size, 3),
    pygame.Rect(enemy_1_x - 100, enemy_1_y - 3, enemy_1_size, 3),
]


coin_hitbox = []

# Main game loop
while running:

    # Draw the background
    screen.fill(SKY_BLUE)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys being pressed
    keys = pygame.key.get_pressed()

    # Keep the player inside the screen
    if player_x < 0:
        player_x = 0

    if player_x > SCREEN_WIDTH - player_size:
        player_x = SCREEN_WIDTH - player_size

    if player_y < 0:
        player_y = 0

    if player_y > SCREEN_HEIGHT - player_size:
        player_y = SCREEN_HEIGHT - player_size

    if not won:

        # Update the player rectangle
        player = pygame.Rect(player_x, player_y, player_size, player_size)

        # Draw the hitbox
        player_jump_box = pygame.Rect(player_x + 5, player_y + player_size, player_size - 10, 3)
        #pygame.draw.rect(screen, RED, player_jump_box)

        enemy_hitbox_1 = pygame.Rect(enemy_1_x, enemy_1_y - 10, enemy_1_size, 10)
            
        # Gravity
        # Gravity
        if jump == False:
            if jump_collision(player_jump_box, floors) == False:
                player_y += 7
            else:
                for floor in floors:
                    if player_jump_box.colliderect(floor):
                        player_y = floor.top - player_size

        # Jump
        if keys[pygame.K_SPACE]:
            if jump == False and jump_collision(player_jump_box, floors) == True:
                jump = True
                jump_speed = -10

                pygame.mixer.init()
                pygame.mixer.music.load("Jumper.mp3")
                pygame.mixer.music.play()

        # Move the player while jumping
        if jump == True:
            player_y += jump_speed
            jump_speed += 0.5
            if check_collision(player, floors) == True:
                player_y -= jump_speed
                jump = False

            if jump_speed > 10:
                jump_speed = 10

        # Move left
        if keys[pygame.K_a]:
            player_x -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)

            if check_collision(player, floors) == True:
                player_x += speed
                jumping = False

        # Move right
        if keys[pygame.K_d]:
            player_x += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)

            if check_collision(player, floors) == True:
                player_x -= speed
                jumping = False

        # Enemy 1 movements
        #for enemy_1 in enemies_1 and enemy_hitbox_1 in enemies_hitbox_1
        #enemy_1_x += enemy_1_speed
        



        #if enemy_1_collision(enemy_hitbox_1, player_jump_box) == True:
        if jump_speed >= 0:
            select_enemy = enemy_1_collision(enemy_hitbox_1, player_jump_box)
            if select_enemy != None:
                enemies_1.remove(select_enemy)
                #enemies_1.pop(select_enemy)
            #if len(enemies_1) >= 1:
                #enemies_1.pop(0)
                #enemies_hitbox_1.pop(0)
                pygame.mixer.init()
                pygame.mixer.music.load("Kill.mp3")
                pygame.mixer.music.play()

    # Check for coins
    collected_coin = check_coin(player, coins)
    
    if collected_coin != None:
        score += 1

        pygame.mixer.init()
        pygame.mixer.music.load("Coins.mp3")
        pygame.mixer.music.play()

        coins.remove(collected_coin)

    # Draw the floors
    for floor in floors:
        pygame.draw.rect(screen, GREEN, floor)

    # Keeps the player from dropping through the world
    player_jump_x = player_x
    player_jump_y = player_y + 100

    # Draw the coins
    for coin in coins:
        pygame.draw.ellipse(screen, GOLD, coin)
        coin_rect = pygame.Rect(coin)
        coin_hitbox.append(coin_rect)

    # Power Ups
    power_1 = pygame.Rect(37.5, 450, 25, 25)
    pygame.draw.ellipse(screen, POWER1, power_1)
    

    # Draw the player
    player = pygame.Rect(player_x, player_y, player_size, player_size)
    pygame.draw.ellipse(screen, PLAYER, player)
    eye_1 = pygame.Rect(player_x, player_y + 4, player_size / 2, player_size / 2)
    pygame.draw.ellipse(screen, WHITE, eye_1)
    eye_2 = pygame.Rect(player_x + 18, player_y + 4, player_size / 2, player_size / 2)
    pygame.draw.ellipse(screen, WHITE, eye_2)
    eye_3 = pygame.Rect(player_x + 3, player_y + 7, player_size / 3, player_size / 3)
    pygame.draw.ellipse(screen, BLACK, eye_3)
    eye_4 = pygame.Rect(player_x + 21, player_y + 7, player_size / 3, player_size / 3)
    pygame.draw.ellipse(screen, BLACK, eye_4)

    # Draw the enemy
    #enemy_1 = pygame.Rect(enemy_1_x, enemy_1_y, enemy_1_size, enemy_1_size)
    for enemy_1 in enemies_1:
        pygame.draw.ellipse(screen, ENEMY1, enemy_1)

    # Draw enemy hitbox
    #enemy_hitbox_1 = pygame.Rect(enemy_1_x, enemy_1_y - 10, enemy_1_size, 10)
    #for enemy_hitbox_1 in enemies_hitbox_1:
        #pygame.draw.rect(screen, RED, enemy_hitbox_1)

    font = pygame.font.SysFont(None, 48)
    message = font.render("COINS: " + str(score), True, GOLD)
    screen.blit(message, (10, 0))

    # Update the display
    pygame.display.flip()

    # Limit the game to 60 FPS
    clock.tick(60)

# Close Pygame
pygame.quit()
