import pygame
from student import Student
import random

import pathlib
path = pathlib.Path(__file__).parent.resolve()

pygame.init()
icon = pygame.image.load(f"{path}/assets/kelgenbayev/t1.png")
pygame.display.set_icon(icon)


def main(i, j, a, b, title):
    # sound settings
    f = f"{path}/assets/mp3/"
    cool_songs = [f"{f}c418_lullaby.mp3", f"{f}c418_sweden.mp3", f"{f}c418_wet.mp3",
                f"{f}evil_morty.mp3", f"{f}rick_roll.mp3", f"{f}undertale_shop.mp3", f"{f}jojo.mp3"]
    fx_fail = pygame.mixer.Sound(f"{f}fail.mp3")
    fx_fail.set_volume(0.6)
    fx_success = pygame.mixer.Sound(f"{f}success.mp3")
    fx_success.set_volume(0.6)

    m = random.randint(0, len(cool_songs)-1)
    pygame.mixer.music.load(cool_songs[m])
    pygame.mixer.music.play(-1)

    # basic initialization
    bounds = (1280, 720)
    window = pygame.display.set_mode(bounds)
    pygame.display.set_caption(f"Wake up, pp2ease! It's {title}!")
    clock = pygame.time.Clock()
    grid = pygame.image.load(f"{path}/assets/Bg.png")
    grid_rect = grid.get_rect()
    font = pygame.font.Font(f"{path}/assets/dogica.ttf", 18)
    font_big = pygame.font.Font(f"{path}/assets/dogica.ttf", 60)
    lecture_failed = pygame.image.load(f"{path}/assets/fail.png")
    lecture_succeed = pygame.image.load(f"{path}/assets/succeed.png")

    f = f"{path}/assets/kelgenbayev/"
    t_frame = 1
    BLACK = (0,0,0)
    RED = (220,20,60)
    GREEN = (173,255,47)
    WHITE = (255,255,255)
    N = 0 # total num of students

    (st_x, st_y) = (120, 340) # starting point of 1st student in 1st half
    (st2_x, st2_y) = (670, 340) # starting point of 1st student in 2nd half
    temp = (st_x, st_y)
    temp2 = (st2_x, st2_y)

    student_sprites = pygame.sprite.Group()
    awake_set = set(()) # stores all awake and half-asleep student's ids

    def teacher_idle(i): # function that runs teacher's animation
        teacher = pygame.image.load(f"{f}t{i}.png")
        window.blit(teacher, (310, 164))
        
    # locating students
    for _ in range(i): # putting 24 student on left side
        for __ in range(j):
            temp = (temp[0] + 70, temp[1]) # student's every right neighbor is located 70px away
            id = '0' + str(_) + str(__) # format of id: first half + row + column
            student_sprites.add(Student(temp[0], temp[1], int(id), a, b))
            awake_set.add(int(id))
            N += 1
        temp = (st_x, temp[1] + 80) # and located 80 px below

    for _ in range(i): # second half on right
        for __ in range(j):
            temp2 = (temp2[0] + 70, temp2[1])
            id = '1' + str(_) + str(__)
            student_sprites.add(Student(temp2[0], temp2[1], int(id), a, b))
            awake_set.add(int(id))
            N += 1
        temp2 = (st2_x, temp2[1] + 80)

    # for user event
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    inc_speed = pygame.USEREVENT + 1
    pygame.time.set_timer(inc_speed, 20000)

    T = pygame.time.get_ticks() # pygame's time continues moving on from pygame.init(), so to reset it we have to get it's current ellapsed time
    next_frame = pygame.time.get_ticks() # for teacher's animation
    
    while True:

        window.blit(grid, grid_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == inc_speed:
                for entity in student_sprites:
                    Student.change_speed(entity)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # reset energy of student with 'asleep' status
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                for entity in student_sprites:
                    Student.click_event(entity, mouse_x, mouse_y)
        # basic text
        sleeping_number = font.render(f'sleeping: {len(student_sprites) - len(awake_set)}', True, BLACK)
        level_number = font.render(f'level:{title}', True, BLACK)
        time_ellapsed = (pygame.time.get_ticks() - T)//1000
        time_text = font.render(f'time: {time_ellapsed} min', True, BLACK)
        window.blit(sleeping_number, (540,100))        
        window.blit(level_number, (540, 140))
        window.blit(time_text, (540, 180))

        # adds/removes from awake_set according to the status of student
        for entity in student_sprites:
            window.blit(entity.image, entity.rect)
            Student.energy_drain(entity)
            if entity.status == 'asleep' and entity.id in awake_set:
                awake_set.remove(entity.id)
            elif entity.status == 'awake' and entity.id not in awake_set:
                awake_set.add(entity.id)

        # teacher animation
        if pygame.time.get_ticks() > next_frame:
            next_frame += 600
            t_frame += 1
            t_frame = t_frame % 42 + 1
        teacher_idle(t_frame)

        # game over
        if N - len(awake_set) > N//2:
            window.fill((0,0,0))
            window.blit(lecture_failed, (0,0))
            failed = font_big.render('LECTURE FAILED', True, RED)
            info1 = font_big.render(f'level:{title}', True, WHITE)
            info2 = font_big.render(f'time ellapsed:{time_ellapsed}', True, WHITE)
            window.blit(failed, (10,30))
            window.blit(info1, (10, 100))
            window.blit(info2, (10, 180))
            pygame.mixer.music.fadeout(3500)
            m = (m+1)%len(cool_songs)
            pygame.display.update()
            for entity in student_sprites:
                entity.energy = 125
                entity.a = a
                entity.b = b
                entity.next_time = pygame.time.get_ticks()
            T = pygame.time.get_ticks() # we have to substract from moving on time the time we lost to restart from 0
            fx_fail.play()
            pygame.time.wait(3000)
            pygame.mixer.music.load(cool_songs[m])
            pygame.mixer.music.play(-1)

        # next level
        if time_ellapsed == 120:
            window.fill((0,0,0))
            window.blit(lecture_succeed, (0,0))
            succeed = font_big.render('LECTURE SAVED', True, GREEN)
            window.blit(succeed, (10,30))
            window.blit(succeed, (10,100))
            window.blit(succeed, (10,180))
            pygame.display.update()
            fx_success.play()
            pygame.time.wait(3000)
            next_frame = pygame.time.get_ticks()
            pygame.mixer.music.fadeout(3500)
            m = (m+1)%len(cool_songs)
            return 0

        pygame.display.update()
        clock.tick(30)