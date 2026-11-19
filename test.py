
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
BLUE = (0, 0, 200)
RED = (255, 0, 0)
GREEN = (91, 179, 59)
BLACK = (0, 0, 0)
PLAYER = (255, 76, 181)
GOLD = (252, 215, 6)

# Set up the player
player_x = 100
player_y = 650
player_size = 35
speed = 5

player_jump_x = player_x
player_jump_y = player_y + 35

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


coin_hitbox = []

# Main game loop
while running:

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
        player_jump_box = pygame.Rect(player_x, player_y + player_size, player_size, 3)

        if check_coin(player, coins) == True:
            score += 1
            pygame.mixer.init()
            pygame.mixer.music.load("Coins.mp3")
            pygame.mixer.music.play()
            

        # Gravity
        # Gravity
        if jump == False:
            if jump_collision(player_jump_box, floors) == False:
                player_y += 5
            else:
                #player_y -= 1
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

    # Check for coins
    collected_coin = check_coin(player, coins)

    if collected_coin != None:
        score += 1

        pygame.mixer.init()
        pygame.mixer.music.load("Coins.mp3")
        pygame.mixer.music.play()

        coins.remove(collected_coin)
    # Draw the background
    screen.fill(SKY_BLUE)

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
    

    # Draw the player
    player = pygame.Rect(player_x, player_y, player_size, player_size)
    pygame.draw.ellipse(screen, PLAYER, player)

    font = pygame.font.SysFont(None, 48)
    message = font.render("COINS: " + str(score), True, GOLD)
    screen.blit(message, (10, 0))

    # Update the display
    pygame.display.flip()

    # Limit the game to 60 FPS
    clock.tick(60)

# Close Pygame
pygame.quit()
