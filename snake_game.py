import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 640, 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
grey = (128, 128, 128)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 128, 0)

# Snake settings
snake_size = 10

# Font
font_style = pygame.font.SysFont(None, 50)


# Functions to display message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [width / 6, height / 3])


def wrap(left, right, top, bottom, x, y, x_change, y_change, width, height, side_of_manifold):
    if x >= width - snake_size:
        print(f"{right=}")
        if right == "point-compactified":
            x = width - snake_size
            x_change = -x_change
            y = height - y
        else:
            x = 0
            if right != left:
                y = height - y
                side_of_manifold = not side_of_manifold
    elif x <= 0:
        print(f"{left=}")
        if left == "point-compactified":
            x = 0
            x_change = -x_change
            y = height - y
        else:
            x = width - snake_size
            if right != left:
                y = height - y
                side_of_manifold = not side_of_manifold
    if y >= height:
        print(f"{bottom=}")
        if bottom == "point-compactified":
            y = height
            x = width - x
            y_change = -y_change
        else:
            y = 0
            if top != bottom:
                x = width - x
                side_of_manifold = not side_of_manifold
    elif y < 0:
        print(f"{top=}")
        if top == "point-compactified":
            y = 0
            x = width - x
            y_change = -y_change
        else:
            y = height
            if top != bottom:
                x = width - x
                side_of_manifold = not side_of_manifold
    print(f"{x=}")
    print(f"{y=}")
    print(f"{snake_size=}")
    return x, y, x_change, y_change, side_of_manifold

# Main function
def gameLoop():
    snake_speed = 15

    # Manifold settings
    top_edge_state = "straight"
    bottom_edge_state = "straight"
    left_edge_state = "straight"
    right_edge_state = "straight"

    # Food settings
    food_edge = "top"
    food_effect = "twisted"

    food_edges = ["left", "right", "top", "bottom"]
    food_effects = ["straight", "twisted", "point-compactified"]

    side_of_manifold = True

    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
    food_side_of_manifold = side_of_manifold

    clock = pygame.time.Clock()

    while not game_over:

        while game_close == True:
            win.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_size
                    x1_change = 0
                elif event.key == pygame.K_q:
                    Length_of_snake += 10
                elif event.key == pygame.K_e:
                    snake_speed += 5

        # Wrap around conditions for torus mode on sides
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_size

        # Apply wrap-around logic
        x1, y1, x1_change, y1_change, side_of_manifold = wrap(
            left_edge_state, 
            right_edge_state, 
            top_edge_state, 
            bottom_edge_state, 
            x1, 
            y1, 
            x1_change, 
            y1_change, 
            width, 
            height,
            side_of_manifold
        )

        x1 += x1_change
        y1 += y1_change
        win.fill(black)
        
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_Head.append(side_of_manifold)

        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for segment in snake_List:
            pygame.draw.rect(win, white if segment[2] else grey, [segment[0], segment[1], snake_size, snake_size])

        pygame.draw.rect(win, green if food_side_of_manifold else dark_green, [foodx, foody, snake_size, snake_size])

        pygame.display.update()

        if x1 == foodx and y1 == foody and side_of_manifold == food_side_of_manifold:
            print(f"{food_edge=}")
            print(f"{food_effect=}")

            if food_effect == "point-compactified":
                if food_edge == "top" or food_edge == "bottom":
                    top_edge_state = "point-compactified"
                    bottom_edge_state = "point-compactified"
                else:
                    left_edge_state = "point-compactified"
                    right_edge_state = "point-compactified"
            else:
                if food_edge == "top":
                    top_edge_state = food_effect
                    if bottom_edge_state == "point-compactified":
                        bottom_edge_state = food_effect
                if food_edge == "bottom":
                    bottom_edge_state = food_effect
                    if top_edge_state == "point-compactified":
                        top_edge_state = food_effect
                if food_edge == "left":
                    left_edge_state = food_effect
                    if right_edge_state == "point-compactified":
                        right_edge_state = food_effect
                if food_edge == "right":
                    right_edge_state = food_effect
                    if left_edge_state == "point-compactified":
                        left_edge_state = food_effect

            foodx = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_size) / 10.0) * 10.0

            food_edge = food_edges[round(random.randrange(0, len(food_edges)))]
            food_effect = food_effects[round(random.randrange(0, len(food_effects)))]

            if (top_edge_state == 'twisted' and bottom_edge_state == 'straight') or (top_edge_state == 'straight' and bottom_edge_state == 'twisted') or (left_edge_state == 'twisted' and right_edge_state == 'straight') or (left_edge_state == 'straight' and right_edge_state == 'twisted'):
                food_side_of_manifold = round(random.randint(0, 1)) == 1
            else:
                food_side_of_manifold = side_of_manifold

            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
