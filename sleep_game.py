import pygame
from student import Student
import random
import pathlib
import os

path = pathlib.Path(__file__).parent.resolve()

def main(window, i=4, j=6, a=5000, b=12000, title='Nurqisa oyan!'):
    """
    Wake‑Up game with photo integration.
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

    # — Загрузка и подготовка фотографий
    photos = []
    photo_paths = [
        f"{path}/assets/photos.webp",  # Студент спит за компьютером
        f"{path}/assets/photos1.webp",  # Студент спит в аудитории
      
    ]
    
    for photo_path in photo_paths:
        if os.path.exists(photo_path):
            try:
                photo = pygame.image.load(photo_path)
                # Масштабируем фотографии для использования в игре (увеличенный размер)
                photo = pygame.transform.scale(photo, (220, 160))
                photos.append(photo)
            except pygame.error:
                print(f"Не удалось загрузить фото: {photo_path}")
    
    # — Создание рамок для фотографий (увеличенные размеры)
    frame_surface = pygame.Surface((235, 175))
    frame_surface.fill((139, 69, 19))  # Коричневая рамка
    frame_inner = pygame.Surface((220, 160))
    frame_inner.fill((255, 255, 255))  # Белая внутренняя часть

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
    photo_display_time = 0
    current_photo_idx = 0

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

        # — Отображение фотографий как картины на стенах (увеличенные размеры)
        if photos:
            # Левая стена - фото студента за компьютером (больший размер)
            if len(photos) > 0:
                window.blit(frame_surface, (20, 30))
                window.blit(frame_inner, (27, 37))
                window.blit(photos[0], (27, 37))
            
            # Правая стена - фото студента в аудитории (больший размер)
            if len(photos) > 1:
                window.blit(frame_surface, (1025, 30))
                window.blit(frame_inner, (1032, 37))
                window.blit(photos[1], (1032, 37))
            
            # Верхняя часть - фото университета (тоже увеличиваем)
            if len(photos) > 2:
                medium_frame = pygame.Surface((180, 130))
                medium_frame.fill((139, 69, 19))
                medium_inner = pygame.Surface((165, 115))
                medium_inner.fill((255, 255, 255))
                medium_photo = pygame.transform.scale(photos[2], (165, 115))
                
                window.blit(medium_frame, (550, 10))
                window.blit(medium_inner, (557, 17))
                window.blit(medium_photo, (557, 17))

        # — Добавление мемориальных табличек под фотографиями (обновленные позиции)
        if photos:
            nameplate_font = pygame.font.Font(f"{path}/assets/dogica.ttf", 14)
            if len(photos) > 0:
                nameplate1 = nameplate_font.render("Студент за работой", True, (0,0,0))
                window.blit(nameplate1, (20, 210))
            
            if len(photos) > 1:
                nameplate2 = nameplate_font.render("Лекция в аудитории", True, (0,0,0))
                window.blit(nameplate2, (1025, 210))
            
            if len(photos) > 2:
                nameplate3 = nameplate_font.render("Наш университет", True, (0,0,0))
                window.blit(nameplate3, (575, 150))

        # — teacher animate (41 кадр)
        now = pygame.time.get_ticks()
        if now >= next_frame:
            next_frame += 100
            frame_idx = (frame_idx + 1) % num_frames
        filename = f"t{frame_idx+1}.png"
        teacher_img = pygame.image.load(str(teach_dir / filename))
        window.blit(teacher_img, (310, 164))

        # — Пасхальное яйцо: случайное появление мини-фотографии (увеличенный размер)
        if photos and elapsed > 10 and random.randint(1, 300) == 1:
            easter_photo = pygame.transform.scale(photos[random.randint(0, len(photos)-1)], (120, 90))
            easter_x = random.randint(50, 1100)
            easter_y = random.randint(50, 150)
            window.blit(easter_photo, (easter_x, easter_y))

        # — game over?
        if slept > total // 2:
            window.fill((0,0,0))
            window.blit(img_fail, (0,0))
            
            # Показываем фото провала (если есть) - увеличенный размер
            if photos:
                fail_photo = pygame.transform.scale(photos[0], (300, 220))
                window.blit(fail_photo, (490, 250))
                fail_text = font.render("Все заснули...", True, (255,255,255))
                window.blit(fail_text, (520, 480))
            
            fx_fail.play()
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.mixer.music.fadeout(1500)
            return False

        # — level success?
        if elapsed >= 30:
            window.fill((0,0,0))
            window.blit(img_success, (0,0))
            
            # Показываем фото успеха (если есть) - увеличенный размер
            if len(photos) > 2:
                success_photo = pygame.transform.scale(photos[2], (300, 220))
                window.blit(success_photo, (490, 250))
                success_text = font.render("Лекция спасена!", True, (255,255,255))
                window.blit(success_text, (520, 480))
            
            fx_success.play()
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.mixer.music.fadeout(1500)
            return True

        pygame.display.update()
        clock.tick(30)


# Дополнительная функция для подготовки фотографий
def prepare_photos():
    """
    Функция для подготовки фотографий для использования в игре.
    Создает необходимые папки и инструкции по размещению фотографий.
    """
    photo_dir = path / "assets" / "photos"
    
    if not photo_dir.exists():
        photo_dir.mkdir(parents=True, exist_ok=True)
        print(f"Создана папка для фотографий: {photo_dir}")
        print("Поместите ваши фотографии в эту папку с именами:")
        print("- photo1.jpg (студент за компьютером)")
        print("- photo2.jpg (студент в аудитории)")
        print("- photo3.jpg (здание университета)")
        print("Рекомендуемый размер: 300x200 пикселей или больше")
    
    return photo_dir