from board import Board
from screen import Screen

if __name__ == "__main__":
    """
    b = Board(10, 10, random_start=True)
    b.solve_with_steps()
    """
    w = 1024
    h = 1024
    block_size = 16
    random_objects = 1500

    board = Board(w//block_size, h//block_size, random_start=True, random_objects=random_objects)
    screen = Screen(board, w = w, h = h, block_size=block_size)
    screen.loop(bfs=False)
