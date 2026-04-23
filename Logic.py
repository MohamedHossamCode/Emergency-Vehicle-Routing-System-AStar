from grid import *

def Astar(start, goals, forced_bonus=None):
    output = [[] for i in range(len(goals))]
    
    for row, goal in enumerate(goals):
        bonus_modes = [forced_bonus] if forced_bonus is not None else [True, False]
        
        for hb in bonus_modes:
            visited = []
            queue = [[(start, 0)]]
            found = False
            
            while queue:
                queue.sort(key=lambda path: path_f_cost(path, goal))
                path = queue.pop(0)
                cell, g_cost = path[-1]
                
                if cell in visited or cell in BLOCKED_CELLS:
                    continue
                visited.append(cell)

                if cell == goal:
                    info = [path, g_cost, len(visited), hb]
                    output[row].append(info)
                    found = True
                    break

                for neighbor in get_neighbors(cell):
                    if neighbor not in visited and neighbor not in BLOCKED_CELLS:
                        # Pass 'hb' to get the correct cost for this iteration
                        new_g = g_cost + get_cell_cost(neighbor, hb)
                        new_path = path.copy()
                        new_path.append((neighbor, new_g))
                        queue.append(new_path)
            
            if not found:
                output[row].append(None)
    return output

def heuristic_cost(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

def get_neighbors(cell):  # Returns valid moves
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dx, dy in directions:
        nx = cell[0] + dx
        ny = cell[1] + dy
        # Check if the new move within the grid or not
        if 0 <= nx <= GRID_SIZE and 0 <= ny <=GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors

def path_f_cost(path, goal):
    cell, g = path[-1]
    return g + heuristic_cost(cell, goal)  # f(n)=g(n)+h(n)


sol = Astar(start, INCIDENTS)
for goal_index, goal_solutions in enumerate(sol):
    print(f"Solutions for Goal {INCIDENTS[goal_index]}:")
    for solution in goal_solutions:
        path, total_cost, visited_count, has_bounes = solution
        print(f"Has Bounes: {has_bounes}",f"Path: {[cell for cell, _ in path]}", f"Total Cost: {total_cost}", f"Visited Cells: {visited_count}", sep="\n")
    print("\n")

print("summary:")
print("="*80)
print(f"{'Goal':>10} {'Has Bounes':>15} {'Total Cost':>15} {'Visited':>20} {'Path Length':>15}")
for goal_index, goal_solutions in enumerate(sol):
    goal = INCIDENTS[goal_index]
    with_bounes = goal_solutions[0]
    without_bounes = goal_solutions[1]
    total_cost_with_bounes = with_bounes[1]
    total_cost_without_bounes = without_bounes[1]
    visited_with_bounes = with_bounes[2]
    visited_without_bounes = without_bounes[2]
    path_length_with_bounes = len(with_bounes[0])
    path_length_without_bounes = len(without_bounes[0])

    print(f"{str(goal):>10} {str(True):>15} {total_cost_with_bounes:>15} {visited_with_bounes:>20} {path_length_with_bounes:>15}")
    print(f"{str(goal):>10} {str(False):>15} {total_cost_without_bounes:>15} {visited_without_bounes:>20} {path_length_without_bounes:>15}")
    print("-"*80)
    print(f"{'Saved':>10} {'':>15} {abs(total_cost_with_bounes - total_cost_without_bounes):>15} {abs(visited_with_bounes - visited_without_bounes):>20} {abs(path_length_with_bounes - path_length_without_bounes):>15}")
    print("="*80)
   