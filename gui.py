import customtkinter as ctk
import tkinter as tk
from grid import *
from Logic import *
CELL = 50
COLORS = {
    "empty":   "#ecf0f1",
    "start":   "#2ecc71",
    "goal":    "#e74c3c",
    "blocked": "#2c3e50",
    "bonus":   "#00cec9",
    "path":    "#f1c40f"
}

app = ctk.CTk()
app.title("🚑 Ambulance Routing System")
app.geometry("600x950")

canvas = tk.Canvas(app, width=550, height=550)
canvas.pack(pady=10)

def draw_grid():
    canvas.delete("all")
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = COLORS["empty"]
            if (x,y) == start: color = COLORS["start"]
            elif (x,y) in INCIDENTS: color = COLORS["goal"]
            elif (x,y) in BLOCKED_CELLS: color = COLORS["blocked"]
            elif (x,y) in BONUS_CELLS: color = COLORS["bonus"]
            
            canvas.create_rectangle(
                x*CELL, y*CELL, (x+1)*CELL, (y+1)*CELL,
                fill=color, outline="white"
            )
            if (x,y) in INCIDENTS:
                canvas.create_text(
                    x*CELL + CELL//2, y*CELL + CELL//2,
                    text=str(INCIDENTS.index((x,y)) + 1),
                    font=("Arial", 13, "bold"), fill="white"
                )

# animation function to animate in a sequentiel manner
def animate(path, step=0, t=0, trail=None, on_complete=None):
    if trail is None: trail = []
    
    if step >= len(path)-1:
        if on_complete:
            app.after(1000, on_complete) # Wait 1 sec before next animation
        return

    draw_grid()
    for (tx,ty) in trail:
        canvas.create_rectangle(tx*CELL, ty*CELL, (tx+1)*CELL, (ty+1)*CELL, fill="#ffeaa7", outline="white")

    for j in range(step+1):
        x,y = path[j][0]
        canvas.create_rectangle(x*CELL, y*CELL, (x+1)*CELL, (y+1)*CELL, fill=COLORS["path"], outline="white")

    (x1,y1) = path[step][0]
    (x2,y2) = path[step+1][0]
    px, py = x1 + (x2-x1)*t, y1 + (y2-y1)*t
    
    color = "red" if int(t*10)%2==0 else "white"
    canvas.create_text(px*CELL + CELL//2, py*CELL + CELL//2, text="🚑", font=("Arial", 20), fill=color)

    t += 0.1
    if t >= 1:
        animate(path, step+1, 0, trail + [path[step][0]], on_complete)
    else:
        app.after(30, lambda: animate(path, step, t, trail, on_complete))

def run():
    goal_index = goal_var.get()
    hb = bonus_var.get()

    if hb is None:
        sol_both = Astar(start, INCIDENTS)
        with_sol = sol_both[goal_index][0]
        without_sol = sol_both[goal_index][1]

        if not with_sol or not without_sol:
            info.configure(text="Path not found!")
            return

        # finish animation first without bonus then start the bonus animation
        def start_bonus_anim():
            info.configure(text=f"Animating: With Bonus | Cost: {with_sol[1]}")
            animate(with_sol[0])

        info.configure(text=f"Animating:  No Bonus | Cost: {without_sol[1]}")
        animate(without_sol[0], on_complete=start_bonus_anim)

        # for upadting comparison table displayed at the bottom
        text = (
            f"{'':12}{'With Bonus':>14}{'No Bonus':>14}{'Saved':>12}\n"
            f"{'─'*52}\n"
            f"{'Cost':12}{with_sol[1]:>14}{without_sol[1]:>14}{round(abs(with_sol[1]-without_sol[1]),2):>12}\n"
            f"{'Visited':12}{with_sol[2]:>14}{without_sol[2]:>14}{abs(with_sol[2]-without_sol[2]):>12}\n"
        )
        compare_label.configure(text=text)
    else:
        sol = Astar(start, INCIDENTS, forced_bonus=hb)
        result = sol[goal_index][0]
        if result:
            path, cost, visited, used = result
            label = "With Bonus" if used else " No Bonus"
            info.configure(text=f"{label} | Cost: {cost} | Visited: {visited}")
            animate(path)

def reset():
    draw_grid()
    info.configure(text="")
    compare_label.configure(text="")

#UI
goal_var = ctk.IntVar(value=0)
frame = ctk.CTkFrame(app)
frame.pack(pady=5)
for i in range(3):
    ctk.CTkRadioButton(frame, text=f"Goal {i+1}", variable=goal_var, value=i).grid(row=0, column=i, padx=5)

bonus_frame = ctk.CTkFrame(app)
bonus_frame.pack(pady=5)
bonus_var = ctk.StringVar(value="True")

# Functional override for getting boolean/None from string
_orig_get = bonus_var.get
def _bonus_get():
    v = _orig_get()
    return True if v == "True" else False if v == "False" else None
bonus_var.get = _bonus_get

ctk.CTkRadioButton(bonus_frame, text="With Bonus", variable=bonus_var, value="True").grid(row=0, column=0, padx=5)
ctk.CTkRadioButton(bonus_frame, text="No Bonus", variable=bonus_var, value="False").grid(row=0, column=1, padx=5)
ctk.CTkRadioButton(bonus_frame, text="Compare", variable=bonus_var, value="None").grid(row=0, column=2, padx=5)

ctk.CTkButton(app, text="Start ", command=run).pack(pady=5)
ctk.CTkButton(app, text="Reset ", command=reset).pack(pady=5)
info = ctk.CTkLabel(app, text="")
info.pack()

compare_box = ctk.CTkFrame(app)
compare_box.pack(padx=16, pady=4, fill="x")
compare_label = ctk.CTkLabel(compare_box, text="", font=("Courier", 11), justify="left")
compare_label.pack(pady=10)

draw_grid()
app.mainloop()