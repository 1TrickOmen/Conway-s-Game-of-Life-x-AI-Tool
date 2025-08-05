# api/game_of_life.py
import numpy as np
from typing import Dict

def word_to_bitmask(word: str, width: int = 60, height: int = 40) -> np.ndarray:
    """
    Convert a word to a binary pattern in the middle of a 60x40 grid.
    Each character -> 8 bits of ASCII -> placed horizontally.
    """
    grid = np.zeros((height, width), dtype=np.uint8)
    binary_str = ''.join(f"{ord(c):08b}" for c in word)

    # Truncate if too long
    if len(binary_str) > width:
        binary_str = binary_str[:width]

    # Center the pattern
    start_x = (width - len(binary_str)) // 2
    start_y = height // 2  # middle row

    for i, bit in enumerate(binary_str):
        grid[start_y, start_x + i] = 1 if bit == '1' else 0

    return grid

def step(grid: np.ndarray) -> np.ndarray:
    """Apply one step of Conway's Game of Life rules."""
    neighbors = (
        np.roll(np.roll(grid, 1, 0), 1, 1) +  # top-left
        np.roll(np.roll(grid, 1, 0), 0, 1) +  # top
        np.roll(np.roll(grid, 1, 0), -1, 1) +  # top-right
        np.roll(np.roll(grid, 0, 0), 1, 1) +  # left
        np.roll(np.roll(grid, 0, 0), -1, 1) +  # right
        np.roll(np.roll(grid, -1, 0), 1, 1) +  # bottom-left
        np.roll(np.roll(grid, -1, 0), 0, 1) +  # bottom
        np.roll(np.roll(grid, -1, 0), -1, 1)   # bottom-right
    )
    return (neighbors == 3) | (grid & (neighbors == 2))

def count_total_spawned(initial: np.ndarray) -> int:
    """Simulate again to count total cells ever alive."""
    grid = initial.copy()
    total = np.sum(initial)
    prev_states = {grid.tobytes()}

    for _ in range(1000):
        next_grid = step(grid)
        live = np.sum(next_grid)
        total += live

        if live == 0:
            break  # extinct
        elif next_grid.tobytes() in prev_states:
            break  # cycle

        prev_states.add(next_grid.tobytes())
        grid = next_grid

    return total

def run_until_stable(word: str, width: int = 60, height: int = 40) -> Dict:
    """Run CGoL from word until stable state."""
    grid = word_to_bitmask(word.lower(), width, height)
    initial = grid.copy()
    total_spawned = np.sum(initial)
    prev_states = [grid.tobytes()]
    generation = 0

    while generation < 1000:
        grid = step(grid)
        generation += 1
        live_count = np.sum(grid)

        current_state = grid.tobytes()

        # Extinction
        if live_count == 0:
            return {
                "generations": generation,
                "score": total_spawned,
                "final_state": "extinct"
            }

        # Cycle detection (last 10 states)
        if current_state in prev_states:
            idx = prev_states.index(current_state)
            cycle_len = len(prev_states) - idx
            if cycle_len < 10:
                return {
                    "generations": generation,
                    "score": count_total_spawned(initial),
                    "final_state": f"oscillator_period_{cycle_len}"
                }

        prev_states.append(current_state)
        if len(prev_states) > 10:
            prev_states.pop(0)

        total_spawned += live_count

    return {
        "generations": 1000,
        "score": count_total_spawned(initial),
        "final_state": "max_generations_reached"
    }