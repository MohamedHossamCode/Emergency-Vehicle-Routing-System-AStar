

def Astar(goal1,goal2,goal3):
    heuristic={

        
    }
    for i in range(0,11,1):
    if i+1==11:
        continue
   
    for j in range(0,11,1):
     if j+1==11:
         continue
     heuristic.update({(i,j):abs(i-4)+abs(j-9)})#Manhattan Distance
     
    visited=[]
    g_cost=0;
    queue=[[(0,0),0]]
    while queue:
        queue.sort(key=path_f_cost)
        path=queue.pop(0)
        cell=path[-1][0]
        if cell in visited or cell in BLOCKED_CELLS:
          continue
        visited.append(cell)
        g_cost=g_cost+1
        if node==goal1 or goal2 or goal3:
            return path
            
        else:
         if cell[0]!=0 and cell[0]!=10 and cell[1]!=0 and cell[1]!=10:
           possible_path=[((cell[0]+1,cell[1]),g_cost),((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]-1),g_cost),((cell[0],cell[1]+1),g_cost)]

         if cell==(0,0):
             possible_path=[((cell[0]+1,cell[1]),g_cost),((cell[0],cell[1]+1),g_cost)]

         if(cell==(0,10)):
            possible_path=[((cell[0]+1,cell[1]),g_cost),((cell[0],cell[1]-1),g_cost)]

         if(cell==(10,0)):
              possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]+1),g_cost)]

         if(cell==(10,10)):
             possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]-1),g_cost)]

         if(cell[0]==0 and cell!=(0,0) and cell!=(0,10)):
               possible_path=[((cell[0],cell[1]-1),g_cost),((cell[0],cell[1]+1),g_cost),((cell[0]+1,cell[1]),g_cost)]

         if(cell[0]==10 and cell!=(10,0) and cell!=(10,10)):
               possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]+1),g_cost),((cell[0],cell[1]-1),g_cost)]
             
         if(cell[1]==0 and cell!=(10,0) and cell!=(10,0)):
               possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0]+1,cell[1]),g_cost),((cell[0],cell[1]+1),g_cost)]

         if(cell[1]==10 and cell!=(10,10) and cell!=(0,10)):
               possible_path=[((cell[0]-1,cell[1]),g_cost),((cell[0],cell[1]-1),g_cost),((cell[0]+1,cell[1]),g_cost)]
         

             
         for(cell2, cost) in possible_path:
                new_path=path.copy()
                possible_path.append((cell2),cost)      
                queue.append(new_path)
                print(queue)

