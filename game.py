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
        if player.colliderect(coin) == True:
            return True
    return False

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
previous_y = 0
jump_height = previous_y + 100

# Create the maze walls
floors = [
    pygame.Rect(0, 700, 1500, 500),
    pygame.Rect(0, 500, 100, 500),
    pygame.Rect(900, 500, 100, 500),
    pygame.Rect(500, 650, 500, 500),
    pygame.Rect(500, 500, 300, 50),
    pygame.Rect(100, 500, 100, 50),
]

coins = [
    pygame.Rect(500, 450, 25, 25)
]

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

        # Update the player rectangle
        player = pygame.Rect(player_x, player_y, player_size, player_size)

    if not won:

        # Draw the hitbox
        player_jump_box = pygame.Rect(player_jump_x, player_jump_y, player_size - 0.5, 3)

        player = pygame.Rect(player_x, player_y, player_size, player_size)

        if check_coin(player, coins) == True:
            score+=1

        #Gravity
        if jump_collision(player_jump_box, floors) == False:
            player_y += 5

        # Jump
        if jump_collision(player_jump_box, floors) == True:
            #if jump == False:
            
            if keys[pygame.K_SPACE]:
                if jump == False:
                    jump = True
                    previous_y = player_y
                else: 
                    player_y -= 150

                pygame.mixer.init()
                pygame.mixer.music.load("Jumper.mp3")
                pygame.mixer.music.play()

                if check_collision(player, floors) == True:
                    player_x += speed


    
        # Move left
        if keys[pygame.K_a]:
            player_x -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)

            if check_collision(player, floors) == True:
                player_x += speed

        # Move right
        if keys[pygame.K_d]:
            player_x += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)

            if check_collision(player, floors) == True:
                player_x -= speed

        # Move up
        #if keys[pygame.K_UP]:
        #    player_y -= speed
        #    player = pygame.Rect(player_x, player_y, player_size, player_size)

        #    if check_collision(player, floors) == True:
        #        player_y += speed

        # Move down
        #if keys[pygame.K_DOWN]:
        #    player_y += speed
        #    player = pygame.Rect(player_x, player_y, player_size, player_size)

        #    if check_collision(player, floors) == True:
        #        player_y -= speed

    # Draw the background
    screen.fill(SKY_BLUE)

    # Draw the floors
    for floor in floors:
        pygame.draw.rect(screen, GREEN, floor)

    #Keeps the player from dropping thru the world    
    player_jump_x = player_x
    player_jump_y = player_y + 35

    # Draw the coins
    for coin in coins:
        pygame.draw.ellipse(screen, GOLD, coin)

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