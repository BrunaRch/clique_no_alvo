import math
import random
import time
import pygame
pygame.init()

WIDTH,HEIGHT = 700, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clique no alvo")

INCREMENTO_DO_ALVO = 400
ALVO_EVENT = pygame.USEREVENT

PADDING_DO_ALVO = 30

BG_COLOR = (1, 30, 45)

class Alvo:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = (255, 0, 0)
    SECOND_COLOR = (255, 255, 255)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
    
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR,(self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR,(self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR,(self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR,(self.x, self.y), self.size * 0.4)

def draw(win, alvos):
    win.fill(BG_COLOR)

    for alvo in alvos:
        alvo.draw(win)

    pygame.display.update()

        
# loop principal
def main():
    run = True
    alvos = []

    pygame.time.set_timer(ALVO_EVENT, INCREMENTO_DO_ALVO)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == ALVO_EVENT:
                x = random.randint(PADDING_DO_ALVO, WIDTH - PADDING_DO_ALVO)
                y = random.randint(PADDING_DO_ALVO, HEIGHT - PADDING_DO_ALVO)
                alvo = Alvo(x, y)
                alvos.append(alvo)
        
        for alvo in alvos:
            alvo.update()

        draw(WIN, alvos)


if __name__ == "__main__":
    main()

# classes dos alvos

