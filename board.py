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

"""
@dataclass
class Box():
    x: int
    y: int
    Type: BoxType
"""

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
    def __init__(self, w: int, h: int, s_x=0, s_y=0, random_start = False, random_objects = 5):
        self.w: int = w
        self.h: int = h
        self.matrix: list[list[[[int, int], BoxType]]] = \
            [[[[x, y], BoxType.SPACE] for y in range(w)] for x in range(h)]

        self.start_x = s_x
        self.start_y = s_y
        if random_start:
            self._random_start(random_objects)
        self.todo    = []
        self.start   = True
        self.end     = False
        self.found   = False

    def _create_random_object(self, obj=BoxType.WALL):
        x = random.randint(0, self.h - 1)
        y = random.randint(0, self.w - 1)
        self.matrix[x][y] = [[x, y], obj]

        if obj == BoxType.ORIGIN:
            self.start_x = x
            self.start_y = y
        return x,y

    def _random_start(self, n=5):
        self.todo    = []
        self.start   = True
        self.end     = False
        self.found   = False
        for i in range(n):
            self._create_random_object()

        end_x, end_y       = self._create_random_object(obj=BoxType.END)
        origin_x, origin_y = self._create_random_object(obj=BoxType.ORIGIN)
        # Avoid overlappin
        while origin_x == end_x and end_y == origin_y:
            origin_x, origin_y = self._create_random_object(obj=BoxType.ORIGIN)

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


    def oneStep(self):
        offsets_x = [1, 0, 0, -1]
        offsets_y = [0, 1, -1, 0]
        if self.start:
            self.start = False
            self.todo  = [self.matrix[self.start_x][self.start_y]]
        
        if not self.todo:
            self.end = True

        else:
            current_BoxType = self.todo.pop(0)
            current_x = current_BoxType[0][0]
            current_y = current_BoxType[0][1]
            for o_x, o_y in zip(offsets_x, offsets_y):
                if self._isGood(o_x + current_x, o_y + current_y) and \
                    self.matrix[o_x + current_x][o_y + current_y][1] != BoxType.VISITED:
                    self.todo.append(self.matrix[o_x + current_x][o_y + current_y])
                    if self.matrix[o_x + current_x][o_y + current_y][1] == BoxType.END:
                        self.end = self.found = True
                        return
                    self.matrix[o_x + current_x][o_y + current_y][1] = BoxType.VISITED

    def solve_with_steps(self, visualize = True):
        while not self.end and not self.found:
            if visualize:
                print(self)
            self.oneStep()

    def bfs(self, rand=True):
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
