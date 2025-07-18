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
    font_medium = pygame.font.Font(f"{path}/assets/dogica.ttf", 24)
    font_small = pygame.font.Font(f"{path}/assets/dogica.ttf", 14)
    img_fail = pygame.image.load(f"{path}/assets/fail.png")
    img_success = pygame.image.load(f"{path}/assets/succeed.png")

    # — Загрузка и подготовка фотографий
    photos = []
    photo_paths = [
        f"{path}/assets/photos.webp",  # Студент спит за компьютером
        f"{path}/assets/photos1.webp",  # Студент спит в аудитории
        f"{path}/assets/classroom.png",  # Реальная аудитория
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

    # — Создание черной доски
    board_width = 400
    board_height = 180
    board_surface = pygame.Surface((board_width, board_height))
    board_surface.fill((25, 25, 25))  # Черная доска
    
    # Рамка доски
    pygame.draw.rect(board_surface, (139, 69, 19), (0, 0, board_width, board_height), 8)
    pygame.draw.rect(board_surface, (50, 50, 50), (8, 8, board_width-16, board_height-16), 4)

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
    
    # Анимация для текста на доске
    board_text_alpha = 0
    board_text_direction = 1

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

        # — stats with improved styling
        slept = total - len(awake_ids)
        elapsed = (pygame.time.get_ticks() - level_start) // 1000
        
        # Создаем красивую панель статистики
        stats_panel = pygame.Surface((280, 200), pygame.SRCALPHA)
        stats_panel.fill((0, 0, 0, 120))  # Полупрозрачный черный фон
        pygame.draw.rect(stats_panel, (255, 255, 255, 50), (0, 0, 280, 200), 2)
        
        window.blit(stats_panel, (520, 80))
        window.blit(font.render(f"Sleeping: {slept}", True, (255,255,255)), (540,100))
        window.blit(font.render(f"Level: {title}", True, (255,255,255)), (540,140))
        window.blit(font.render(f"Time: {elapsed}s", True, (255,255,255)), (540,180))
        
        # Добавляем информацию о разработчиках
        dev_info = font_small.render("DevOps: Bernard", True, (200,200,200))
        window.blit(dev_info, (540, 220))
        
        tech_info = font_small.render("Tech Lead: k.turysov", True, (200,200,200))
        window.blit(tech_info, (540, 240))
        
        game_info = font_small.render("Game by nFactorial", True, (200,200,200))
        window.blit(game_info, (540, 260))

        # — Отображение фотографий как картины на стенах
        if photos:
            # Левая стена - фото студента за компьютером
            if len(photos) > 0:
                window.blit(frame_surface, (20, 30))
                window.blit(frame_inner, (27, 37))
                window.blit(photos[0], (27, 37))
            
            # Правая стена - фото студента в аудитории
            if len(photos) > 1:
                window.blit(frame_surface, (1025, 30))
                window.blit(frame_inner, (1032, 37))
                window.blit(photos[1], (1032, 37))
            
            # Правая сторона внизу - реальная аудитория (новая фотография)
            if len(photos) > 2:
                # Создаем рамку для новой фотографии
                new_frame = pygame.Surface((200, 150))
                new_frame.fill((139, 69, 19))
                new_frame_inner = pygame.Surface((185, 135))
                new_frame_inner.fill((255, 255, 255))
                new_photo = pygame.transform.scale(photos[2], (185, 135))
                
                window.blit(new_frame, (1070, 240))
                window.blit(new_frame_inner, (1077, 247))
                window.blit(new_photo, (1077, 247))

        # — Улучшенная черная доска с белым текстом
        board_x = 440
        board_y = 50
        window.blit(board_surface, (board_x, board_y))
        
        # Заголовок игры - белый текст на черной доске
        title_text = font_medium.render("Game for Nurqisa", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=board_x + board_width//2, y=board_y + 25)
        window.blit(title_text, title_rect)
        
        # Подзаголовок
        subtitle_text = font_small.render("Wake Up Challenge", True, (200, 255, 200))
        subtitle_rect = subtitle_text.get_rect(centerx=board_x + board_width//2, y=board_y + 50)
        window.blit(subtitle_text, subtitle_rect)
        
        # Разделительная линия белая
        pygame.draw.line(window, (255, 255, 255), 
                        (board_x + 40, board_y + 75), (board_x + board_width - 40, board_y + 75), 2)
        
        # Инструкции на английском с яркими цветами для черной доски
        instructions = [
            ("Goal: Keep students awake!", (255, 100, 100)),
            ("Click = Wake up student", (100, 200, 255)),
            (f"Time: {elapsed}s / 30s", (255, 200, 100)),
            (f"Sleeping: {slept}/{total}", (255, 100, 255))
        ]
        
        for i, (instruction, color) in enumerate(instructions):
            inst_text = font_small.render(instruction, True, color)
            inst_rect = inst_text.get_rect(centerx=board_x + board_width//2, y=board_y + 90 + i*18)
            window.blit(inst_text, inst_rect)

        # — Добавление табличек под фотографиями на английском
        if photos:
            nameplate_font = font_small
            if len(photos) > 0:
                nameplate1 = nameplate_font.render("Student at Work", True, (255,255,255))
                # Создаем фон для таблички
                nameplate_bg = pygame.Surface((140, 25), pygame.SRCALPHA)
                nameplate_bg.fill((0, 0, 0, 180))
                window.blit(nameplate_bg, (30, 210))
                window.blit(nameplate1, (35, 215))
            
            if len(photos) > 1:
                nameplate2 = nameplate_font.render("Lecture Hall", True, (255,255,255))
                nameplate_bg2 = pygame.Surface((120, 25), pygame.SRCALPHA)
                nameplate_bg2.fill((0, 0, 0, 180))
                window.blit(nameplate_bg2, (1040, 210))
                window.blit(nameplate2, (1045, 215))
            
            if len(photos) > 2:
                nameplate3 = nameplate_font.render("Real Classroom", True, (255,255,255))
                nameplate_bg3 = pygame.Surface((150, 25), pygame.SRCALPHA)
                nameplate_bg3.fill((0, 0, 0, 180))
                window.blit(nameplate_bg3, (1085, 395))
                window.blit(nameplate3, (1090, 400))

        # — teacher animate (41 кадр)
        now = pygame.time.get_ticks()
        if now >= next_frame:
            next_frame += 100
            frame_idx = (frame_idx + 1) % num_frames
        filename = f"t{frame_idx+1}.png"
        teacher_img = pygame.image.load(str(teach_dir / filename))
        window.blit(teacher_img, (310, 164))
        
        # Добавляем табличку "Bernard AI" под учителем
        teacher_name_bg = pygame.Surface((120, 25), pygame.SRCALPHA)
        teacher_name_bg.fill((0, 0, 0, 180))
        teacher_name = font_small.render("Bernard AI", True, (255, 255, 255))
        teacher_name_rect = teacher_name.get_rect(center=(375, 315))
        teacher_bg_rect = teacher_name_bg.get_rect(center=(375, 315))
        
        window.blit(teacher_name_bg, teacher_bg_rect)
        window.blit(teacher_name, teacher_name_rect)

        # — Пасхальное яйцо: случайное появление мини-фотографии с эффектом
        if photos and elapsed > 10 and random.randint(1, 400) == 1:
            easter_photo = pygame.transform.scale(photos[random.randint(0, len(photos)-1)], (100, 75))
            easter_x = random.randint(50, 1100)
            easter_y = random.randint(50, 150)
            
            # Добавляем эффект свечения
            glow_surface = pygame.Surface((120, 95), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surface, (255, 255, 0, 100), (0, 0, 120, 95))
            window.blit(glow_surface, (easter_x-10, easter_y-10))
            window.blit(easter_photo, (easter_x, easter_y))

        # — game over?
        if slept > total // 2:
            window.fill((0,0,0))
            window.blit(img_fail, (0,0))
            
            # Показываем фото провала (если есть) - увеличенный размер
            if photos:
                fail_photo = pygame.transform.scale(photos[0], (300, 220))
                window.blit(fail_photo, (490, 250))
                fail_text = font_medium.render("Everyone fell asleep...", True, (255,255,255))
                window.blit(fail_text, (480, 480))
                
                # Добавляем информацию о разработчиках
                dev_text = font_small.render("DevOps Infrastructure: Bernard", True, (150,150,150))
                window.blit(dev_text, (420, 520))
                
                tech_text = font_small.render("Tech Lead: k.turysov", True, (150,150,255))
                window.blit(tech_text, (450, 540))
            
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
            if len(photos) > 1:
                success_photo = pygame.transform.scale(photos[1], (300, 220))
                window.blit(success_photo, (490, 250))
                success_text = font_medium.render("Lecture Saved!", True, (255,255,255))
                window.blit(success_text, (530, 480))
                
                # Добавляем благодарность команде
                team_text = font_small.render("Thanks to nFactorial Team!", True, (150,255,150))
                window.blit(team_text, (460, 520))
                
                bernard_text = font_small.render("DevOps Support: Bernard", True, (150,150,255))
                window.blit(bernard_text, (480, 540))
                
                tech_text = font_small.render("Tech Lead: k.turysov", True, (255,200,150))
                window.blit(tech_text, (490, 560))
            
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
        print("Place your photos in this folder with names:")
        print("- photo1.jpg (student at computer)")
        print("- photo2.jpg (student in classroom)")  
        print("- classroom.jpg (real classroom photo)")
        print("Recommended size: 300x200 pixels or larger")
        print("\nGame developed by nFactorial team")
        print("DevOps Infrastructure: Bernard")
        print("Tech Lead: k.turysov")
    
    return photo_dir