from board import Board


if __name__ == "__main__":
    b = Board(10,10,random_start = True)
    b.solve_with_steps()
