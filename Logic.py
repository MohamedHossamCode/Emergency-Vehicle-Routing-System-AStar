import grid

def Astar(start,goal1,goal2,goal3):
    # heuristic={
        
    # }

    # for i in range(0,11,1):
    #     if i+1==11:
    #         continue

    # for j in range(0,11,1):
    #     if j+1==11:
    #         continue
    # heuristic.update({(i,j):abs(i-4)+abs(j-9)})#Manhattan Distance
    visited=[]
    queue=[[(start,0)]]
    # queue:
    # [
    #     [((0,0),0)], #path 1
    #     [((0,0),0),((1,0),1)], #path 2
    #]

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

        # else:
        #     if cell[0]!=0 and cell[0]!=10 and cell[1]!=0 and cell[1]!=10:
        #         possible_path=[((cell[0]+1,cell[1]),g_cost),((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]-1),g_cost),((cell[0],cell[1]+1),g_cost)]

        #     if cell==(0,0):
        #         possible_path=[((cell[0]+1,cell[1]),g_cost),((cell[0],cell[1]+1),g_cost)]

        #     if(cell==(0,10)):
        #         possible_path=[((cell[0]+1,cell[1]),g_cost),((cell[0],cell[1]-1),g_cost)]

        #     if(cell==(10,0)):
        #         possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]+1),g_cost)]

        #     if(cell==(10,10)):
        #         possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]-1),g_cost)]

        #     if(cell[0]==0 and cell!=(0,0) and cell!=(0,10)):
        #         possible_path=[((cell[0],cell[1]-1),g_cost),((cell[0],cell[1]+1),g_cost),((cell[0]+1,cell[1]),g_cost)]

        #     if(cell[0]==10 and cell!=(10,0) and cell!=(10,10)):
        #         possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]+1),g_cost),((cell[0],cell[1]-1),g_cost)]
                
        #     if(cell[1]==0 and cell!=(10,0) and cell!=(10,0)):
        #         possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0]+1,cell[1]),g_cost),((cell[0],cell[1]+1),g_cost)]

        #     if(cell[1]==10 and cell!=(10,10) and cell!=(0,10)):
        #         possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]-1),g_cost),((cell[0]+1,cell[1]),g_cost)]
            
        # for(cell2, cost) in possible_path:
        #         new_path=path.copy()
        #         possible_path.append((cell2),cost)      
        #         queue.append(new_path)
        #         print(queue)

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
print(sol)