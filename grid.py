GRID_SIZE = 10
start = (0, 0)

BLOCKED_CELLS = [
    (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (0,1),
    (8, 1), (9, 1), (0, 2), (1, 2), (3, 2), (4, 2), (9, 2), (0, 3), (4, 3),
    (5, 3), (6, 3), (7, 3), (9, 3), (7, 4), (0, 5), (1, 5), (3, 6), (4, 6),
    (5, 6), (3,7), (5, 7), (9, 7), (3, 8), (7, 8), (8, 8), (9,8), (9,9)
    # Add all 20+ dark blue cells from your image here
]

BONUS_CELLS = [
    (8,3), (4, 4), (5, 4), (6, 4), (8,4), (6, 5), # The cyan cells
    (7, 5), (8, 5), (6, 6), (6, 7)
]

INCIDENTS = [
    (8, 2), (4,7), (8, 9)]  # The 3 red squares[span_4](end_span)


def get_cell_cost(current_cell,has_bounes):
    if current_cell in BLOCKED_CELLS:
        return float('inf')  # Infinity cost (cannot pass)[span_5](end_span)

    if current_cell in BONUS_CELLS:
        if has_bounes:
            return 0.5
        else:
            return 1.0
    return 1.0