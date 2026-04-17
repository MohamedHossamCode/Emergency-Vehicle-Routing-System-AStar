'''
import grid
def Astar(start,goal1,goal2,goal3):
  

    while queue:
        queue.sort(key=lambda path: path_f_cost(path, goal1))
        path=queue.pop(0)
        cell,g_cost=path[-1] #[(cell,g_cost)]
        if cell in visited or cell in grid.BLOCKED_CELLS:
            continue
        visited.append(cell)

        if cell==goal1 or cell == goal2 or cell == goal3:
            return path,g_cost,len(visited)
        
        #Explore neighbors
        for neighbor in get_neighbors(cell):
            if neighbor not in visited and neighbor not in grid.BLOCKED_CELLS:
                new_g = g_cost + grid.get_cell_cost(neighbor)
                new_path=path.copy()
                new_path.append((neighbor,new_g))
                queue.append(new_path)

        

def heuristic_cost(cell,goal):
    return abs(cell[0]-goal[0])+abs(cell[1]-goal[1])

def get_neighbors(cell): #Returns valid moves
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dx, dy in directions:
        nx = cell[0] + dx
        ny = cell[1] + dy
        #Check if the new move within the grid or not
        if 0 <= nx < grid.GRID_SIZE and 0 <= ny < grid.GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors

def path_f_cost(path,goal):
    cell,g = path[-1]
    return g + heuristic_cost(cell,goal) #f(n)=g(n)+h(n)

sol = Astar(grid.start,grid.INCIDENTS[0],grid.INCIDENTS[1],grid.INCIDENTS[2])
print("Path:", [cell for cell, cost in sol[0]])

print("Total Cost:", sol[1])
print("Nodes Visited:", sol[2])
print("Path Length:", len(sol[0]))
'''

def Astar(start, goal1, goal2, goal3):

 is_emergency=[True, False]
 for is_emergency_true in is_emergency: 
    start = (0, 0)
    visited = []
    #loopingبنعرف حالة الطوارق مرة بصح و مرة بخظأ من خلال ال
    queue = [[(start, 0)]]
    while queue:

        queue.sort(key=lambda path: path_f_cost(path, goal1))
        path = queue.pop(0)
        cell, g_cost = path[-1]  # [(cell,g_cost)]
        if cell in visited or cell in grid.BLOCKED_CELLS:
            continue
        visited.append(cell)

        if cell == goal1 or cell == goal2 or cell == goal3:
            info=[path, g_cost, len(visited),is_emergency_true]
            print("Path:", [cell for cell, cost in info[0]])
            print("Total Cost:", info[1])
            print("Nodes Visited:", info[2])
            print("Path Length:", len(info[0]))
            print(info)
            print("______________________________________________________________________________________________________________________________________________________________________________________________")
             #print() هنا ضروري علشان نعرف نطبع اكثر من قيمة
             #return هترجع قيمة وحدة بس
             

        # Explore neighbors
        for neighbor in get_neighbors(cell):
            if neighbor not in visited and neighbor not in grid.BLOCKED_CELLS:
                new_g = g_cost + grid.get_cell_cost(neighbor, is_emergency_true)
                new_path = path.copy()
                new_path.append((neighbor, new_g))
                queue.append(new_path)


def heuristic_cost(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def get_neighbors(cell):  # Returns valid moves
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dx, dy in directions:
        nx = cell[0] + dx
        ny = cell[1] + dy
        # Check if the new move within the grid or not
        if 0 <= nx <= grid.GRID_SIZE and 0 <= ny <=grid.GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors


def path_f_cost(path, goal):
    cell, g = path[-1]
    return g + heuristic_cost(cell, goal)  # f(n)=g(n)+h(n)


Astar(grid.start, grid.INCIDENTS[0], grid.INCIDENTS[1], grid.INCIDENTS[2])
