'''
    Map Generator (Version 2)
    Sirius 
    2025.07.11
'''

import random

def generate_map(map_num, size=30, obstacles=100):
    # Initialize empty grid (not actually used, just for conceptual understanding)
    grid = [[0 for _ in range(size)] for _ in range(size)]
    
    # Randomly select start and end points (1-30), ensuring they're different
    start = (random.randint(1, size), random.randint(1, size))
    end = start
    while end == start:
        end = (random.randint(1, size), random.randint(1, size))
    
    # Place obstacles ensuring they don't overlap with start or end points
    obstacles_list = []
    for _ in range(obstacles):
        while True:
            x, y = random.randint(1, size), random.randint(1, size)
            if (x, y) != start and (x, y) != end and (x, y) not in obstacles_list:
                obstacles_list.append((x, y))
                break
    
    # Format the map data as specified
    map_str = f"Map {map_num}\n"
    map_str += f"Start: {start[0]} {start[1]}\n"
    map_str += f"End: {end[0]} {end[1]}\n"
    map_str += "Obstacles:\n"
    for obs in obstacles_list:
        map_str += f"{obs[0]} {obs[1]}\n"
    
    return map_str

# Get user input for the number of maps to generate
while True:
    try:
        num_maps = int(input("Enter the number of maps to generate (1-100): "))
        if 1 <= num_maps <= 100:
            break
        else:
            print("Please enter a number between 1 and 100.")
    except ValueError:
        print("Please enter a valid integer.")

# Generate maps and write to file
with open("Maps.txt", "w") as f:
    for i in range(1, num_maps + 1):
        map_data = generate_map(i)
        f.write(map_data)
        if i < num_maps:  # No extra newline after the last map
            f.write("\n")

print(f"{num_maps} maps have been generated and saved to Maps.txt")