import random
from collections import deque

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


def find_ai_direction(snake, other_snakes, food, grid_width, grid_height, current_direction):
    if food is None:
        return current_direction

    start = snake[0]

    obstacles = set()

    for other_snake in other_snakes:
        obstacles.update(other_snake)

    obstacles.update(snake[:-1])
    obstacles.discard(start)

    queue = deque([(start, [])])
    visited = {start}

    while queue:
        position, path = queue.popleft()

        if position == food and path:
            return path[0]

        for direction in DIRECTIONS:
            if direction == (-current_direction[0], -current_direction[1]):
                continue

            next_position = (
                position[0] + direction[0],
                position[1] + direction[1]
            )

            if (
                next_position[0] < 0
                or next_position[0] >= grid_width
                or next_position[1] < 0
                or next_position[1] >= grid_height
            ):
                continue

            if next_position in obstacles or next_position in visited:
                continue

            visited.add(next_position)

            queue.append((next_position, path + [direction]))

    safe_moves = []

    for direction in DIRECTIONS:
        if direction == (-current_direction[0], -current_direction[1]):
            continue

        next_position = (
            start[0] + direction[0],
            start[1] + direction[1]
        )

        if (
            0 <= next_position[0] < grid_width
            and 0 <= next_position[1] < grid_height
            and next_position not in obstacles
        ):
            safe_moves.append(direction)

    return random.choice(safe_moves) if safe_moves else current_direction
              
