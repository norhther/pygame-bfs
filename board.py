from enum import Enum, auto
import random
from yachalk import chalk
from dataclasses import dataclass


class BoxType(Enum):
    SPACE = auto()
    WALL = auto()
    END = auto()
    VISITED = auto()
    ORIGIN = auto()

    def __str__(self):
        if self.name == "SPACE":
            return "."
        elif self.name == "WALL":
            return "*"
        elif self.name == "VISITED":
            return "V"
        elif self.name == "ORIGIN":
            return "O"
        else:
            return "E"


@dataclass
class Box():
    x: int
    y: int
    Type: BoxType


def chalk_print(val):
    if val == BoxType.WALL:
        print(chalk.red(val), end="")
    elif val == BoxType.ORIGIN:
        print(chalk.blue(val), end="")
    elif val == BoxType.VISITED:
        print(chalk.green(val), end="")
    else:
        print(val, end="")


class Board():
    def __init__(self, w: int, h: int, s_x=0, s_y=0):
        self.w: int = w
        self.h: int = h
        self.matrix: list[list[[[int, int], BoxType]]] = \
            [[[[x, y], BoxType.SPACE] for y in range(w)] for x in range(h)]
        self.start_x = s_x
        self.start_y = s_y

    def _create_random_object(self, obj=BoxType.WALL):
        x = random.randint(0, self.h - 1)
        y = random.randint(0, self.w - 1)
        self.matrix[x][y] = [[x, y], obj]

        if obj == BoxType.ORIGIN:
            self.start_x = x
            self.start_y = y

    def _random_start(self, n=15):
        for i in range(n):
            self._create_random_object()

        self._create_random_object(obj=BoxType.END)
        self._create_random_object(obj=BoxType.ORIGIN)

    def __str__(self):
        res: str = ""
        for row in self.matrix:
            for val in row:
                chalk_print(val[1])
            print()
        return res

    def _isGood(self, x, y):
        return x >= 0 and y >= 0 and \
            x < self.h and y < self.w and \
            (self.matrix[x][y][1] == BoxType.SPACE
                or self.matrix[x][y][1] == BoxType.END)

    def bfs(self, rand=True):
        """
            BFS implementation.
            Pre: (init_x,init_y) can NOT be in the same location as BoxType.End
        """
        if rand:
            self._random_start()

        offsets_x = [1, 0, 0, -1]
        offsets_y = [0, 1, -1, 0]
        q = [self.matrix[self.start_x][self.start_y]]
        while q:
            current_BoxType = q.pop(0)
            current_x = current_BoxType[0][0]
            current_y = current_BoxType[0][1]
            print(self)
            for o_x, o_y in zip(offsets_x, offsets_y):
                if self._isGood(o_x + current_x, o_y + current_y) and \
                    self.matrix[o_x + current_x][o_y + current_y][1] != BoxType.VISITED:
                    q.append(self.matrix[o_x + current_x][o_y + current_y])
                    if self.matrix[o_x + current_x][o_y + current_y][1] == BoxType.END:
                        print("END!")
                        print(self)
                        return
                    self.matrix[o_x + current_x][o_y + current_y][1] = BoxType.VISITED

        print("NO PATH FOUND!")
        print(self)
