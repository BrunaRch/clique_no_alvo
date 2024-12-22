import math
import random
import time
import pygame
pygame.init()
    
WIDTH, HEIGHT = 700, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clique no alvo")

# Definição de constantes
INCREMENTO_DO_ALVO = 400
ALVO_EVENT = pygame.USEREVENT

PADDING_DO_ALVO = 30

BG_COLOR = (40, 40, 90)
VIDAS = 3
TOP_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 18)


class Alvo:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = (220, 30, 10)
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

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 +(y - self.y)**2)
        return dis <= self.size

# limpa tela  
def draw(win, alvos):
    win.fill(BG_COLOR)

    for alvo in alvos:
        alvo.draw(win)


def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

# 1- Dados na tela enquanto o jogo roda
def draw_top(win, elapsed_time, alvo_clicado, perdas):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_HEIGHT))
    time_label = LABEL_FONT.render(f"Tempo: {format_time(elapsed_time)}", 1, "black")

    speed = round(alvo_clicado / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Velocidade: {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Pontos: {alvo_clicado}", 1, "black")

    vidas_label = LABEL_FONT.render(f"Vidas: {VIDAS - perdas}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (400, 5))
    win.blit(vidas_label, (580, 5))

# 2 - Dados no meio da tela quando termina o jogo
def end_screen(win, elapsed_time, alvo_clicado, clicks):
    win.fill(BG_COLOR)

    # Textos
    time_label = LABEL_FONT.render(f"Tempo: {format_time(elapsed_time)}", 1, "white")
    speed = round(alvo_clicado / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Velocidade: {speed} alvos/segun.", 1, "white")
    hits_label = LABEL_FONT.render(f"Pontos: {alvo_clicado}", 1, "black")
    end_message = LABEL_FONT.render("Pressione qualquer tecla para sair", 1, "white")

    # Ajusta a posição dos textos na tela
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 150))
    win.blit(hits_label, (get_middle(hits_label), 200))
    win.blit(end_message, (get_middle(end_message), 350))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                exit()

def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/ 2

# loop principal
def main():
    run = True
    alvos = []
    clock = pygame.time.Clock()

    alvo_clicado = 0
    clicks = 0
    perdas = 0
    start_time = time.time()

    pygame.time.set_timer(ALVO_EVENT, INCREMENTO_DO_ALVO)

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == ALVO_EVENT:
                x = random.randint(PADDING_DO_ALVO + TOP_HEIGHT, HEIGHT - PADDING_DO_ALVO)
                y = random.randint(PADDING_DO_ALVO, HEIGHT - PADDING_DO_ALVO)
                alvo = Alvo(x, y)
                alvos.append(alvo)

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicks += 1
        
        for alvo in alvos:
            alvo.update()

            if alvo.size <= 0:
                alvos.remove(alvo)
                perdas += 1

            if clicks and alvo.collide(*mouse_pos):
                alvos.remove(alvo)
                alvo_clicado += 1

        if perdas >= VIDAS:
            end_screen(WIN, elapsed_time, alvo_clicado, clicks)
            run = False

        draw(WIN, alvos)
        draw_top(WIN, elapsed_time, alvo_clicado, perdas)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
