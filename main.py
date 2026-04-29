from Logic import *
from GUI import *

sol = Astar(grid.start, grid.INCIDENTS)
for goal_index, goal_solutions in enumerate(sol):
    print(f"Solutions for Goal {grid.INCIDENTS[goal_index]}:")
    for solution in goal_solutions:
        path, total_cost, visited_count, has_bounes = solution
        print(f"Has Bounes: {has_bounes}",f"Path: {[cell for cell, _ in path]}", f"Total Cost: {total_cost}", f"Visited Cells: {visited_count}", sep="\n")
    print("\n")

print("summary:")
print("="*80)
print(f"{'Goal':>10} {'Has Bounes':>15} {'Total Cost':>15} {'Visited':>20} {'Path Length':>15}")
for goal_index, goal_solutions in enumerate(sol):
    goal = grid.INCIDENTS[goal_index]
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

app.mainloop()