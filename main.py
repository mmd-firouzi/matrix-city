import random 
 
city_width = 20 
city_height = 20 
 
num_squares = 20 
num_intersections = 40 
 

city = [[' ' for _ in range(city_width)] for _ in range(city_height)] # create the city 
 

for _ in range(num_squares):  # randomly place squares
    x = random.randint(1, city_width - 2) 
    y = random.randint(1, city_height - 2) 
    while city[y][x] != ' ' or (city[y][x-1] == '@' or city[y][x+1] == '@' or city[y-1][x] == '@' or city[y+1][x] == '@'): 
        x = random.randint(1, city_width - 2) 
        y = random.randint(1, city_height - 2) 
    city[y][x] = '@' 
 

for _ in range(num_intersections):  # randomly place intersections 
    x = random.randint(1, city_width - 2) 
    y = random.randint(1, city_height - 2) 
    while city[y][x] != ' ' or (city[y][x-1] == '@' or city[y][x+1] == '@' or city[y-1][x] == '@' or city[y+1][x] == '@')  or (city[y][x-1] == '#' or city[y][x+1] == '#' or city[y-1][x] == '#' or city[y+1][x] == '#'): 
        x = random.randint(1, city_width - 2) 
        y = random.randint(1, city_height - 2) 
    city[y][x] = '#' 
 

directions = [ 
    [(0, 1), (0, -1)],  # horizontal streets 
    [(-1, 0), (1, 0)]  # vertical streets 
] 
 
#starting positions and directions of the cars 
num_cars = int(input("Enter the number of cars: ")) 
cars = [] 
for i in range(num_cars): 
    x = random.randint(1, city_width - 2) 
    y = random.randint(1, city_height - 2) 
    while city[y][x] != ' ': 
        x = random.randint(1, city_width - 2) 
        y = random.randint(1, city_height - 2) 
    direction = random.choice(directions[x % 2]) #odd or even rows and column
    cars.append((x, y, direction)) 
 

def update_car(car):
    x, y, direction = car
    dx, dy = direction
    new_x, new_y = (x + dx) % 20, (y + dy) % 20

    if city[new_y][new_x] == '@':
        # move clockwise around the square
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

    elif city[new_y][new_x] == '#':     # randomly choose
        allowed_directions = []
        for d in directions[x % 2]:
            if (new_x + d[0], new_y + d[1]) not in cars:
                allowed_directions.append(d)
        
        if not allowed_directions:
            return None 
        else:
            direction = random.choice(allowed_directions)

    else:

        if (new_x + dx, new_y + dy) in cars:
            return None
    
    return (new_x, new_y, direction)

 
def print_city(cars): 
    for y, row in enumerate(city): 
        for x, cell in enumerate(row): 
            if (x, y) in [(c[0], c[1]) for c in cars]: 
                print('*', end='') 
            elif cell == ' ': 
                print('.', end='')
            else: 
                print(cell, end='') 
            print(' ', end='') 
        print() 
    for x, y, _ in cars: 
        print(f'car at ({x}, {y})') 

# run the simulation 
num_steps = int(input("Enter the number of steps: ")) 
for step in range(num_steps): 
    print(f'step {step}:') 
    new_cars = [] 
    for car in cars: 
        new_car = update_car(car) 
        if new_car is not None: 
            new_cars.append(new_car) 
    cars = new_cars 
    print_city(cars)
