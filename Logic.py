from grid import *
import tkinter as tk

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
    # ================== GUI ==================
CELL_SIZE = 52
COLORS = {
    "empty":   "#ecf0f1",
    "start":   "#2ecc71",
    "goal":    "#e74c3c",
    "blocked": "#2c3e50",
    "bonus":   "#00cec9",
    "path":    "#f1c40f",
    "trail":   "#ffeaa7",
}
 
def draw_grid(highlight_path=None, trail=None, agent_pos=None):
    canvas.delete("all")
    highlight = set(highlight_path) if highlight_path else set()
    trail_set = set(trail) if trail else set()
 
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if (x, y) in trail_set:
                color = COLORS["trail"]
            elif (x, y) in highlight:
                color = COLORS["path"]
            elif (x, y) == start:
                color = COLORS["start"]
            elif (x, y) in INCIDENTS:
                color = COLORS["goal"]
            elif (x, y) in BLOCKED_CELLS:
                color = COLORS["blocked"]
            elif (x, y) in BONUS_CELLS:
                color = COLORS["bonus"]
            else:
                color = COLORS["empty"]
 
            canvas.create_rectangle(
                x*CELL_SIZE, y*CELL_SIZE,
                (x+1)*CELL_SIZE, (y+1)*CELL_SIZE,
                fill=color, outline="white", width=1
            )
 
            # Number the incident cells
            if (x, y) in INCIDENTS:
                idx = INCIDENTS.index((x, y)) + 1
                canvas.create_text(
                    x*CELL_SIZE + CELL_SIZE//2,
                    y*CELL_SIZE + CELL_SIZE//2,
                    text=str(idx),
                    font=("Arial", 13, "bold"),
                    fill="white"
                )
 
    # Draw ambulance at interpolated position
    if agent_pos is not None:
        px, py = agent_pos
        canvas.create_text(
            px*CELL_SIZE + CELL_SIZE//2,
            py*CELL_SIZE + CELL_SIZE//2,
            text="🚑",
            font=("Arial", 18)
        )
 
def animate(path, step=0, t=0, trail=None):
    if trail is None:
        trail = []
 
    if step >= len(path) - 1:
        drawn = [c for c, _ in path]
        draw_grid(highlight_path=drawn, trail=[], agent_pos=path[-1][0])
        return
 
    drawn_so_far = [path[j][0] for j in range(step + 1)]
 
    (x1, y1) = path[step][0]
    (x2, y2) = path[step + 1][0]
    px = x1 + (x2 - x1) * t
    py = y1 + (y2 - y1) * t
 
    draw_grid(highlight_path=drawn_so_far, trail=trail, agent_pos=(px, py))
 
    t += 0.1
    if t >= 1:
        new_trail = trail + [path[step][0]]
        animate(path, step + 1, 0, new_trail)
    else:
        root.after(30, lambda: animate(path, step, t, trail))
 
def run():
    g_idx = goal_var.get()
    has_bonus = bonus_var.get()
    sol_data = Astar(start, INCIDENTS, has_bonus)
    result_list = sol_data[g_idx]
    result = result_list[0] if result_list else None
    
    if result is None:
        info.config(text="No path found!")
        return
 
    path, cost, visited, hb = result
    bonus_label = "With Bonus" if hb else "Without Bonus"
    info.config(text=f"{bonus_label}  |  Cost: {cost}  |  Visited: {visited}  |  Steps: {len(path)}")
    animate(path)
 
def reset():
    draw_grid()
    info.config(text="")
 
root = tk.Tk()
root.title("🚑 Ambulance Pathfinding System")
root.configure(bg="#1a1a2e")
root.resizable(False, False)
 
title_label = tk.Label(root, text="🚑 Ambulance Pathfinding — A*",
                       font=("Arial", 14, "bold"), bg="#1a1a2e", fg="white")
title_label.pack(pady=(10, 4))
 
# Legend
legend_frame = tk.Frame(root, bg="#1a1a2e")
legend_frame.pack(pady=2)
legend_items = [
    ("#2ecc71", "Start"),
    ("#e74c3c", "Incident"),
    ("#00cec9", "Bonus Road"),
    ("#2c3e50", "Blocked"),
    ("#f1c40f", "Path"),
]
for color, label in legend_items:
    tk.Label(legend_frame, bg=color, width=2, relief="flat").pack(side="left", padx=2)
    tk.Label(legend_frame, text=label, bg="#1a1a2e", fg="white",
             font=("Arial", 9)).pack(side="left", padx=(0, 8))
 
canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE,
                   bg="#1a1a2e", highlightthickness=0)
canvas.pack(padx=10, pady=8)
draw_grid()
 
# Goal selection
ctrl_frame = tk.Frame(root, bg="#1a1a2e")
ctrl_frame.pack(pady=4)
tk.Label(ctrl_frame, text="Goal:", bg="#1a1a2e", fg="white",
         font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6)
goal_var = tk.IntVar(value=0)
for i in range(3):
    tk.Radiobutton(ctrl_frame, text=f"Incident {i+1} {INCIDENTS[i]}",
                   variable=goal_var, value=i,
                   bg="#1a1a2e", fg="white", selectcolor="#16213e",
                   activebackground="#1a1a2e", activeforeground="white",
                   font=("Arial", 9)).grid(row=0, column=i+1, padx=4)
 
# Bonus toggle
bonus_frame = tk.Frame(root, bg="#1a1a2e")
bonus_frame.pack(pady=4)
tk.Label(bonus_frame, text="Bonus Roads:", bg="#1a1a2e", fg="white",
         font=("Arial", 10, "bold")).pack(side="left", padx=6)
bonus_var = tk.BooleanVar(value=True)
tk.Radiobutton(bonus_frame, text=" Use Bonus (cost 0.5)",
               variable=bonus_var, value=True,
               bg="#1a1a2e", fg="#00cec9", selectcolor="#16213e",
               activebackground="#1a1a2e", activeforeground="#00cec9",
               font=("Arial", 9)).pack(side="left", padx=6)
tk.Radiobutton(bonus_frame, text=" Ignore Bonus (cost 1.0)",
               variable=bonus_var, value=False,
               bg="#1a1a2e", fg="#fd79a8", selectcolor="#16213e",
               activebackground="#1a1a2e", activeforeground="#fd79a8",
               font=("Arial", 9)).pack(side="left", padx=6)
 
# Buttons
btn_frame = tk.Frame(root, bg="#1a1a2e")
btn_frame.pack(pady=6)
tk.Button(btn_frame, text="  Start  ", command=run,
          bg="#0984e3", fg="white", font=("Arial", 11, "bold"),
          relief="flat", padx=10, pady=4).pack(side="left", padx=8)
tk.Button(btn_frame, text="  Reset  ", command=reset,
          bg="#636e72", fg="white", font=("Arial", 11, "bold"),
          relief="flat", padx=10, pady=4).pack(side="left", padx=8)
 
info = tk.Label(root, text="", font=("Arial", 11), bg="#1a1a2e", fg="#dfe6e9")
info.pack(pady=(4, 12))
 
root.mainloop()
