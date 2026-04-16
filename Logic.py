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
        # Check if the new move within the grid or not
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
def Astar(start,incident,is_emergency):
 
       start=(0,0)
       visited=[]
       goal=incident[0]
       queue=[[(start,0)]]
       while queue:
   
     
        queue.sort(key=lambda path: path_f_cost(path))
        path=queue.pop(0)
        cell,g_cost=path[-1] #[(cell,g_cost)]
    
        if cell in visited or cell in BLOCKED_CELLS:
            continue
        visited.append(cell)
        if cell==goal:
             return goal,  path,  g_cost, len(visited)
             queue=[(start,0)]
             continue
        #Explore neighbors
        for neighbor in get_neighbors(cell):
            if neighbor not in visited and neighbor not in BLOCKED_CELLS:
                new_g = g_cost + get_cell_cost(neighbor,is_emergency) #the value of this emergency parametrt will be assigned to get_cell cost function 
                                                                        
                new_path=path.copy()
                new_path.append((neighbor,new_g))
                queue.append(new_path)



def heuristic_cost(cell,goal):
    
    if cell in BONUS_CELLS and emergency_true==True:
     return abs(cell[0]-goal[0])+abs(cell[1]-goal[1])/2 #condition for halving the heuristic cost
    else:
     return abs(cell[0]-goal[0])+abs(cell[1]-goal[1])
        

      
def get_neighbors(cell): #Returns valid moves
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for (dx, dy) in directions:
        nx = cell[0] + dx
        ny = cell[1] + dy
        # Check if the new move within the grid or not
        if 0 <= nx <= 10 and 0 <= ny <= 10:#max is 10 and min is 0 is the graph must be in these boundries
            neighbors.append((nx, ny))
            return neighbors

def path_f_cost(path,goal):
    cell,g = path[-1]
    return g + heuristic_cost(cell,goal) #f(n)=g(n)+h(n)
_
start=(0,0)

sol = Astar(start,incident,True)
print("goal:",sol[0])
print("Path:", [cell for cell, cost in sol[0]])
print("Total Cost:", sol[2])
print("Nodes Visited:", sol[3])
print("Path Length:", len(sol[1]))
print(sol)

print(sol)
                                                                                                   
