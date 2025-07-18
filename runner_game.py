import pygame
import random
import pathlib
import math
import os
from enum import Enum
from typing import Dict, List, Tuple

def main(window):
    """
    nFactorial Incubator Challenge
    Помогите Bakha пройти инкубатор, избегая Aselya и собирая монеты  CEO!
    """
    # Инициализация
    pygame.display.set_caption("nFactorial Incubator Challenge")
    pygame.mixer.init()  # Инициализация звуковой системы
    clock = pygame.time.Clock()
    W, H = window.get_size()
    GROUND_Y = int(H * 0.85)
    
    # Цвета nFactorial
    NFACT_BLUE = (13, 71, 161)
    NFACT_GREEN = (0, 230, 118)
    NFACT_ORANGE = (255, 111, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_GRAY = (30, 30, 30)
    LIGHT_GRAY = (200, 200, 200)
    
    # Инициализация музыки
    music_playing = False
    music_volume = 0.4  # Немного тише для гонки
    
    def load_music():
        """Загрузка музыки racer.mp3"""
        try:
            base = pathlib.Path(__file__).parent.resolve()
            music_path = base / "assets" / "mp3" / "racer.mp3"
            if music_path.exists():
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.set_volume(music_volume)
                print(f"Музыка загружена: {music_path}")
                return True
            else:
                print(f"Файл музыки не найден: {music_path}")
                return False
        except Exception as e:
            print(f"Ошибка при загрузке музыки: {e}")
            return False
    
    def play_music():
        """Воспроизведение музыки"""
        nonlocal music_playing
        try:
            if not music_playing:
                pygame.mixer.music.play(-1)  # -1 означает бесконечное воспроизведение
                music_playing = True
                print("Музыка гонки начала играть")
        except Exception as e:
            print(f"Ошибка при воспроизведении музыки: {e}")
    
    def stop_music():
        """Остановка музыки"""
        nonlocal music_playing
        try:
            pygame.mixer.music.stop()
            music_playing = False
            print("Музыка остановлена")
        except Exception as e:
            print(f"Ошибка при остановке музыки: {e}")
    
    def pause_music():
        """Пауза музыки"""
        nonlocal music_playing
        try:
            pygame.mixer.music.pause()
            music_playing = False
            print("Музыка поставлена на паузу")
        except Exception as e:
            print(f"Ошибка при паузе музыки: {e}")
    
    def unpause_music():
        """Возобновление музыки"""
        nonlocal music_playing
        try:
            pygame.mixer.music.unpause()
            music_playing = True
            print("Музыка возобновлена")
        except Exception as e:
            print(f"Ошибка при возобновлении музыки: {e}")
    
    def set_music_volume(volume):
        """Установка громкости музыки (0.0 - 1.0)"""
        nonlocal music_volume
        try:
            music_volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(music_volume)
            print(f"Громкость музыки установлена: {music_volume}")
        except Exception as e:
            print(f"Ошибка при установке громкости: {e}")
    
    # Загрузка музыки
    load_music()
    
    # Загрузка ресурсов
    base = pathlib.Path(__file__).parent.resolve()
    
    # Попытка загрузить изображения персонажей
    def load_character_image(filename, size=(80, 100)):
        try:
            img = pygame.image.load(str(base / "assets" / "students" / filename)).convert_alpha()
            # Применяем сглаживание для более округлого вида
            img = pygame.transform.smoothscale(img, size)
            return img
        except:
            # Создаем заглушку если файл не найден
            surface = pygame.Surface(size, pygame.SRCALPHA)
            # Разные цвета для разных персонажей
            if "bakha" in filename:
                color = NFACT_BLUE
                # Более округлое тело
                pygame.draw.ellipse(surface, color, (10, 30, size[0]-20, size[1]-40))
                # Округлая голова
                pygame.draw.circle(surface, WHITE, (size[0]//2, 20), 18)
                # Глаза
                pygame.draw.circle(surface, BLACK, (size[0]//2-6, 17), 3)
                pygame.draw.circle(surface, BLACK, (size[0]//2+6, 17), 3)
                # Улыбка
                pygame.draw.arc(surface, BLACK, (size[0]//2-8, 20, 16, 10), 0, 3.14, 2)
            elif "aselya" in filename:
                color = (220, 50, 50)
                # Округлые формы вместо прямоугольных
                pygame.draw.ellipse(surface, color, (0, 0, size[0], size[1]))
                pygame.draw.ellipse(surface, (255, 100, 100), (8, 8, size[0]-16, size[1]-16))
                # Добавляем эффекты
                for i in range(15):
                    x, y = random.randint(0, size[0]-5), random.randint(0, size[1]-5)
                    pygame.draw.circle(surface, (255, 0, 0), (x, y), 2)
            elif "bekzhan" in filename:
                color = NFACT_GREEN
                # Большая округлая монета
                pygame.draw.circle(surface, color, (size[0]//2, size[1]//2), size[0]//2-2)
                pygame.draw.circle(surface, WHITE, (size[0]//2, size[1]//2), size[0]//2-8)
                pygame.draw.circle(surface, color, (size[0]//2, size[1]//2), size[0]//2-14)
                # Символ в центре
                font = pygame.font.Font(None, 32)
                text = font.render("B", True, WHITE)
                text_rect = text.get_rect(center=(size[0]//2, size[1]//2))
                surface.blit(text, text_rect)
            return surface
    
    # Загрузка фона
    try:
        bg_image = pygame.image.load(str(base / "assets" /"students"/ "background.png")).convert()
        bg_image = pygame.transform.scale(bg_image, (W, H))
    except:
        # Создаем градиентный фон если файл не найден
        bg_image = pygame.Surface((W, H))
        for y in range(H):
            ratio = y / H
            r = int(50 * (1 - ratio) + 100 * ratio)
            g = int(80 * (1 - ratio) + 120 * ratio)
            b = int(120 * (1 - ratio) + 180 * ratio)
            pygame.draw.line(bg_image, (r, g, b), (0, y), (W, y))
    
    # Загрузка изображений персонажей с увеличенными размерами
    bakha_img = load_character_image("bakha.png", (65, 95))
    aselya_img = load_character_image("aselya.png", (70, 70))
    aselya1_img = load_character_image("aselya1.png", (70, 70))  # Второй вариант Aselya
    bekzhan_img = load_character_image("bekzhan.png", (45, 45))
    
    # Список изображений Aselya для случайного выбора
    aselya_images = [aselya_img, aselya1_img]
    
    # Шрифты
    font_small = pygame.font.Font(None, 24)
    font_medium = pygame.font.Font(None, 32)
    font_big = pygame.font.Font(None, 48)
    font_huge = pygame.font.Font(None, 72)
    
    # Полосы движения
    lanes = [W * 0.2, W * 0.5, W * 0.8]
    GRAVITY = 1.5
    JUMP_V = -22
    
    # Система частиц
    class Particle:
        def __init__(self, x: float, y: float, vx: float, vy: float, color: Tuple[int, int, int], life: int):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.color = color
            self.life = life
            self.max_life = life
        
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.vy += 0.2  # Гравитация
            self.life -= 1
        
        def draw(self, surface):
            alpha = int(255 * (self.life / self.max_life))
            try:
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)
            except:
                pass
    
    class ParticleSystem:
        def __init__(self):
            self.particles = []
        
        def add_explosion(self, x: float, y: float, color: Tuple[int, int, int]):
            for _ in range(15):
                vx = random.uniform(-8, 8)
                vy = random.uniform(-12, -4)
                self.particles.append(Particle(x, y, vx, vy, color, 30))
        
        def update(self):
            self.particles = [p for p in self.particles if p.life > 0]
            for particle in self.particles:
                particle.update()
        
        def draw(self, surface):
            for particle in self.particles:
                particle.draw(surface)
    
    # Игрок (Bakha)
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = bakha_img.copy()
            self.lane_idx = 1
            self.rect = self.image.get_rect(midbottom=(lanes[self.lane_idx], GROUND_Y - 5))
            self.vy = 0
            self.jumping = False
            self.animation_frame = 0
            self.animation_timer = 0
            self.invulnerable = 0
            self.trail_positions = []
        
        def update(self):
            # Физика прыжка
            if self.jumping:
                self.vy += GRAVITY
                self.rect.y += self.vy
                if self.rect.bottom >= GROUND_Y - 5:
                    self.rect.bottom = GROUND_Y - 5
                    self.vy = 0
                    self.jumping = False
            
            # Анимация
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.animation_frame = (self.animation_frame + 1) % 4
                self.animation_timer = 0
            
            # Обновление состояний
            if self.invulnerable > 0:
                self.invulnerable -= 1
            
            # След
            self.trail_positions.append((self.rect.centerx, self.rect.centery))
            if len(self.trail_positions) > 8:
                self.trail_positions.pop(0)
        
        def move_left(self):
            if self.lane_idx > 0:
                self.lane_idx -= 1
                self.rect.centerx = lanes[self.lane_idx]
        
        def move_right(self):
            if self.lane_idx < 2:
                self.lane_idx += 1
                self.rect.centerx = lanes[self.lane_idx]
        
        def jump(self):
            if not self.jumping:
                self.jumping = True
                self.vy = JUMP_V
        
        def draw_trail(self, surface):
            for i, pos in enumerate(self.trail_positions):
                if i > 0:
                    alpha = int(255 * (i / len(self.trail_positions)) * 0.3)
                    try:
                        pygame.draw.circle(surface, NFACT_BLUE, pos, 2)
                    except:
                        pass
    
    # Препятствие (Aselya) с случайным выбором варианта
    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, speed: float):
            super().__init__()
            # Случайно выбираем один из вариантов Aselya
            self.image = random.choice(aselya_images).copy()
            self.speed = speed
            self.lane_idx = random.randint(0, 2)
            self.rect = self.image.get_rect(midbottom=(lanes[self.lane_idx], -50))
            self.rotation = 0
        
        def update(self):
            self.rect.y += self.speed
            self.rotation += 2
            if self.rect.top > H:
                self.kill()
    
    # Монета (Bekzhan) с эффектами
    class Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.original_image = bekzhan_img.copy()
            self.image = self.original_image.copy()
            self.lane_idx = random.randint(0, 2)
            self.rect = self.image.get_rect(center=(lanes[self.lane_idx], -30))
            self.float_offset = 0
            self.collected = False
            self.pulse_timer = 0
            self.glow_radius = 0
        
        def update(self):
            self.rect.y += 5
            self.float_offset += 0.2
            self.pulse_timer += 0.15
            
            # Плавающее движение
            self.rect.x += math.sin(self.float_offset) * 1.5
            
            # Анимация вращения
            angle = (pygame.time.get_ticks() * 0.3) % 360
            self.image = pygame.transform.rotate(self.original_image, angle)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            # Эффект пульсации
            scale_factor = 1.0 + math.sin(self.pulse_timer) * 0.1
            if scale_factor != 1.0:
                new_size = (int(45 * scale_factor), int(45 * scale_factor))
                self.image = pygame.transform.scale(self.original_image, new_size)
                self.image = pygame.transform.rotate(self.image, angle)
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
            
            # Эффект свечения
            self.glow_radius = 20 + math.sin(self.pulse_timer * 2) * 8
            
            if self.rect.top > H:
                self.kill()
        
        def draw_glow(self, surface):
            # Рисуем эффект свечения вокруг монеты
            glow_surface = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
            
            # Градиентное свечение
            for i in range(int(self.glow_radius)):
                alpha = max(0, int(50 * (1 - i / self.glow_radius)))
                color = (*NFACT_GREEN, alpha)
                try:
                    pygame.draw.circle(glow_surface, NFACT_GREEN, 
                                     (int(self.glow_radius), int(self.glow_radius)), 
                                     int(self.glow_radius - i))
                except:
                    pass
            
            # Позиция для отрисовки свечения
            glow_x = self.rect.centerx - self.glow_radius
            glow_y = self.rect.centery - self.glow_radius
            surface.blit(glow_surface, (glow_x, glow_y), special_flags=pygame.BLEND_ADD)
    
    # Инициализация системы
    particle_system = ParticleSystem()
    
    # Игровые объекты
    player = Player()
    obstacles = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    
    # Игровые переменные
    score = 0  # Количество собранных монет Bekzhan
    health = 0  # Количество столкновений с Aselya (-3 = исключение)
    distance = 0
    game_speed = 6
    
    # События
    OBSTACLE_EVENT = pygame.USEREVENT + 1
    COIN_EVENT = pygame.USEREVENT + 2
    SPEED_UP_EVENT = pygame.USEREVENT + 3
    
    # Установка таймеров
    pygame.time.set_timer(OBSTACLE_EVENT, 1500)  # Aselya появляется каждые 1.5 сек
    pygame.time.set_timer(COIN_EVENT, 2000)      # Bekzhan монеты каждые 2 сек
    pygame.time.set_timer(SPEED_UP_EVENT, 10000) # Ускорение каждые 10 сек
    
    def draw_hud(surface):
        # Фон HUD
        hud_surface = pygame.Surface((W, 100), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 150))
        surface.blit(hud_surface, (0, 0))
        
        # Заголовок
        title_text = font_medium.render("nFactorial Incubator Challenge", True, WHITE)
        surface.blit(title_text, (10, 10))
        
        # Счетчик монет Bekzhan с увеличенной иконкой
        bekzhan_mini = pygame.transform.scale(bekzhan_img, (35, 35))
        surface.blit(bekzhan_mini, (10, 35))
        score_text = font_medium.render(f"CEO coins: {score}/7", True, NFACT_GREEN)
        surface.blit(score_text, (55, 45))
        
        # Счетчик столкновений с Aselya с увеличенной иконкой
        aselya_mini = pygame.transform.scale(aselya_img, (35, 35))
        surface.blit(aselya_mini, (280, 35))
        health_color = (255, 0, 0) if health <= -2 else (255, 200, 0) if health <= -1 else WHITE
        health_text = font_medium.render(f"Aselya hits: {health}/3", True, health_color)
        surface.blit(health_text, (325, 45))
        
        # Прогресс бар для победы
        progress_rect = pygame.Rect(480, 50, 200, 15)
        pygame.draw.rect(surface, DARK_GRAY, progress_rect)
        progress_fill = int(200 * (score / 7))
        pygame.draw.rect(surface, NFACT_GREEN, (480, 50, progress_fill, 15))
        progress_text = font_small.render("Прогресс в инкубаторе", True, WHITE)
        surface.blit(progress_text, (480, 30))
        
        # Дистанция
        distance_text = font_small.render(f"Дистанция: {distance}м", True, WHITE)
        surface.blit(distance_text, (W - 150, 15))
        
        # Скорость
        speed_text = font_small.render(f"Скорость: {game_speed}", True, WHITE)
        surface.blit(speed_text, (W - 150, 35))
        
        # Индикатор музыки
        music_status = "🔊" if music_playing else "🔇"
        music_text = font_small.render(f"Музыка: {music_status}", True, WHITE)
        surface.blit(music_text, (W - 150, 55))
    
    def draw_lanes(surface):
        # Полосы движения
        for i, lane_x in enumerate(lanes):
            # Пунктирная линия
            for y in range(0, H, 40):
                if i < len(lanes) - 1:  # Не рисуем после последней полосы
                    pygame.draw.line(surface, LIGHT_GRAY, 
                                   (lane_x + 25, y), (lane_x + 25, y + 20), 2)
        
        # Земля
        pygame.draw.rect(surface, DARK_GRAY, (0, GROUND_Y, W, H - GROUND_Y))
        
        # Детали дороги
        for i in range(3):
            pygame.draw.line(surface, WHITE, (lanes[i] - 30, GROUND_Y), (lanes[i] - 30, GROUND_Y - 10), 3)
            pygame.draw.line(surface, WHITE, (lanes[i] + 30, GROUND_Y), (lanes[i] + 30, GROUND_Y - 10), 3)
    
    def show_victory_screen():
        # Останавливаем музыку при победе
        stop_music()
        
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        window.blit(overlay, (0, 0))
        
        # Большое изображение Bakha
        victory_bakha = pygame.transform.scale(bakha_img, (150, 225))
        window.blit(victory_bakha, (W//2 - 75, H//2 - 200))
        
        victory_text = font_huge.render("ПОЗДРАВЛЯЕМ!", True, NFACT_GREEN)
        subtitle_text = font_medium.render("Bakha принят в nFactorial Incubator DEMO day!", True, WHITE)
        score_text = font_medium.render(f"Собрано монет CEO: {score}", True, NFACT_GREEN)
        distance_text = font_medium.render(f"Пройдено: {distance}м", True, WHITE)
        
        texts = [victory_text, subtitle_text, score_text, distance_text]
        y_positions = [H//2 + 50, H//2 + 100, H//2 + 130, H//2 + 160]
        
        for text, y in zip(texts, y_positions):
            window.blit(text, (W//2 - text.get_width()//2, y))
        
        pygame.display.flip()
        pygame.time.wait(4000)
        return True
    
    def show_failure_screen():
        # Останавливаем музыку при поражении
        stop_music()
        
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        window.blit(overlay, (0, 0))
        
        # Большое изображение случайной Aselya
        failure_aselya = pygame.transform.scale(random.choice(aselya_images), (150, 150))
        window.blit(failure_aselya, (W//2 - 75, H//2 - 200))
        
        failure_text = font_huge.render("ИСКЛЮЧЕН!", True, (255, 0, 0))
        subtitle_text = font_medium.render("Aselya исключила Bakha из инкубатора!", True, WHITE)
        score_text = font_medium.render(f"Собрано монет: {score}/7", True, (255, 200, 0))
        hits_text = font_medium.render(f"Столкновений с Aselya: {abs(health)}", True, (255, 0, 0))
        
        texts = [failure_text, subtitle_text, score_text, hits_text]
        y_positions = [H//2 + 50, H//2 + 100, H//2 + 130, H//2 + 160]
        
        for text, y in zip(texts, y_positions):
            window.blit(text, (W//2 - text.get_width()//2, y))
        
        pygame.display.flip()
        pygame.time.wait(4000)
        return False
    
    # Автоматически запускаем музыку при старте игры
    play_music()
    
    # Основной игровой цикл
    running = True
    dt = 0
    
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time в секундах
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_music()
                    return True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move_left()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move_right()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.jump()
                elif event.key == pygame.K_m:
                    # Управление музыкой клавишей M
                    if music_playing:
                        pause_music()
                    else:
                        unpause_music()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Увеличение громкости
                    set_music_volume(music_volume + 0.1)
                elif event.key == pygame.K_MINUS:
                    # Уменьшение громкости
                    set_music_volume(music_volume - 0.1)
            
            elif event.type == OBSTACLE_EVENT:
                obstacle = Obstacle(game_speed)
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
            
            elif event.type == COIN_EVENT:
                coin = Coin()
                coins.add(coin)
                all_sprites.add(coin)
            
            elif event.type == SPEED_UP_EVENT:
                game_speed += 1
                # Увеличиваем частоту препятствий
                if game_speed > 8:
                    pygame.time.set_timer(OBSTACLE_EVENT, max(800, 1500 - (game_speed - 6) * 100))
        
        # Обновление объектов
        all_sprites.update()
        particle_system.update()
        
        # Увеличение дистанции
        distance += 1
        
        # Столкновения с препятствиями (Aselya)
        if player.invulnerable <= 0:
            hit_obstacles = pygame.sprite.spritecollide(player, obstacles, True)
            if hit_obstacles:
                health -= 1
                particle_system.add_explosion(player.rect.centerx, player.rect.centery, (255, 0, 0))
                player.invulnerable = 120  # 2 секунды неуязвимости
                
                # Проверка на исключение
                if health <= -3:
                    return show_failure_screen()
        
        # Сбор монет (Bekzhan) с улучшенными эффектами
        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected_coins:
            score += 1
            # Мощный эффект при сборе монеты
            particle_system.add_explosion(coin.rect.centerx, coin.rect.centery, NFACT_GREEN)
            # Дополнительные золотые частицы
            for _ in range(10):
                vx = random.uniform(-6, 6)
                vy = random.uniform(-10, -2)
                particle_system.particles.append(
                    Particle(coin.rect.centerx, coin.rect.centery, vx, vy, (255, 215, 0), 40)
                )
            
            # Проверка на победу
            if score >= 7:
                return show_victory_screen()
        
        # Отрисовка
        # Фон
        window.blit(bg_image, (0, 0))
        
        # Дорога
        draw_lanes(window)
        
        # След игрока
        player.draw_trail(window)
        
        # Мигание при неуязвимости
        if player.invulnerable > 0 and player.invulnerable % 20 < 10:
            pass  # Не рисуем игрока
        else:
            # Рисуем игрока
            window.blit(player.image, player.rect)
        
        # Рисуем эффекты свечения для монет
        for coin in coins:
            coin.draw_glow(window)
        
        # Рисуем препятствия и монеты
        for sprite in all_sprites:
            if sprite != player:
                window.blit(sprite.image, sprite.rect)
        
        # Частицы
        particle_system.draw(window)
        
        # HUD
        draw_hud(window)
        
        # Подсказки управления (первые 15 секунд)
        if pygame.time.get_ticks() < 15000:
            hints = [
                "Цель: Соберите 7 монет CEO для поступления в инкубатор",
                "Избегайте Aselya! 3 столкновения = исключение",
                "Управление: Стрелки/WASD - движение, SPACE/W - прыжок",
                "M - пауза/возобновление музыки, +/- - громкость, ESC - выход"
            ]
            
            hint_bg = pygame.Surface((W, 80), pygame.SRCALPHA)
            hint_bg.fill((0, 0, 0, 180))
            window.blit(hint_bg, (0, H - 80))
            
            for i, hint in enumerate(hints):
                hint_text = font_small.render(hint, True, WHITE)
                window.blit(hint_text, (10, H - 75 + i * 18))
        
        # Индикатор неуязвимости
        if player.invulnerable > 0:
            invul_text = font_small.render(f"Защита: {player.invulnerable//60 + 1}s", True, NFACT_BLUE)
            window.blit(invul_text, (W - 150, H - 40))
        
        # Предупреждение при критическом здоровье
        if health <= -2:
            warning_text = font_big.render("ОСТОРОЖНО! СЛЕДУЮЩЕЕ СТОЛКНОВЕНИЕ = ИСКЛЮЧЕНИЕ!", True, (255, 0, 0))
            text_rect = warning_text.get_rect(center=(W//2, 150))
            # Мигающий эффект
            if (pygame.time.get_ticks() // 300) % 2:
                window.blit(warning_text, text_rect)
        
        pygame.display.flip()
    
    return False