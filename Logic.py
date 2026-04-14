

GRID_SIZE = 10
start = (0, 0)

BLOCKED_CELLS = [
    (3, 0), (6, 0), (8, 0), (0, 2), (1, 2), (7, 2), (8, 2), (0, 3), (6, 3), (0, 4), (1, 4), (2, 4), (4, 4), (4, 5),
    (5, 5), (7, 5), (9, 5), (1, 6), (5, 6), (9, 6), (1, 7), (5, 7), (6, 7), (7, 7), (9, 7), (4, 8), (5, 8), (9, 8),
    (0, 9), (1, 9), (2, 9), (7, 9), (8, 9), (9, 9)
    # Add all 20+ dark blue cells from your image here
]

BONUS_CELLS = [
    (5, 4), (6, 4), (7, 4), (8, 4), (2, 6),  # The cyan cells
    (3, 6), (2, 7), (0, 8), (1, 8), (2, 8)
]

INCIDENTS = [(4, 9), (6, 6), (0, 7)]  # The 3 red squares[span_4](end_span)


def get_cell_cost(current_cell):
    if current_cell in BLOCKED_CELLS:
        return float('inf')  # Infinity cost (cannot pass)[span_5](end_span)

    if current_cell in BONUS_CELLS:
        return 0.5

    return 1.0


def Astar(start, goal1, goal2, goal3):
    visited = []
    queue = [[(start)]]
    while queue:
        queue.sort
        path = queue.pop(0)
        cell = path[-1][0]
        if cell in visited or cell in BLOCKED_CELLS:
            continue
        visited.append(cell)
        if cell == goal1 or goal2 or goal3:
            return path
        else:

            possible_path = [((path[0][0][0] + 1, path[0][0][0]), path[0][1]),
                             ((path[0][0][0], path[0][0][0] + 1), path[0][1])]
            for (cell2, cost) in possible_path:
                new_path = path.copy()
                new_path.append((cell2), cost)
                queue.append(new_path)
                print(queue)
