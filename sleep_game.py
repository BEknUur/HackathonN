import pygame
from student import Student
import random
import pathlib
import os

path = pathlib.Path(__file__).parent.resolve()

def main(window, i=4, j=6, a=5000, b=12000, title='Nurqisa oyan!'):
    """
    Wake‑Up game.
    window  — pygame.Surface из main.py
    i, j    — ряды и колонки студентов
    a, b    — скорость потери энергии
    title   — название уровня
    Возвращает True (успех) или False (выход).
    """
    # — sound setup
    base_mp3 = f"{path}/assets/mp3/"
    tracks = [
        "c418_lullaby.mp3", "c418_sweden.mp3", "c418_wet.mp3",
        "evil_morty.mp3", "rick_roll.mp3",
        "undertale_shop.mp3", "jojo.mp3"
    ]
    fx_fail = pygame.mixer.Sound(base_mp3 + "fail.mp3")
    fx_success = pygame.mixer.Sound(base_mp3 + "success.mp3")
    fx_fail.set_volume(0.6)
    fx_success.set_volume(0.6)

    pygame.mixer.music.load(base_mp3 + random.choice(tracks))
    pygame.mixer.music.play(-1)

    # — window & assets
    pygame.display.set_caption(f"Wake up — {title}")
    clock = pygame.time.Clock()
    bg = pygame.image.load(f"{path}/assets/Bg.png")
    font = pygame.font.Font(f"{path}/assets/dogica.ttf", 18)
    font_big = pygame.font.Font(f"{path}/assets/dogica.ttf", 60)
    img_fail = pygame.image.load(f"{path}/assets/fail.png")
    img_success = pygame.image.load(f"{path}/assets/succeed.png")

    # — prepare students
    student_sprites = pygame.sprite.Group()
    awake_ids = set()
    total = 0

    def populate(start, half):
        nonlocal total
        x0, y0 = start
        for row in range(i):
            x = x0
            for col in range(j):
                x += 70
                sid = int(f"{half}{row}{col}")
                s = Student(x, y0, sid, a, b)
                student_sprites.add(s)
                awake_ids.add(sid)
                total += 1
            y0 += 80

    populate((120, 340), 0)
    populate((670, 340), 1)

    # teacher animation setup: ровно 41 кадр
    teach_dir = path / "assets" / "kelgenbayev"
    num_frames = 41
    frame_idx = 0
    next_frame = pygame.time.get_ticks()

    # speed‑up event
    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 10000)

    level_start = pygame.time.get_ticks()

    # — main loop
    while True:
        window.blit(bg, (0, 0))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return False
            if ev.type == INC_SPEED:
                for s in student_sprites:
                    s.change_speed()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = pygame.mouse.get_pos()
                for s in student_sprites:
                    s.click_event(mx, my)

        # — update & draw students
        for s in student_sprites:
            s.energy_drain()
            if s.status == 'asleep' and s.id in awake_ids:
                awake_ids.remove(s.id)
            elif s.status != 'asleep' and s.id not in awake_ids:
                awake_ids.add(s.id)
            window.blit(s.image, s.rect)

        # — stats
        slept = total - len(awake_ids)
        elapsed = (pygame.time.get_ticks() - level_start) // 1000
        window.blit(font.render(f"Sleeping: {slept}", True, (0,0,0)), (540,100))
        window.blit(font.render(f"Level:{title}", True, (0,0,0)), (540,140))
        window.blit(font.render(f"Time: {elapsed}", True, (0,0,0)), (540,180))

        # — teacher animate (41 кадр)
        now = pygame.time.get_ticks()
        if now >= next_frame:
            next_frame += 100
            frame_idx = (frame_idx + 1) % num_frames
        filename = f"t{frame_idx+1}.png"
        teacher_img = pygame.image.load(str(teach_dir / filename))
        window.blit(teacher_img, (310, 164))

        # — game over?
        if slept > total // 2:
            window.fill((0,0,0))
            window.blit(img_fail, (0,0))
            fx_fail.play()
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.mixer.music.fadeout(1500)
            return False

        # — level success?
        if elapsed >= 30:
            window.fill((0,0,0))
            window.blit(img_success, (0,0))
            fx_success.play()
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.mixer.music.fadeout(1500)
            return True

        pygame.display.update()
        clock.tick(30)
