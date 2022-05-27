# My Beat Maker!
import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
purple = (160, 32, 240)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Dope Beats')
label_font = pygame.font.Font("Bitter-Regular.ttf", 30)

fps = 60
timer = pygame.time.Clock()



def draw_grid():
    left_box = pygame.draw.rect(screen, purple, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, purple, [0,HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat',True, white)
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render('Kick', True, white)
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 430))
    floor_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_text, (30, 530))
    for i in range(6):
        pygame.draw.line(screen, purple, (0, (i * 100) + 100), (200, (i * 100) + 100), 5)



run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()

