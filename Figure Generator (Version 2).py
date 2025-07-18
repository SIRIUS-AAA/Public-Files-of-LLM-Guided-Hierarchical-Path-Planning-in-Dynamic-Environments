'''
    Figure Generator (Version 2)
    Sirius
    2025.07.11

    Map Visualizer
    Generates 30x30 grid maps with paths from A* and Deepseek algorithms
    Start: Green triangle (▲)
    End: Red triangle (▼)
    Obstacles: Gray squares
    A* Path: Blue line
    Deepseek Path: Orange line
'''

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def read_maps(file_path):
    """Read map data from file including start, end, and obstacles"""
    maps = {}
    current_map = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Map'):
                current_map = line.split()[1]
                maps[current_map] = {'start': None, 'end': None, 'obstacles': []}
            elif line.startswith('Start:'):
                parts = line.split()
                maps[current_map]['start'] = (int(parts[1]), int(parts[2]))
            elif line.startswith('End:'):
                parts = line.split()
                maps[current_map]['end'] = (int(parts[1]), int(parts[2]))
            elif line and line[0].isdigit():
                parts = line.split()
                if len(parts) == 2:
                    maps[current_map]['obstacles'].append((int(parts[0]), int(parts[1])))
    return maps

def read_paths(file_path):
    """Read path coordinates from algorithm output files"""
    paths = {}
    current_map = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Map'):
                current_map = line.split()[1]
                paths[current_map] = []
            elif line and line[0].isdigit():
                parts = line.split()
                if len(parts) == 2:
                    paths[current_map].append((int(parts[0]), int(parts[1])))
    return paths

def plot_map(map_data, a_star_path, deepseek_path, map_num):
    """Visualize a single map with paths and markers"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Create grid background
    for x in range(1, 31):
        for y in range(1, 31):
            if (x, y) == map_data['start']:
                # Start point - green triangle (▲)
                ax.plot(x, y, 'g^', markersize=12, label='Start')
            elif (x, y) == map_data['end']:
                # End point - red triangle (▼)
                ax.plot(x, y, 'rv', markersize=12, label='End')
            elif (x, y) in map_data['obstacles']:
                # Obstacle - gray square
                rect = patches.Rectangle((x-0.5, y-0.5), 1, 1, 
                                      facecolor='gray', edgecolor='black')
                ax.add_patch(rect)
            else:
                # Empty cell - white square
                rect = patches.Rectangle((x-0.5, y-0.5), 1, 1, 
                                      facecolor='white', edgecolor='black')
                ax.add_patch(rect)
    
    # Plot A* algorithm path (blue)
    if a_star_path:
        a_star_x = [p[0] for p in a_star_path]
        a_star_y = [p[1] for p in a_star_path]
        ax.plot(a_star_x, a_star_y, color='blue', 
               linewidth=5, alpha=0.7, label='A* Path')
    
    # Plot Deepseek algorithm path (orange)
    if deepseek_path:
        deepseek_x = [p[0] for p in deepseek_path]
        deepseek_y = [p[1] for p in deepseek_path]
        ax.plot(deepseek_x, deepseek_y, color='orange', 
               linewidth=5, alpha=0.7, label='Deepseek Path')
    
    # Configure plot appearance
    ax.set_xlim(0.5, 30.5)
    ax.set_ylim(0.5, 30.5)
    ax.set_xticks(np.arange(1, 31, 1))
    ax.set_yticks(np.arange(1, 31, 1))
    ax.tick_params(axis='both', which='both', length=0)  # Remove tick marks
    ax.set_title(f'Figure of Map {map_num}')
    ax.legend(loc='upper right')
    ax.set_aspect('equal')
    
    # Create Figures directory if it doesn't exist
    if not os.path.exists('Figures'):
        os.makedirs('Figures')
    
    # Save and close
    plt.tight_layout()
    plt.savefig(f'Figures/Figure of Map {map_num}.png', dpi=300)
    plt.close()

def main():
    """Main function to process all maps"""
    # Read input files
    maps = read_maps('Maps.txt')
    a_star_paths = read_paths('Paths by A-star Algorithm.txt')
    deepseek_paths = read_paths('Paths by Deepseek.txt')
    
    # Generate visualization for each map
    for map_num in maps:
        plot_map(maps[map_num], 
                a_star_paths.get(map_num, []), 
                deepseek_paths.get(map_num, []), 
                map_num)

if __name__ == '__main__':
    main()