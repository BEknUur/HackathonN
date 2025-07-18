import pygame
import random
import math
import time
import pathlib
import os
from typing import List, Tuple, Optional

def main(window):
    """
    Дитрис - Diana Tetris Edition
    Соберите 3 блока за 30 секунд с фотографиями Дианы!
    """
    pygame.display.set_caption("Дитрис — Diana Edition")
    pygame.mixer.init()  # Инициализация звуковой системы
    clock = pygame.time.Clock()
    W, H = window.get_size()
    
    # Цвета nFactorial
    NFACT_BLUE = (13, 71, 161)
    NFACT_GREEN = (0, 230, 118)
    NFACT_ORANGE = (255, 111, 0)
    NFACT_RED = (226, 35, 26)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_BG = (20, 20, 40)
    LIGHT_GRAY = (200, 200, 200)
    GOLD = (255, 215, 0)
    PURPLE = (128, 0, 128)
    CYAN = (0, 255, 255)
    PINK = (255, 192, 203)
    
    # Музыка
    music_playing = False
    music_volume = 0.5
    def load_music():
        try:
            base = pathlib.Path(__file__).parent.resolve()
            music_path = base / "assets" / "mp3" / "detris.mp3"
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
        nonlocal music_playing
        try:
            if not music_playing:
                pygame.mixer.music.play(-1)
                music_playing = True
                print("Музыка Дитрис начала играть")
        except Exception as e:
            print(f"Ошибка при воспроизведении музыки: {e}")
    def stop_music():
        nonlocal music_playing
        try:
            pygame.mixer.music.stop()
            music_playing = False
            print("Музыка остановлена")
        except Exception as e:
            print(f"Ошибка при остановке музыки: {e}")
    def pause_music():
        nonlocal music_playing
        try:
            pygame.mixer.music.pause()
            music_playing = False
            print("Музыка поставлена на паузу")
        except Exception as e:
            print(f"Ошибка при паузе музыки: {e}")
    def unpause_music():
        nonlocal music_playing
        try:
            pygame.mixer.music.unpause()
            music_playing = True
            print("Музыка возобновлена")
        except Exception as e:
            print(f"Ошибка при возобновлении музыки: {e}")
    def set_music_volume(volume):
        nonlocal music_volume
        try:
            music_volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(music_volume)
            print(f"Громкость музыки установлена: {music_volume}")
        except Exception as e:
            print(f"Ошибка при установке громкости: {e}")
    load_music()
    play_music()
    
    # Настройки игрового поля
    GRID_WIDTH = 10
    GRID_HEIGHT = 15  # Уменьшили высоту для более быстрой игры
    BLOCK_SIZE = 35   # Увеличили размер блоков
    GRID_X = W // 2 - (GRID_WIDTH * BLOCK_SIZE) // 2
    GRID_Y = 80
    
    # Игровые настройки
    GAME_TIME = 30  # 30 секунд
    TARGET_LINES = 3  # Нужно собрать 3 линии
    
    # Загрузка ресурсов
    base = pathlib.Path(__file__).parent.resolve()
    
    # Загрузка фонового изображения аудитории
    try:
        classroom_bg = pygame.image.load(str(base / "assets" / "body.png")).convert()
        classroom_bg = pygame.transform.scale(classroom_bg, (W, H))
    except:
        # Создаем заглушку аудитории
        classroom_bg = pygame.Surface((W, H))
        # Градиент как в аудитории
        for y in range(H):
            ratio = y / H
            r = int(70 * (1 - ratio) + 120 * ratio)
            g = int(90 * (1 - ratio) + 140 * ratio)
            b = int(130 * (1 - ratio) + 180 * ratio)
            pygame.draw.line(classroom_bg, (r, g, b), (0, y), (W, y))
        
        # Добавляем элементы аудитории
        # Доска
        pygame.draw.rect(classroom_bg, (40, 60, 40), (50, 50, 300, 150))
        pygame.draw.rect(classroom_bg, WHITE, (50, 50, 300, 150), 3)
        
        # Столы
        for i in range(3):
            for j in range(4):
                table_x = 100 + j * 150
                table_y = 300 + i * 80
                pygame.draw.rect(classroom_bg, (139, 69, 19), (table_x, table_y, 120, 60))
    
    # Загрузка фото Дианы
    try:
        diana_photo = pygame.image.load(str(base / "assets" / "diana.png")).convert_alpha()
        # Масштабируем фото для блоков (увеличиваем)
        diana_block = pygame.transform.smoothscale(diana_photo, (BLOCK_SIZE, BLOCK_SIZE))
    except:
        # Создаем заглушку Дианы (больше размер)
        diana_block = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(diana_block, PINK, (BLOCK_SIZE//2, BLOCK_SIZE//2), BLOCK_SIZE//2-2)
        pygame.draw.circle(diana_block, WHITE, (BLOCK_SIZE//2, BLOCK_SIZE//2), BLOCK_SIZE//2-5)
        font_small = pygame.font.Font(None, 16)
        text = font_small.render("DIANA", True, PINK)
        diana_block.blit(text, (BLOCK_SIZE//2-15, BLOCK_SIZE//2-8))
    
    try:
        logo = pygame.image.load(str(base / "assets" / "logo.png")).convert_alpha()
        logo = pygame.transform.smoothscale(logo, (40, 40))
    except:
        logo = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(logo, NFACT_BLUE, (20, 20), 18)
        pygame.draw.circle(logo, WHITE, (20, 20), 12)
    
    # Шрифты (увеличенные для лучшей читаемости)
    try:
        font_path = str(base / "assets" / "dogica.ttf")
        font_small = pygame.font.Font(font_path, 16)    # Увеличили
        font_medium = pygame.font.Font(font_path, 22)   # Увеличили
        font_large = pygame.font.Font(font_path, 32)    # Увеличили
        font_huge = pygame.font.Font(font_path, 48)     # Увеличили
    except:
        font_small = pygame.font.Font(None, 20)
        font_medium = pygame.font.Font(None, 26)
        font_large = pygame.font.Font(None, 36)
        font_huge = pygame.font.Font(None, 52)
    
    # Дитрис фигуры (упрощенные для быстрой игры)
    DIANA_SHAPES = {
        'I': {
            'blocks': [[(0, 1), (1, 1), (2, 1), (3, 1)]],
            'color': PINK,
            'name': 'Diana Line'
        },
        'O': {
            'blocks': [[(0, 0), (1, 0), (0, 1), (1, 1)]],
            'color': NFACT_GREEN,
            'name': 'Diana Square'
        },
        'T': {
            'blocks': [[(1, 0), (0, 1), (1, 1), (2, 1)]],
            'color': NFACT_ORANGE,
            'name': 'Diana T'
        },
        'L': {
            'blocks': [[(0, 0), (0, 1), (0, 2), (1, 2)]],
            'color': NFACT_BLUE,
            'name': 'Diana L'
        }
    }
    
    # Система частиц
    class Particle:
        def __init__(self, x: float, y: float, color: Tuple[int, int, int], text: str = ""):
            self.x = x
            self.y = y
            self.color = color
            self.text = text
            self.vy = random.uniform(-4, -1)
            self.vx = random.uniform(-2, 2)
            self.life = 80
            self.max_life = 80
            self.size = random.randint(3, 6)
        
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.life -= 1
            self.size = max(1, int(self.size * (self.life / self.max_life)))
        
        def draw(self, surface):
            if self.life > 0:
                if self.text:
                    # Тень для текста частиц
                    text_shadow = font_medium.render(self.text, True, BLACK)
                    surface.blit(text_shadow, (int(self.x) + 2, int(self.y) + 2))
                    text_surface = font_medium.render(self.text, True, self.color)
                    surface.blit(text_surface, (int(self.x), int(self.y)))
                else:
                    pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
    
    class ParticleSystem:
        def __init__(self):
            self.particles = []
        
        def add_line_clear_effect(self, line_y: int):
            for i in range(GRID_WIDTH):
                x = GRID_X + i * BLOCK_SIZE + BLOCK_SIZE // 2
                y = GRID_Y + line_y * BLOCK_SIZE + BLOCK_SIZE // 2
                
                # Розовые искры для Дианы
                for _ in range(5):
                    self.particles.append(Particle(x, y, PINK))
                
                # Текстовые эффекты
                if i % 2 == 0:
                    effects = ["Diana!", "Amazing!", "Perfect!"]
                    text = random.choice(effects)
                    self.particles.append(Particle(x, y, GOLD, text))
        
        def add_diana_celebration(self, grid_center_x: int, grid_center_y: int):
            # Эпичный эффект Дианы
            for _ in range(30):
                x = grid_center_x + random.randint(-150, 150)
                y = grid_center_y + random.randint(-100, 100)
                self.particles.append(Particle(x, y, random.choice([PINK, GOLD, NFACT_GREEN])))
            
            # Специальный текст
            self.particles.append(Particle(grid_center_x - 50, grid_center_y, GOLD, "DIANA POWER!"))
        
        def update(self):
            self.particles = [p for p in self.particles if p.life > 0]
            for particle in self.particles:
                particle.update()
        
        def draw(self, surface):
            for particle in self.particles:
                particle.draw(surface)
    
    # Дитрис фигура
    class DianaTetromino:
        def __init__(self, shape_type: str):
            self.shape_type = shape_type
            self.shape_data = DIANA_SHAPES[shape_type]
            self.color = self.shape_data['color']
            self.blocks = self.shape_data['blocks'][0].copy()
            self.x = GRID_WIDTH // 2 - 2
            self.y = 0
        
        def can_move(self, dx: int, dy: int, grid):
            for bx, by in self.blocks:
                new_x = self.x + bx + dx
                new_y = self.y + by + dy
                
                # Проверка границ
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return False
                
                # Проверка столкновения с блоками
                if new_y >= 0 and grid[new_y][new_x] is not None:
                    return False
            
            return True
        
        def move(self, dx: int, dy: int, grid):
            if self.can_move(dx, dy, grid):
                self.x += dx
                self.y += dy
                return True
            return False
        
        def draw(self, surface):
            for bx, by in self.blocks:
                block_x = GRID_X + (self.x + bx) * BLOCK_SIZE
                block_y = GRID_Y + (self.y + by) * BLOCK_SIZE
                
                # Рисуем фотографию Дианы как блок
                surface.blit(diana_block, (block_x, block_y))
                
                # Добавляем рамку
                pygame.draw.rect(surface, self.color, (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE), 4)
                
                # Добавляем блеск
                highlight = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 80))
                surface.blit(highlight, (block_x, block_y))
    
    # Игровое состояние
    class DianaGameState:
        def __init__(self):
            self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            self.current_piece = None
            self.score = 0
            self.lines_cleared = 0
            self.fall_time = 0
            self.fall_speed = 800  # Медленнее для лучшего контроля
            self.game_over = False
            self.game_won = False
            self.paused = False
            
            # Таймер
            self.start_time = pygame.time.get_ticks()
            self.time_left = GAME_TIME
            
            self.spawn_piece()
        
        def spawn_piece(self):
            # Случайно выбираем фигуру
            shape = random.choice(list(DIANA_SHAPES.keys()))
            self.current_piece = DianaTetromino(shape)
            
            # Проверка game over
            if not self.current_piece.can_move(0, 0, self.grid):
                self.game_over = True
        
        def place_piece(self):
            # Размещение фигуры на поле
            for bx, by in self.current_piece.blocks:
                grid_x = self.current_piece.x + bx
                grid_y = self.current_piece.y + by
                
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    self.grid[grid_y][grid_x] = self.current_piece.color
            
            self.check_lines()
            self.spawn_piece()
        
        def check_lines(self):
            lines_to_clear = []
            
            # Найти полные линии
            for y in range(GRID_HEIGHT):
                if all(self.grid[y][x] is not None for x in range(GRID_WIDTH)):
                    lines_to_clear.append(y)
            
            if lines_to_clear:
                # Очистка линий
                for y in lines_to_clear:
                    particle_system.add_line_clear_effect(y)
                    del self.grid[y]
                    self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
                
                # Обновление счета
                lines_count = len(lines_to_clear)
                self.lines_cleared += lines_count
                self.score += lines_count * 100
                
                # Проверка победы - нужно 3 линии
                if self.lines_cleared >= TARGET_LINES:
                    self.game_won = True
                    particle_system.add_diana_celebration(
                        GRID_X + GRID_WIDTH * BLOCK_SIZE // 2,
                        GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2
                    )
        
        def update(self, dt: int):
            if self.game_over or self.game_won or self.paused:
                return
            
            # Обновление таймера
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.start_time) // 1000
            self.time_left = max(0, GAME_TIME - elapsed)
            
            # Проверка времени
            if self.time_left <= 0:
                self.game_over = True
                return
            
            self.fall_time += dt
            
            if self.fall_time >= self.fall_speed:
                if not self.current_piece.move(0, 1, self.grid):
                    self.place_piece()
                self.fall_time = 0
        
        def draw_grid(self, surface):
            # Полупрозрачная подложка для игрового поля
            grid_bg = pygame.Surface((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), pygame.SRCALPHA)
            grid_bg.fill((0, 0, 0, 150))
            surface.blit(grid_bg, (GRID_X, GRID_Y))
            
            # Сетка
            for x in range(GRID_WIDTH + 1):
                pygame.draw.line(surface, WHITE, 
                               (GRID_X + x * BLOCK_SIZE, GRID_Y), 
                               (GRID_X + x * BLOCK_SIZE, GRID_Y + GRID_HEIGHT * BLOCK_SIZE), 2)
            
            for y in range(GRID_HEIGHT + 1):
                pygame.draw.line(surface, WHITE, 
                               (GRID_X, GRID_Y + y * BLOCK_SIZE), 
                               (GRID_X + GRID_WIDTH * BLOCK_SIZE, GRID_Y + y * BLOCK_SIZE), 2)
            
            # Размещенные блоки (фотографии Дианы)
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.grid[y][x] is not None:
                        block_x = GRID_X + x * BLOCK_SIZE
                        block_y = GRID_Y + y * BLOCK_SIZE
                        
                        # Рисуем фотографию Дианы
                        surface.blit(diana_block, (block_x, block_y))
                        
                        # Рамка с цветом фигуры
                        pygame.draw.rect(surface, self.grid[y][x], 
                                       (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE), 4)
        
        def draw_ui(self, surface):
            # Основная информационная панель с улучшенной читаемостью
            info_x = 30
            info_y = 120
            
            # Большой контрастный фон для UI
            ui_bg = pygame.Surface((300, 280), pygame.SRCALPHA)
            ui_bg.fill((0, 0, 0, 240))  # Более темный фон
            surface.blit(ui_bg, (info_x - 15, info_y - 15))
            
            # Белая рамка для лучшей видимости
            pygame.draw.rect(surface, WHITE, (info_x - 15, info_y - 15, 300, 280), 4)
            
            # Заголовок с большим шрифтом
            title_text = font_large.render("DITRIS", True, PINK)
            # Тень для заголовка
            title_shadow = font_large.render("DITRIS", True, BLACK)
            surface.blit(title_shadow, (info_x + 2, info_y - 48))
            surface.blit(title_text, (info_x, info_y - 50))
            
            # Прогресс с контрастным фоном
            progress_bg = pygame.Surface((270, 35), pygame.SRCALPHA)
            progress_bg.fill((255, 255, 255, 240))  # Белый фон
            surface.blit(progress_bg, (info_x, info_y - 5))
            
            progress_text = font_medium.render(f"Lines: {self.lines_cleared}/{TARGET_LINES}", True, BLACK)
            surface.blit(progress_text, (info_x + 10, info_y + 5))
            
            # Прогресс бар (увеличиваем)
            progress_width = 260
            progress_height = 30
            progress_bg_rect = pygame.Rect(info_x, info_y + 40, progress_width, progress_height)
            pygame.draw.rect(surface, WHITE, progress_bg_rect)
            pygame.draw.rect(surface, BLACK, progress_bg_rect, 4)
            
            progress_fill = int((progress_width - 8) * (self.lines_cleared / TARGET_LINES))
            if progress_fill > 0:
                fill_rect = pygame.Rect(info_x + 4, info_y + 44, progress_fill, progress_height - 8)
                pygame.draw.rect(surface, PINK, fill_rect)
            
            # Таймер с контрастным фоном
            timer_bg = pygame.Surface((270, 35), pygame.SRCALPHA)
            timer_color = (255, 200, 200) if self.time_left <= 10 else (255, 255, 255)
            timer_bg.fill((*timer_color, 240))
            surface.blit(timer_bg, (info_x, info_y + 80))
            
            time_color = NFACT_RED if self.time_left <= 10 else BLACK
            time_text = font_medium.render(f"Time: {self.time_left}s", True, time_color)
            surface.blit(time_text, (info_x + 10, info_y + 90))
            
            # Таймер бар (увеличиваем)
            timer_width = 260
            timer_height = 25
            timer_bg_rect = pygame.Rect(info_x, info_y + 125, timer_width, timer_height)
            pygame.draw.rect(surface, WHITE, timer_bg_rect)
            pygame.draw.rect(surface, BLACK, timer_bg_rect, 4)
            
            timer_fill = int((timer_width - 8) * (self.time_left / GAME_TIME))
            if timer_fill > 0:
                timer_bar_color = NFACT_RED if self.time_left <= 10 else NFACT_GREEN
                fill_rect = pygame.Rect(info_x + 4, info_y + 129, timer_fill, timer_height - 8)
                pygame.draw.rect(surface, timer_bar_color, fill_rect)
            
            # Счет с контрастным фоном
            score_bg = pygame.Surface((270, 35), pygame.SRCALPHA)
            score_bg.fill((255, 255, 255, 240))
            surface.blit(score_bg, (info_x, info_y + 160))
            
            score_text = font_medium.render(f"Score: {self.score}", True, BLACK)
            surface.blit(score_text, (info_x + 10, info_y + 170))
            
            # Управление
            controls_x = W - 280
            controls_y = 120
            
            # Фон для управления
            controls_bg = pygame.Surface((270, 220), pygame.SRCALPHA)
            controls_bg.fill((0, 0, 0, 240))
            surface.blit(controls_bg, (controls_x - 10, controls_y - 10))
            
            # Белая рамка
            pygame.draw.rect(surface, WHITE, (controls_x - 10, controls_y - 10, 270, 220), 4)
            
            controls_title = font_medium.render("Controls:", True, NFACT_ORANGE)
            # Тень для заголовка
            title_shadow = font_medium.render("Controls:", True, BLACK)
            surface.blit(title_shadow, (controls_x + 2, controls_y + 2))
            surface.blit(controls_title, (controls_x, controls_y))
            
            controls = [
                "← → - Move",
                "↓ - Speed up", 
                "SPACE - Drop",
                "P - Pause",
                "R - Restart",
                "",
                "Goal: 3 lines",
                "in 30 seconds!"
            ]
            
            for i, control in enumerate(controls):
                if control == "":
                    continue
                    
                # Контрастный фон для каждой строки
                if control:
                    text_bg = pygame.Surface((250, 25), pygame.SRCALPHA)
                    text_bg.fill((255, 255, 255, 180))
                    surface.blit(text_bg, (controls_x, controls_y + 35 + i * 22))
                
                color = NFACT_GREEN if "Goal" in control or "seconds" in control else BLACK
                control_surface = font_small.render(control, True, color)
                surface.blit(control_surface, (controls_x + 5, controls_y + 40 + i * 22))
    
    def draw_diana_showcase(surface, game_state):
        """Красивая витрина с увеличенной фотографией Дианы"""
        showcase_x = W - 250  # Сдвигаем левее
        showcase_y = H - 300  # Увеличиваем размер
        
        # Увеличенные размеры витрины
        showcase_width = 220
        showcase_height = 250
        
        # Анимация
        time_factor = pygame.time.get_ticks() * 0.004
        pulse = math.sin(time_factor) * 0.15 + 1.0
        
        # Многослойная рамка
        for i in range(10):
            offset = int(i * pulse)
            frame_color = (255 - i*15, 192 - i*10, 203 - i*8) if i < 5 else PINK
            frame_rect = pygame.Rect(showcase_x - 15 + offset, showcase_y - 15 + offset, 
                                   showcase_width + 30 - offset*2, showcase_height + 30 - offset*2)
            pygame.draw.rect(surface, frame_color, frame_rect, 3)
        
        # Основная рамка
        main_frame = pygame.Rect(showcase_x, showcase_y, showcase_width, showcase_height)
        pygame.draw.rect(surface, BLACK, main_frame)
        pygame.draw.rect(surface, PINK, main_frame, 6)
        
        # Увеличенная фотография Дианы
        try:
            diana_display = pygame.transform.smoothscale(diana_photo, 
                                                       (showcase_width - 20, int(showcase_height * 0.75)))
        except:
            diana_display = pygame.transform.scale(diana_block, 
                                                 (showcase_width - 20, int(showcase_height * 0.75)))
        surface.blit(diana_display, (showcase_x + 10, showcase_y + 10))
        
        # Градиентный фон для текста
        text_area_height = int(showcase_height * 0.25)
        text_y = showcase_y + int(showcase_height * 0.75)
        
        text_bg = pygame.Surface((showcase_width - 20, text_area_height))
        for y in range(text_area_height):
            ratio = y / text_area_height
            r = int(PINK[0] * (1 - ratio) + BLACK[0] * ratio)
            g = int(PINK[1] * (1 - ratio) + BLACK[1] * ratio)
            b = int(PINK[2] * (1 - ratio) + BLACK[2] * ratio)
            pygame.draw.line(text_bg, (r, g, b), (0, y), (showcase_width - 20, y))
        
        surface.blit(text_bg, (showcase_x + 10, text_y))
        
        # Разделительная линия
        pygame.draw.line(surface, GOLD, (showcase_x + 10, text_y), (showcase_x + showcase_width - 10, text_y), 3)
        
        # Текст с тенями
        text_lines = [
            ("DIANA", GOLD, font_large),
            ("Queen of Tetris", PINK, font_medium)
        ]
        
        current_y = text_y + 15
        for text, color, font in text_lines:
            # Тень
            text_shadow = font.render(text, True, BLACK)
            text_shadow_rect = text_shadow.get_rect(center=(showcase_x + showcase_width//2 + 2, current_y + 2))
            surface.blit(text_shadow, text_shadow_rect)
            
            # Основной текст
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(showcase_x + showcase_width//2, current_y))
            surface.blit(text_surface, text_rect)
            current_y += 30
        
        # Эффекты при высоком прогрессе
        if game_state.lines_cleared >= 1:
            # Сердечки
            for i in range(3):
                heart_x = showcase_x + 30 + i * 50
                heart_y = showcase_y - 40
                heart_offset = math.sin(time_factor + i) * 8
                
                heart_text = font_large.render("💖", True, PINK)
                surface.blit(heart_text, (heart_x, heart_y + heart_offset))
        
        if game_state.lines_cleared >= 2:
            # Корона
            crown_text = font_huge.render("👑", True, GOLD)
            crown_rect = crown_text.get_rect(center=(showcase_x + showcase_width//2, showcase_y - 60))
            surface.blit(crown_text, crown_rect)
        
        if game_state.lines_cleared >= 3:
            # Звезды вокруг
            for i in range(8):
                angle = i * math.pi / 4 + time_factor
                star_x = showcase_x + showcase_width//2 + math.cos(angle) * 80
                star_y = showcase_y + showcase_height//2 + math.sin(angle) * 60
                
                star_text = font_large.render("⭐", True, GOLD)
                surface.blit(star_text, (star_x, star_y))
    
    # Инициализация
    game_state = DianaGameState()
    particle_system = ParticleSystem()
    
    def draw_title(surface):
        # Заголовок с эффектами
        title_bg = pygame.Surface((W, 80), pygame.SRCALPHA)
        title_bg.fill((0, 0, 0, 200))
        surface.blit(title_bg, (0, 0))
        
        # Логотип
        surface.blit(logo, (W // 2 - 250, 20))
        
        # Заголовок
        title_text = font_huge.render("DITRIS", True, PINK)
        
        
        # Тень для заголовка
        title_shadow = font_huge.render("DITRIS", True, BLACK)
        surface.blit(title_shadow, (W // 2 - 98, 22))
        surface.blit(title_text, (W // 2 - 100, 20))
        
        # Тень для подзаголовка
        subtitle_shadow = font_large.render("Diana Tetris Edition", True, BLACK)
        surface.blit(subtitle_shadow, (W // 2 - 122, 52))
       
    
    # Главный игровой цикл
    running = True
    last_time = pygame.time.get_ticks()
    
    while running:
        current_time = pygame.time.get_ticks()
        dt = current_time - last_time
        last_time = current_time
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_music()
                    return True
                if event.key == pygame.K_m:
                    if music_playing:
                        pause_music()
                    else:
                        unpause_music()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    set_music_volume(music_volume + 0.1)
                elif event.key == pygame.K_MINUS:
                    set_music_volume(music_volume - 0.1)
                
                if not game_state.game_over and not game_state.game_won:
                    if event.key == pygame.K_LEFT:
                        game_state.current_piece.move(-1, 0, game_state.grid)
                    elif event.key == pygame.K_RIGHT:
                        game_state.current_piece.move(1, 0, game_state.grid)
                    elif event.key == pygame.K_DOWN:
                        if game_state.current_piece.move(0, 1, game_state.grid):
                            game_state.score += 1
                    elif event.key == pygame.K_SPACE:
                        # Быстрый сброс
                        while game_state.current_piece.move(0, 1, game_state.grid):
                            game_state.score += 2
                        game_state.place_piece()
                    elif event.key == pygame.K_p:
                        game_state.paused = not game_state.paused
                
                if event.key == pygame.K_r:
                    # Перезапуск
                    game_state = DianaGameState()
                    particle_system = ParticleSystem()
        
        # Обновление
        game_state.update(dt)
        particle_system.update()
        
        # Отрисовка
        # Фон аудитории
        window.blit(classroom_bg, (0, 0))
        
        # Затемнение для лучшей видимости игрового поля
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        window.blit(overlay, (0, 0))
        
        draw_title(window)
        draw_diana_showcase(window, game_state)
        
        # Игровое поле
        game_state.draw_grid(window)
        
        # Текущая фигура
        if game_state.current_piece and not game_state.game_over and not game_state.game_won:
            game_state.current_piece.draw(window)
        
        # Интерфейс
        game_state.draw_ui(window)
        
        # Частицы
        particle_system.draw(window)
        
        # Подсказка о клавише ESC с контрастным фоном
        esc_hint = font_medium.render("ESC - Back to menu", True, WHITE)
        hint_bg = pygame.Surface((esc_hint.get_width() + 20, 30), pygame.SRCALPHA)
        hint_bg.fill((0, 0, 0, 200))
        window.blit(hint_bg, (W - esc_hint.get_width() - 30, H - 40))
        pygame.draw.rect(window, WHITE, (W - esc_hint.get_width() - 30, H - 40, esc_hint.get_width() + 20, 30), 2)
        window.blit(esc_hint, (W - esc_hint.get_width() - 20, H - 35))
        
        # Пауза
        if game_state.paused:
            pause_overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 200))
            window.blit(pause_overlay, (0, 0))
            
            # Тень для текста паузы
            pause_shadow = font_huge.render("PAUSED", True, BLACK)
            pause_text = font_huge.render("PAUSED", True, NFACT_ORANGE)
            pause_rect = pause_text.get_rect(center=(W // 2, H // 2))
            window.blit(pause_shadow, (pause_rect.x + 3, pause_rect.y + 3))
            window.blit(pause_text, pause_rect)
            
            # Тень для инструкции
            resume_shadow = font_large.render("Press P to continue", True, BLACK)
            resume_text = font_large.render("Press P to continue", True, WHITE)
            resume_rect = resume_text.get_rect(center=(W // 2, H // 2 + 60))
            window.blit(resume_shadow, (resume_rect.x + 2, resume_rect.y + 2))
            window.blit(resume_text, resume_rect)
        
        # Победа
        if game_state.game_won:
            victory_overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            victory_overlay.fill((0, 0, 0, 220))
            window.blit(victory_overlay, (0, 0))
            
            # Большая фотография Дианы для победы
            try:
                victory_diana = pygame.transform.smoothscale(diana_photo, (250, 300))
            except:
                victory_diana = pygame.transform.scale(diana_block, (250, 300))
            
            diana_rect = victory_diana.get_rect(center=(W // 2, H // 2 - 120))
            
            # Рамка вокруг фото победы
            frame_rect = pygame.Rect(diana_rect.x - 10, diana_rect.y - 10, diana_rect.width + 20, diana_rect.height + 20)
            pygame.draw.rect(window, GOLD, frame_rect, 8)
            window.blit(victory_diana, diana_rect)
            
            # Корона над Дианой
            crown_text = font_huge.render("👑", True, GOLD)
            crown_rect = crown_text.get_rect(center=(W // 2, H // 2 - 250))
            window.blit(crown_text, crown_rect)
            
            # Текст победы с тенью
            victory_shadow = font_huge.render("DIANA WINS!", True, BLACK)
            victory_text = font_huge.render("DIANA WINS!", True, PINK)
            victory_rect = victory_text.get_rect(center=(W // 2, H // 2 + 120))
            window.blit(victory_shadow, (victory_rect.x + 3, victory_rect.y + 3))
            window.blit(victory_text, victory_rect)
            
            stats_text = [
                f"3 lines cleared in {GAME_TIME - game_state.time_left} seconds!",
                f"Final score: {game_state.score}",
                "Diana -Queen of Tetris! 💖"
            ]
            
            for i, stat in enumerate(stats_text):
                color = GOLD if i == 2 else WHITE
                # Тень для статистики
                stat_shadow = font_large.render(stat, True, BLACK)
                stat_surface = font_large.render(stat, True, color)
                stat_rect = stat_surface.get_rect(center=(W // 2, H // 2 + 160 + i * 35))
                window.blit(stat_shadow, (stat_rect.x + 2, stat_rect.y + 2))
                window.blit(stat_surface, stat_rect)
            
            # Инструкции с контрастным фоном
            restart_text = font_large.render("R - play again | ESC - exit", True, WHITE)
            restart_bg = pygame.Surface((restart_text.get_width() + 20, 40), pygame.SRCALPHA)
            restart_bg.fill((0, 0, 0, 180))
            restart_rect = restart_text.get_rect(center=(W // 2, H // 2 + 280))
            window.blit(restart_bg, (restart_rect.x - 10, restart_rect.y - 5))
            pygame.draw.rect(window, WHITE, (restart_rect.x - 10, restart_rect.y - 5, restart_text.get_width() + 20, 40), 2)
            window.blit(restart_text, restart_rect)
            
            # Конфетти вокруг Дианы
            for i in range(20):
                confetti_x = W // 2 + random.randint(-250, 250)
                confetti_y = H // 2 + random.randint(-200, 200)
                confetti_color = random.choice([PINK, GOLD, NFACT_GREEN, NFACT_ORANGE])
                
                offset = math.sin(pygame.time.get_ticks() * 0.01 + i) * 8
                pygame.draw.rect(window, confetti_color, 
                               (confetti_x + offset, confetti_y, 8, 15))
        
        # Поражение
        if game_state.game_over and not game_state.game_won:
            game_over_overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            game_over_overlay.fill((0, 0, 0, 220))
            window.blit(game_over_overlay, (0, 0))
            
            # Грустная Диана
            try:
                sad_diana = pygame.transform.smoothscale(diana_photo, (200, 250))
                # Применяем серый фильтр
                gray_diana = pygame.Surface((200, 250), pygame.SRCALPHA)
                gray_diana.blit(sad_diana, (0, 0))
                gray_overlay = pygame.Surface((200, 250), pygame.SRCALPHA)
                gray_overlay.fill((120, 120, 120, 120))
                gray_diana.blit(gray_overlay, (0, 0))
            except:
                gray_diana = pygame.transform.scale(diana_block, (200, 250))
            
            diana_rect = gray_diana.get_rect(center=(W // 2, H // 2 - 100))
            
            # Рамка вокруг грустной Дианы
            frame_rect = pygame.Rect(diana_rect.x - 8, diana_rect.y - 8, diana_rect.width + 16, diana_rect.height + 16)
            pygame.draw.rect(window, LIGHT_GRAY, frame_rect, 6)
            window.blit(gray_diana, diana_rect)
            
            # Текст поражения с тенью
            game_over_shadow = font_huge.render("TIME'S UP!", True, BLACK)
            game_over_text = font_huge.render("TIME'S UP!", True, NFACT_RED)
            game_over_rect = game_over_text.get_rect(center=(W // 2, H // 2 + 100))
            window.blit(game_over_shadow, (game_over_rect.x + 3, game_over_rect.y + 3))
            window.blit(game_over_text, game_over_rect)
            
            # Результат с тенью
            result_shadow = font_large.render(f"Lines cleared: {game_state.lines_cleared}/3", True, BLACK)
            result_text = font_large.render(f"Lines cleared: {game_state.lines_cleared}/3", True, WHITE)
            result_rect = result_text.get_rect(center=(W // 2, H // 2 + 150))
            window.blit(result_shadow, (result_rect.x + 2, result_rect.y + 2))
            window.blit(result_text, result_rect)
            
            # Ободряющий текст
            if game_state.lines_cleared > 0:
                encourage_msg = "Good result! Try again!"
                encourage_color = NFACT_GREEN
            else:
                encourage_msg = "Diana believes in you! Try again!"
                encourage_color = PINK
            
            encourage_shadow = font_large.render(encourage_msg, True, BLACK)
            encourage_text = font_large.render(encourage_msg, True, encourage_color)
            encourage_rect = encourage_text.get_rect(center=(W // 2, H // 2 + 190))
            window.blit(encourage_shadow, (encourage_rect.x + 2, encourage_rect.y + 2))
            window.blit(encourage_text, encourage_rect)
            
            # Инструкции с контрастным фоном
            restart_text = font_large.render("R - try again | ESC - exit", True, WHITE)
            restart_bg = pygame.Surface((restart_text.get_width() + 20, 40), pygame.SRCALPHA)
            restart_bg.fill((0, 0, 0, 180))
            restart_rect = restart_text.get_rect(center=(W // 2, H // 2 + 240))
            window.blit(restart_bg, (restart_rect.x - 10, restart_rect.y - 5))
            pygame.draw.rect(window, WHITE, (restart_rect.x - 10, restart_rect.y - 5, restart_text.get_width() + 20, 40), 2)
            window.blit(restart_text, restart_rect)
        
        # Мигающее предупреждение при малом времени
        if game_state.time_left <= 10 and game_state.time_left > 0 and not game_state.game_won and not game_state.paused:
            if (pygame.time.get_ticks() // 500) % 2:  # Мигание каждые 0.5 сек
                warning_text = font_huge.render(f"{game_state.time_left} SECONDS LEFT!", True, NFACT_RED)
                warning_rect = warning_text.get_rect(center=(W // 2, 120))
                
                # Контрастный фон для предупреждения
                warning_bg = pygame.Surface((warning_text.get_width() + 30, warning_text.get_height() + 20), pygame.SRCALPHA)
                warning_bg.fill((255, 0, 0, 150))
                window.blit(warning_bg, (warning_rect.x - 15, warning_rect.y - 10))
                pygame.draw.rect(window, WHITE, (warning_rect.x - 15, warning_rect.y - 10, warning_text.get_width() + 30, warning_text.get_height() + 20), 4)
                
                # Тень для предупреждения
                warning_shadow = font_huge.render(f"{game_state.time_left} SECONDS LEFT!", True, BLACK)
                window.blit(warning_shadow, (warning_rect.x + 3, warning_rect.y + 3))
                window.blit(warning_text, warning_rect)
        
        # Показываем цель игры в начале
        if game_state.time_left > 25 and game_state.lines_cleared == 0 and not game_state.paused:
            goal_text = font_large.render("Clear 3 lines in 30 seconds!", True, GOLD)
            goal_rect = goal_text.get_rect(center=(W // 2, H - 80))
            
            # Контрастный фон для цели
            goal_bg = pygame.Surface((goal_text.get_width() + 30, goal_text.get_height() + 20), pygame.SRCALPHA)
            goal_bg.fill((0, 0, 0, 180))
            window.blit(goal_bg, (goal_rect.x - 15, goal_rect.y - 10))
            pygame.draw.rect(window, GOLD, (goal_rect.x - 15, goal_rect.y - 10, goal_text.get_width() + 30, goal_text.get_height() + 20), 3)
            
            # Тень для цели
            goal_shadow = font_large.render("Goal: Clear 3 lines in 30 seconds with Diana!", True, BLACK)
            window.blit(goal_shadow, (goal_rect.x + 2, goal_rect.y + 2))
            window.blit(goal_text, goal_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return False


# Главная функция для запуска игры
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    main(screen)
    pygame.quit()