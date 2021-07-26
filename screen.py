import pygame
from board import BoxType

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (238, 130, 238)


class Screen:
    def __init__(self, board, w=512, h=512, fps=120, caption="screen", block_size=16):
        self.w = w
        self.h = h
        self.fps = fps
        self.caption = caption
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(caption)
        self.clock = clock = pygame.time.Clock()
        self.block_size = block_size
        self.board = board

    def drawGrid(self):
        for x in range(0, self.w, self.block_size):
            for y in range(0, self.h, self.block_size):

                box_type = self.board.get(y // self.block_size, x // self.block_size)
                rect = pygame.Rect(x, y, self.block_size, self.block_size)

                if box_type == BoxType.SPACE:
                    pygame.draw.rect(self.screen, WHITE, rect)
                elif box_type == BoxType.VISITED:
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif box_type == BoxType.WALL:
                    pygame.draw.rect(self.screen, RED, rect)
                elif box_type == BoxType.END:
                    pygame.draw.rect(self.screen, VIOLET, rect)
                elif box_type == BoxType.ORIGIN:

                    pygame.draw.rect(self.screen, BLACK, rect)

    def loop(self, bfs=False):
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BLACK)
            if self.board.end:
                self.board.random_start(1500)
                pygame.time.wait(200)
            self.drawGrid()


            self.board.oneStep(bfs)

            pygame.display.flip()

    pygame.quit()
