import random
import pygame


city_width = 20
city_height = 20


num_squares = 20
num_intersections = 40


city = [[' ' for _ in range(city_width)] for _ in range(city_height)]


for _ in range(num_squares):
    x = random.randint(1, city_width - 2)
    y = random.randint(1, city_height - 2)
    while city[y][x] != ' ' or (city[y][x-1] == '@' or city[y][x+1] == '@' or city[y-1][x] == '@' or city[y+1][x] == '@'):
        x = random.randint(1, city_width - 2)
        y = random.randint(1, city_height - 2)
    city[y][x] = '@'

for _ in range(num_intersections):
    x = random.randint(1, city_width - 2)
    y = random.randint(1, city_height - 2)
    while city[y][x] != ' ' or (city[y][x-1] == '@' or city[y][x+1] == '@' or city[y-1][x] == '@' or city[y+1][x] == '@')  or (city[y][x-1] == '#' or city[y][x+1] == '#' or city[y-1][x] == '#' or city[y+1][x] == '#'):
        x = random.randint(1, city_width - 2)
        y = random.randint(1, city_height - 2)
    city[y][x] = '#'

directions = [
    [(0, 1), (0, -1)],  
    [(-1, 0), (1, 0)]  
]


num_cars = int(input("Enter the number of cars: "))
cars = []
for i in range(num_cars):
    x = random.randint(1, city_width - 2)
    y = random.randint(1, city_height - 2)
    while city[y][x] != ' ':
        x = random.randint(1, city_width - 2)
        y = random.randint(1, city_height - 2)
    direction = random.choice(directions[x % 2])
    cars.append((x, y, direction))


pygame.init()


screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('City Simulation')


def update_car(car , directions):
    x, y, direction = car
    dx, dy = direction
    new_x, new_y = (x + dx) % 20, (y + dy) % 20
    if city[new_y][new_x] == '@':

        if (dx, dy) == (0, 1):
            new_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        elif (dx, dy) == (0, -1):
            new_directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        elif (dx, dy) == (1, 0):
            new_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        elif (dx, dy) == (-1, 0):
            new_directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        
        new_direction = None
        for d in new_directions:
            if d != (-dx, -dy) and (new_x + d[0], new_y + d[1]) not in cars:
                new_direction = d
                break
        
        if new_direction is None:
            return None  
        else:
            direction = new_direction

    elif city[new_y][new_x] == '#':

        allowed_directions = []
        for d in directions[new_x % 2]:
            if d != (-dx, -dy) and city[new_y+d[1]][new_x+d[0]] != '@' and (new_x + d[0], new_y + d[1]) not in cars:
                allowed_directions.append(d)
        if not allowed_directions:
            return None  
        else:
            direction = random.choice(allowed_directions)

    return (new_x, new_y, direction)


running = True
clock = pygame.time.Clock()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    for i in range(len(cars)):
        new_car = update_car(cars[i], directions)
        if new_car is not None:
            cars[i] = new_car


    screen.fill((255, 255, 255))
    square_color = (128, 128, 128)
    street_color = (200, 200, 200)
    car_color = (255, 0, 0)
    square_size = screen_width // city_width
    street_width = 2
    for y in range(city_height):
        for x in range(city_width):
            rect = pygame.Rect(x * square_size, y * square_size, square_size, square_size)
            if city[y][x] == '@':
                pygame.draw.rect(screen, square_color, rect)
            else:
                pygame.draw.rect(screen, street_color, rect)
            if city[y][x] == '#' and x % 2 == y % 2:
                pygame.draw.line(screen, (0, 0, 0), (x * square_size, y * square_size + square_size // 2),
                                 ((x + 1) * square_size, y * square_size + square_size // 2), street_width)
            elif city[y][x] == '#' and x % 2 != y % 2:
                pygame.draw.line(screen, (0, 0, 0), (x * square_size + square_size // 2, y * square_size),
                                 (x * square_size + square_size // 2, (y + 1) * square_size), street_width)
    for car in cars:
        x, y, _ = car
        pygame.draw.circle(screen, car_color, (x * square_size + square_size // 2, y * square_size + square_size // 2),
                           square_size // 3)

    pygame.display.flip()
    clock.tick(5)  

pygame.quit()
