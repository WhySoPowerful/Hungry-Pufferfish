import pygame
import datetime
import random
import os

startTime = datetime.datetime.now()

pygame.init()
font = pygame.font.SysFont("consolas", 25)
game_over_font = pygame.font.SysFont("consolas", 75)

clock = pygame.time.Clock()
FPS = 144
full_screen = False
version = 0.2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# width, height = pygame.display.list_modes()[0]
# if width == () and height == ():
#     width = 800
#     height = 600
screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Hungry Pufferfish")
icon = pygame.image.load("assets/icon.ico")
pygame.display.set_icon(icon)

apple_eaten_sound = pygame.mixer.Sound("assets/apple_eaten.wav")


def execution_time():
    end_time = datetime.datetime.now()
    time_difference = end_time - startTime
    total_time_s = time_difference.total_seconds()
    return f"The program ran for {round(total_time_s, 3)} seconds ({int(total_time_s * 1000)} ms), with a total of {round(total_time_s, 0) * FPS} frames ({FPS} fps). "


def show_version():
    version_text = font.render(f"v{version}", True, WHITE)
    screen.blit(version_text, (screen.get_width() - version_text.get_width(), screen.get_height() - version_text.get_height()))


def quit_game():
    global running
    print(execution_time())
    running = False
    pygame.quit()
    quit()


def game_over_func(speed):
    game_over_text = game_over_font.render("Game Over", True, RED)
    round_text = font.render(f"You lost at Round {speed}", True, RED)
    buttons_text = font.render("(R) to Retry - (Esc) to Quit", True, RED)

    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2 - game_over_text.get_height() // 2))
    screen.blit(round_text, (screen.get_width() // 2 - round_text.get_width() // 2, screen.get_height() // 2 + game_over_text.get_height() // 2))
    screen.blit(buttons_text, (screen.get_width() // 2 - buttons_text.get_width() // 2, screen.get_height() // 2 + buttons_text.get_height() + game_over_text.get_height() // 2 + round_text.get_height() // 2))


def snake(rect_size, snake_list, player_head, player_image, snake_length):
    # screen.fill(WHITE, (rect_pos_x, rect_pos_y, rect_size, rect_size))

    i = 0
    for coordinates in snake_list:
        # pygame.draw.rect(screen, WHITE, (coordinates[0], coordinates[1], rect_size, rect_size))
        if i < len(snake_list) - 1:  # this code gets executed on every iteration of the loop, except for the last
            i += 1
            player_image_smaller = pygame.transform.scale(player_image, (player_image.get_width() - snake_length + i, player_image.get_height() - snake_length + i))
            screen.blit(player_image_smaller, (coordinates[0] + (player_image_smaller.get_width() // 2) - i, coordinates[1] + (player_image_smaller.get_height() // 2) - i))
        else:  # this gets executed on the last iteration of the for loop, drawing the player head
            screen.blit(player_head, (coordinates[0], coordinates[1]))


def variables(speed, total_round_time, time_remaining):
    speed_text = font.render(f"Round = {speed}", True, WHITE)
    screen.blit(speed_text, (screen.get_width() // 2 - speed_text.get_width() // 2, speed_text.get_height() // 2))

    round_timer = font.render(f"Time remaining = {time_remaining - int(total_round_time)}s", True, WHITE)
    screen.blit(round_timer, (screen.get_width() // 2 - round_timer.get_width() // 2, speed_text.get_height() + (round_timer.get_height() // 2)))


running = True
game_over = False


def game_loop():
    global full_screen
    global game_over
    global screen

    player_image = pygame.image.load(os.path.join("assets/pufferfish_tail.png")).convert_alpha()

    player_head = pygame.image.load(os.path.join("assets/pufferfish.png")).convert_alpha()

    player_width = player_image.get_width()
    player_height = player_image.get_height()
    player_pos_x = screen.get_width() // 2 - player_width // 2
    player_pos_y = screen.get_height() // 2 - player_height // 2

    snake_list = []
    snake_length = 50

    direction_x = 0
    direction_y = 0
    speed = 1

    delay = 0

    timer_started = False
    time_remaining = 150
    total_round_time = 0

    # useless, gets assigned current time when game starts, wrote here just to delete
    # "local variable might be referenced before assignment" warning
    round_start_time = 0

    apple_image = pygame.image.load(os.path.join("assets/carrot.png")).convert_alpha()
    apple_x = random.randrange(0, screen.get_width() - apple_image.get_width())
    apple_y = random.randrange(0, screen.get_height() - apple_image.get_height())
    apple_eaten = False

    game_started = False

    while running:

        while game_over:
            screen.fill(BLACK)
            game_over_func(speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.type == pygame.KEYDOWN:
                    game_started = True
                    if event.key == pygame.K_ESCAPE:
                        quit_game()
                    if event.key == pygame.K_F11:
                        full_screen = not full_screen  # toggle fullscreen, didn't know you could do it
                        if full_screen:
                            screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)
                    if event.key == pygame.K_r:
                        game_over = False
                        game_loop()

            pygame.display.flip()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.VIDEORESIZE:
                    if not full_screen:
                        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.type == pygame.KEYDOWN:
                    game_started = True
                    if event.key == pygame.K_ESCAPE:
                        quit_game()
                    if event.key == pygame.K_F11:
                        full_screen = not full_screen  # toggle fullscreen, didn't know you could do it
                        if full_screen:
                            screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)

                    # directions
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if direction_x != 1:  # if player is going right, don't allow him to go left
                            direction_x = -1
                            direction_y = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if direction_x != -1:
                            direction_x = 1
                            direction_y = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if direction_y != 1:
                            direction_y = -1
                            direction_x = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if direction_y != -1:
                            direction_y = 1
                            direction_x = 0

            # portals (player off screen)
            if player_pos_x >= screen.get_width():
                player_pos_x = 0 - player_width
            elif player_pos_x + player_width <= 0:
                player_pos_x = screen.get_width()
            elif player_pos_y + player_height <= 0:
                player_pos_y = screen.get_height()
            elif player_pos_y >= screen.get_height():
                player_pos_y = 0 - player_height

            # generate a new apple if player enters apple's space
            if apple_x <= (player_pos_x + player_width//2) <= apple_x + apple_image.get_width() and apple_y <= (player_pos_y + player_height//2) <= apple_y + apple_image.get_height():
                apple_eaten = True

            # move player 1 time every 3 frames
            if delay % 3 == 2:
                player_pos_x += direction_x * speed
                player_pos_y += direction_y * speed

                snake_head = [player_pos_x, player_pos_y]
                snake_list.append(snake_head)

                delay = -1
            delay += 1

            screen.fill(BLACK)

            if not game_started:
                screen_text = font.render("Press W-A-S-D or arrow keys to play", True, WHITE)
                screen.blit(screen_text, (screen.get_width() // 2 - screen_text.get_width() // 2, screen.get_height() // 4))
            else:
                if not timer_started:
                    round_start_time = datetime.datetime.now()
                    timer_started = True
                if apple_eaten:
                    apple_eaten_sound.play()
                    apple_x = random.randrange(0, screen.get_width() - apple_image.get_width())
                    apple_y = random.randrange(0, screen.get_height() - apple_image.get_height())
                    apple_eaten = False
                    speed += 1
                    round_start_time = datetime.datetime.now()
                else:
                    screen.blit(apple_image, (apple_x, apple_y))
                    round_current_time = datetime.datetime.now()
                    round_time_difference = round_current_time - round_start_time
                    total_round_time = round_time_difference.total_seconds()
                    if total_round_time > time_remaining:
                        game_over = True

            if len(snake_list) > snake_length:
                snake_list.pop(0)
            snake(player_width, snake_list, player_head, player_image, snake_length)

            variables(speed, total_round_time, time_remaining)
            show_version()
            pygame.display.flip()
            clock.tick(FPS)


game_loop()
