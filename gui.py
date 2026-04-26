import customtkinter as ctk

# ================== SETTINGS==================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ================== GUI ==================
CELL = 50

COLORS = {
    "empty": "#2c3e50",
    "start": "#20ec75",
    "goal": "#e74c3c",
    "blocked": "#2B2727",
    "bonus": "#3B5F5F",
    "path": "#8a8683"
}

app = ctk.CTk()
app.title("🚑 Ambulance Routing System")
app.geometry("600x720")

canvas = ctk.CTkCanvas(app, width=550, height=550)
canvas.pack(pady=10)

def draw_grid():
    canvas.delete("all")
    for x in range(GRID_SIZE+1):
        for y in range(GRID_SIZE+1):

            color = COLORS["empty"]

            if (x,y) == start:
                color = COLORS["start"]
            elif (x,y) in INCIDENTS:
                color = COLORS["goal"]
            elif (x,y) in BLOCKED_CELLS:
                color = COLORS["blocked"]
            elif (x,y) in BONUS_CELLS:
                color = COLORS["bonus"]

            canvas.create_rectangle(
                x*CELL, y*CELL,
                (x+1)*CELL, (y+1)*CELL,
                fill=color, outline="white"
            )

stop_animation = False
def animate(path, step=0, t=0, trail=None):
    global stop_animation
    
    if stop_animation:
        stop_animation = False
        return
    
    if trail is None:
        trail = []

    if step >= len(path)-1:
        return

    draw_grid()

    # trail
    for (tx,ty) in trail:
        canvas.create_rectangle(
            tx*CELL, ty*CELL,
            (tx+1)*CELL, (ty+1)*CELL,
            fill="#ffeaa7", outline="white"
        )

    # path
    for j in range(step+1):
        x,y = path[j][0]
        canvas.create_rectangle(
            x*CELL, y*CELL,
            (x+1)*CELL, (y+1)*CELL,
            fill=COLORS["path"], outline="white"
        )

    (x1,y1) = path[step][0]
    (x2,y2) = path[step+1][0]

    px = x1 + (x2-x1)*t
    py = y1 + (y2-y1)*t

    color = "red" if int(t*10)%2==0 else "white"

    canvas.create_text(
        px*CELL + CELL//2,
        py*CELL + CELL//2,
        text="🚑",
        font=("Arial", 20),
        fill=color
    )

    t += 0.05

    if t >= 1:
        animate(path, step+1, 0, trail + [path[step][0]])
    else:
        app.after(30, lambda: animate(path, step, t, trail))

def run():
    global stop_animation
    stop_animation = False
    
    goal_index = goal_var.get()

    sol = Astar(start, INCIDENTS)

    path, cost, visited, bonus = sol[goal_index][0]

    info_label.configure(
        text=f"Cost: {cost} | Visited: {visited} | Bonus: {bonus}"
    )

    animate(path)

def reset():
    global stop_animation
    stop_animation = True
    
    draw_grid()
    info_label.configure(text="")

# ================== CONTROLS ==================
goal_var = ctk.IntVar(value=0)

frame = ctk.CTkFrame(app)
frame.pack(pady=5)

ctk.CTkRadioButton(frame, text="Goal 1", variable=goal_var, value=0).grid(row=0,column=0,padx=5)
ctk.CTkRadioButton(frame, text="Goal 2", variable=goal_var, value=1).grid(row=0,column=1,padx=5)
ctk.CTkRadioButton(frame, text="Goal 3", variable=goal_var, value=2).grid(row=0,column=2,padx=5)

ctk.CTkButton(app, text="Start 🚀", command=run, fg_color="green", hover_color="darkgreen").pack(pady=5)
ctk.CTkButton(app, text="Reset 🔄", command=reset, fg_color="gray", hover_color="darkgray").pack(pady=5)
ctk.CTkButton(app, text="Exit❌", command=app.destroy, fg_color="red", hover_color="darkred").pack(pady=5)

info_label = ctk.CTkLabel(app, text="")
info_label.pack(pady=10)

draw_grid()
app.mainloop()