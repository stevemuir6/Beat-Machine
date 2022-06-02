# My Beat Maker!
import pygame
from pygame import mixer
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
light_gray = (170, 170, 170)
purple = (160, 32, 240)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
WIDTH = 1400
HEIGHT = 800
active_length = 8
active_beat = 1

# load in sounds
hi_hat = mixer.Sound('sounds\\hi hat.WAV')
snare = mixer.Sound('sounds\\snare.WAV')
kick = mixer.Sound('sounds\\kick.WAV')
crash = mixer.Sound('sounds\\crash.wav')
clap = mixer.Sound('sounds\\clap.wav')
tom = mixer.Sound('sounds\\tom.WAV')

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Dope Beats')
label_font = pygame.font.Font("Bitter-Regular.ttf", 30)
medium_font = pygame.font.Font("Bitter-Regular.ttf", 23)
beat_changed = True
timer = pygame.time.Clock()
fps = 60
beats = 8
bpm = 240
instruments = 6
playing = True
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
pygame.mixer.set_num_channels(instruments * 3)
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
typing = False
index = 100


def draw_grid(clicks, beat, actives):
    boxes = []
    left_box = pygame.draw.rect(screen, purple, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, purple, [0, HEIGHT - 200, WIDTH, 200], 5)
    for i in range(instruments):
        pygame.draw.line(screen, purple, (0, i * 100), (200, i * 100), 3)
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render('Kick', True, colors[actives[2]])
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30, 430))
    floor_text = label_font.render('Floor Tom', True, colors[actives[5]])
    screen.blit(floor_text, (30, 530))
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5,
                                     ((WIDTH - 200) // beats) - 10, 90], 0, 3)
            pygame.draw.rect(screen, gold,
                             [i * ((WIDTH - 200) // beats) + 200, j * 100,
                              ((WIDTH - 200) // beats), 100], 5, 5)
            pygame.draw.rect(screen, black,
                             [i * ((WIDTH - 200) // beats) + 200, j * 100,
                                             ((WIDTH - 200) // beats), 100], 2, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats),
                                                 instruments * 100], 5, 3)
    return boxes


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('SAVE MENU:  Enter a Name for Current Beat', True, white)
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, purple, [WIDTH - 200, HEIGHT - 100, 100, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 188, HEIGHT - 73))
    saving_btn = pygame.draw.rect(screen, purple, [WIDTH // 2 - 200, HEIGHT * 0.75, 400, 100], 0, 5)
    saving_txt = label_font.render('Save Beat', True, white)
    screen.blit(saving_txt, (WIDTH // 2 - 70, HEIGHT * 0.75 + 30))
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, purple, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, beat_name, entry_rect


def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('LOAD MENU:  Select a Beat to Load', True, white)
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, purple, [WIDTH - 200, HEIGHT - 100, 100, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 188, HEIGHT - 73))
    loading_btn = pygame.draw.rect(screen, purple, [WIDTH // 2 - 200, HEIGHT * 0.87, 400, 100], 0, 5)
    loading_txt = label_font.render('Load Beat', True, white)
    screen.blit(loading_txt, (WIDTH // 2 - 70, HEIGHT * 0.87 + 30))
    delete_btn = pygame.draw.rect(screen, purple, [(WIDTH // 2) - 500, HEIGHT * 0.87, 200, 100], 0, 5)
    delete_txt = label_font.render('Delete Beat', True, white)
    screen.blit(delete_txt, ((WIDTH // 2) - 485, HEIGHT * 0.87 + 30))
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, purple, [190, 100 + index*50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beats_index_end  = saved_beats[beat].index(', bpm')
            loaded_beats = int(saved_beats[beat][name_index_end + 8:beats_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm = int(saved_beats[beat][beats_index_end + 6:bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rect = pygame.draw.rect(screen, purple, [190, 90, 1000, 600], 5, 5)
    return exit_btn, loading_btn, entry_rect, delete_btn, loaded_info


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, purple, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, gold)
    else:
        play_text2 = medium_font.render('Paused', True, gold)
    screen.blit(play_text2, (70, HEIGHT - 100))
    # bpm buttons
    bpm_rect = pygame.draw.rect(screen, purple, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, gold)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, purple, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, purple, [510, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render('+5', True, white)
    screen.blit(add_text, (520, HEIGHT - 140))
    sub_text = medium_font.render('-5', True, white)
    screen.blit(sub_text, (520, HEIGHT - 90))
    # beats per loop buttons
    beats_rect = pygame.draw.rect(screen, purple, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (626, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{beats}', True, gold)
    screen.blit(bpm_text2, (690, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, purple, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, purple, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, white)
    screen.blit(add_text2, (820, HEIGHT - 140))
    sub_text2 = medium_font.render('-1', True, white)
    screen.blit(sub_text2, (820, HEIGHT - 90))
    # clear board
    clear_button = pygame.draw.rect(screen, purple, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render("Clear Board", True, white)
    screen.blit(clear_text, (1167, HEIGHT - 120))
    # save and load buttons
    save_button = pygame.draw.rect(screen, purple, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = label_font.render("Save Beat", True, white)
    screen.blit(save_text, (930, HEIGHT - 145))
    load_button = pygame.draw.rect(screen, purple, [900, HEIGHT - 100, 200, 48], 0, 5)
    load_text = label_font.render("Load Beat", True, white)
    screen.blit(load_text, (930, HEIGHT - 95))
    # instrument rectangles  * the ability to turn instruments on and off
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)
    if beat_changed:
        play_notes()
        beat_changed = False
    if save_menu:
        exit_button, saving_button, beat_name, entry_rect = draw_save_menu(beat_name, typing)
    elif load_menu:
        exit_button, loading_button, entry_rect, delete_button, loaded_information = draw_load_menu(index)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos) and playing:
                playing = False
            elif play_pause.collidepoint(event.pos) and not playing:
                playing = True
                active_beat = 0
                active_length = 0
            if beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            if bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            if clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
            if save_button.collidepoint(event.pos):
                save_menu = True
            if load_button.collidepoint(event.pos):
                load_menu = True
                playing = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                typing = False
                beat_name = ''
            if entry_rect.collidepoint(event.pos):
                if save_menu:
                    if typing:
                        typing = False
                    else:
                        typing = True
                if load_menu:
                    index = (event.pos[1] - 100) // 50
            if save_menu:
                if saving_button.collidepoint(event.pos):
                    file = open('saved_beats.txt', 'w')
                    saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    load_menu = False
                    playing = True
                    typing = False
                    beat_name = ''
            if load_menu:
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= len(saved_beats):
                        beats = loaded_information[0]
                        bpm = loaded_information[1]
                        clicked = loaded_information[2]
                        index = 100
                        save_menu = False
                        load_menu = False
                        playing = True
                        typing = False
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0:
                beat_name = beat_name[:-1]

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

file = open('saved_beats.txt', 'w')
for i in range(len(saved_beats)):
    file.write(str(saved_beats[i]))
file.close()
pygame.quit()
