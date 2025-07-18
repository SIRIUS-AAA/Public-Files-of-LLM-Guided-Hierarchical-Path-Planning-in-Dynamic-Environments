'''
    A-star Algorithm (Version 5)
    Sirius
    2025.07.11
'''

import heapq
import math

def read_maps(filename):
    with open(filename, 'r') as f:
        content = f.read().split('\n\n')
    maps = []
    for map_str in content:
        if not map_str.strip():
            continue
        lines = map_str.split('\n')
        start = tuple(map(int, lines[1].split(': ')[1].split()))
        end = tuple(map(int, lines[2].split(': ')[1].split()))
        obstacles = set(tuple(map(int, line.split())) for line in lines[4:] if line.strip())
        maps.append({
            'map_num': int(lines[0].split()[1]),
            'start': start,
            'end': end,
            'obstacles': obstacles
        })
    return maps

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(map_data):
    start = map_data['start']
    end = map_data['end']
    obstacles = map_data['obstacles']
    
    # Directions: up, down, left, right (4-connected grid)
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, end)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        close_set.add(current)
        
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Check bounds (1-30) and not obstacle
            if (1 <= neighbor[0] <= 30 and 1 <= neighbor[1] <= 30 and 
                neighbor not in obstacles):
                
                tentative_g_score = gscore[current] + 1
                
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, float('inf')):
                    continue
                    
                if tentative_g_score < gscore.get(neighbor, float('inf')) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
    
    return None  # No path found

def write_paths(maps, output_filename):
    with open(output_filename, 'w') as f:
        for i, map_data in enumerate(maps, 1):
            path = a_star_search(map_data)
            f.write(f"Map {map_data['map_num']}\n")
            if path:
                f.write(f"Path Length: {len(path)-1}\n")  # Added line for path length
                f.write(f"Path: \n") # Added line Path:
                for step in path:
                    f.write(f"{step[0]} {step[1]}\n")
            else:
                f.write("Path Length: 0\n")  # Added line for path length when no path
                f.write("No path found\n")
            if i < len(maps):  # No extra newline after last map
                f.write("\n")

# Main execution
if __name__ == "__main__":
    input_filename = "Maps.txt"
    output_filename = "Paths by A-star Algorithm.txt"
    
    maps = read_maps(input_filename)
    write_paths(maps, output_filename)
    
    print(f"Paths written to {output_filename}")