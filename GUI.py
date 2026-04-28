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
app.geometry("600x1050")

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

def animate(path, step=0, t=0, trail=None, on_complete=None):
    if trail is None: trail = []
    if step >= len(path)-1:
        if on_complete:
            app.after(1000, on_complete)
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
    sol = Astar(start, INCIDENTS)
    goal_sol = sol[goal_index]

    if len(goal_sol) < 2:
        info.configure(text="Path not found!")
        return

    with_sol    = goal_sol[0]  # has_bonus=True
    without_sol = goal_sol[1]  # has_bonus=False

    if hb is None:
        def start_bonus_anim():
            info.configure(text=f"▶ With Bonus | Cost: {with_sol[1]}")
            animate(with_sol[0])
        info.configure(text=f"▶ No Bonus | Cost: {without_sol[1]}")
        animate(without_sol[0], on_complete=start_bonus_anim)
        update_compare_table(with_sol, without_sol)
    else:
        # ✅ THE FIX: pick correct solution based on user choice
        result = with_sol if hb else without_sol
        path, cost, visited, used = result
        label = "With Bonus" if hb else "No Bonus"
        info.configure(text=f"▶ {label} | Cost: {cost} | Visited: {visited}")
        animate(path)

def update_compare_table(with_sol, without_sol):
    cost_saved    = round(abs(with_sol[1] - without_sol[1]), 2)
    visited_saved = abs(with_sol[2] - without_sol[2])
    rows = [
        ("",          "With Bonus",   "No Bonus",     "Saved"),
        ("Cost",      with_sol[1],    without_sol[1], cost_saved),
        ("Visited",   with_sol[2],    without_sol[2], visited_saved),
    ]
    for widget in compare_inner.winfo_children():
        widget.destroy()

    colors = ["#1e272e", "#2d3436"]
    headers = ["", "With Bonus", "No Bonus", "Saved"]
    col_colors = ["#636e72", "#00cec9", "#e17055", "#2ecc71"]

    for col, (h, c) in enumerate(zip(headers, col_colors)):
        ctk.CTkLabel(compare_inner, text=h, font=("Arial", 11, "bold"),
                     text_color=c, width=100, anchor="center").grid(row=0, column=col, padx=4, pady=4)

    data_rows = [
        ("Cost",    with_sol[1],    without_sol[1], cost_saved),
        ("Visited", with_sol[2],    without_sol[2], visited_saved),
    ]
    for r, (label, w, wo, saved) in enumerate(data_rows):
        bg = colors[r % 2]
        ctk.CTkLabel(compare_inner, text=label, font=("Arial", 11, "bold"),
                     text_color="#b2bec3", width=100, anchor="center",
                     fg_color=bg, corner_radius=4).grid(row=r+1, column=0, padx=4, pady=3)
        ctk.CTkLabel(compare_inner, text=str(w), font=("Arial", 11),
                     text_color="#00cec9", width=100, anchor="center",
                     fg_color=bg, corner_radius=4).grid(row=r+1, column=1, padx=4, pady=3)
        ctk.CTkLabel(compare_inner, text=str(wo), font=("Arial", 11),
                     text_color="#e17055", width=100, anchor="center",
                     fg_color=bg, corner_radius=4).grid(row=r+1, column=2, padx=4, pady=3)
        ctk.CTkLabel(compare_inner, text=str(saved), font=("Arial", 11, "bold"),
                     text_color="#2ecc71", width=100, anchor="center",
                     fg_color=bg, corner_radius=4).grid(row=r+1, column=3, padx=4, pady=3)

def compare():
    bonus_var._orig_set("None")
    run()

def reset():
    draw_grid()
    info.configure(text="")
    for widget in compare_inner.winfo_children():
        widget.destroy()

def kill():
    app.destroy()

# ── UI ───
goal_var = ctk.IntVar(value=0)
frame = ctk.CTkFrame(app)
frame.pack(pady=5)
for i in range(3):
    ctk.CTkRadioButton(frame, text=f"Goal {i+1}", variable=goal_var, value=i).grid(row=0, column=i, padx=5)

bonus_frame = ctk.CTkFrame(app)
bonus_frame.pack(pady=5)
bonus_var = ctk.StringVar(value="True")

_orig_get = bonus_var.get
_orig_set = bonus_var.set
def _bonus_get():
    v = _orig_get()
    return True if v == "True" else False if v == "False" else None
bonus_var.get = _bonus_get
bonus_var._orig_set = _orig_set

ctk.CTkRadioButton(bonus_frame, text="With Bonus", variable=bonus_var, value="True").grid(row=0, column=0, padx=5)
ctk.CTkRadioButton(bonus_frame, text="No Bonus",   variable=bonus_var, value="False").grid(row=0, column=1, padx=5)

btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=5)
ctk.CTkButton(btn_frame, text="▶  Start",   command=run,     width=120).grid(row=0, column=0, padx=6)
ctk.CTkButton(btn_frame, text="⟳  Reset",   command=reset,   width=120).grid(row=0, column=1, padx=6)
ctk.CTkButton(btn_frame, text="⇄  Compare", command=compare, width=120).grid(row=0, column=2, padx=6)
ctk.CTkButton(btn_frame, text="✕  Quit",    command=kill,    width=120,
              fg_color="#c0392b", hover_color="#96281b").grid(row=0, column=3, padx=6)

info = ctk.CTkLabel(app, text="", font=("Arial", 12))
info.pack(pady=4)

compare_box = ctk.CTkFrame(app)
compare_box.pack(padx=16, pady=4, fill="x")
compare_inner = ctk.CTkFrame(compare_box, fg_color="transparent")
compare_inner.pack(pady=10)

draw_grid()
app.mainloop()