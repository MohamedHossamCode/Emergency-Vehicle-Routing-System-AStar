# AI project
## Work flow
1. make a pull before working (to have your project up-to-date)
2. work on your branch first (if there is a need for sub-branch do it)
3. push your edits on your branch first
4. after finishing a task push it to main branch (wait until approval)
---
## Project requirments
**Emergency Vehicle Routing System [A*]:**
Model a fixed 10x10 city grid (100 cells). At least 15 road cells are blocked (hardcoded coordinates) and 10 road cells have an emergency-cleared bonus (travel cost halved). 
Use A* to route an ambulance from a fixed depot (cell 0,0) to 3 different fixed incident locations. 
Required output for each incident: (1) optimal path as cell coordinates, (2) total travel cost, (3) comparison with the standard route ignoring emergency bonuses (cost difference and cells saved), (4) total nodes expanded. 
The program must clearly print results for all 3 incidents in a table. [Bonus +2: GUI animated grid with ambulance moving along path] 