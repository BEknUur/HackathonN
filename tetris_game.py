import pygame
import random
import math
import time
import pathlib
from typing import List, Tuple, Optional

def main(window):
    """
    nFactorial Tetris - Code Block Edition
    Собирай блоки кода в правильном порядке!
    """
    pygame.display.set_caption("nFactorial Tetris — Code Block Edition")
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
    
    # Настройки игрового поля
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    BLOCK_SIZE = 30
    GRID_X = W // 2 - (GRID_WIDTH * BLOCK_SIZE) // 2
    GRID_Y = 50
    
    # Загрузка ресурсов
    base = pathlib.Path(__file__).parent.resolve()
    try:
        logo = pygame.image.load(str(base / "assets" / "logo.png")).convert_alpha()
        logo = pygame.transform.smoothscale(logo, (40, 40))
    except:
        logo = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(logo, NFACT_BLUE, (20, 20), 18)
        pygame.draw.circle(logo, WHITE, (20, 20), 12)
    
    # Шрифты
    try:
        font_path = str(base / "assets" / "dogica.ttf")
        font_small = pygame.font.Font(font_path, 12)
        font_medium = pygame.font.Font(font_path, 16)
        font_large = pygame.font.Font(font_path, 24)
        font_huge = pygame.font.Font(font_path, 36)
    except:
        font_small = pygame.font.Font(None, 16)
        font_medium = pygame.font.Font(None, 20)
        font_large = pygame.font.Font(None, 28)
        font_huge = pygame.font.Font(None, 40)
    
    # Тетрис фигуры с nFactorial тематикой
    TETRIS_SHAPES = {
        'I': {
            'blocks': [[(0, 1), (1, 1), (2, 1), (3, 1)]],
            'color': NFACT_BLUE,
            'name': 'def function():',
            'icon': 'def'
        },
        'O': {
            'blocks': [[(0, 0), (1, 0), (0, 1), (1, 1)]],
            'color': GOLD,
            'name': 'class Object:',
            'icon': '{}'
        },
        'T': {
            'blocks': [[(1, 0), (0, 1), (1, 1), (2, 1)]],
            'color': PURPLE,
            'name': 'try/except',
            'icon': 'try'
        },
        'S': {
            'blocks': [[(1, 0), (2, 0), (0, 1), (1, 1)]],
            'color': NFACT_GREEN,
            'name': 'if condition:',
            'icon': 'if'
        },
        'Z': {
            'blocks': [[(0, 0), (1, 0), (1, 1), (2, 1)]],
            'color': NFACT_RED,
            'name': 'for loop:',
            'icon': 'for'
        },
        'J': {
            'blocks': [[(0, 0), (0, 1), (1, 1), (2, 1)]],
            'color': NFACT_ORANGE,
            'name': 'while True:',
            'icon': 'while'
        },
        'L': {
            'blocks': [[(2, 0), (0, 1), (1, 1), (2, 1)]],
            'color': CYAN,
            'name': 'import module',
            'icon': 'import'
        }
    }
    
    # Система частиц
    class Particle:
        def __init__(self, x: float, y: float, color: Tuple[int, int, int], text: str = ""):
            self.x = x
            self.y = y
            self.color = color
            self.text = text
            self.vy = random.uniform(-3, -1)
            self.vx = random.uniform(-1, 1)
            self.life = 60
            self.max_life = 60
            self.size = random.randint(2, 5)
        
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.life -= 1
            self.size = max(1, int(self.size * (self.life / self.max_life)))
        
        def draw(self, surface):
            if self.life > 0:
                if self.text:
                    text_surface = font_small.render(self.text, True, self.color)
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
                
                # Искры
                for _ in range(3):
                    self.particles.append(Particle(x, y, GOLD))
                
                # Текстовые эффекты
                if i % 3 == 0:
                    effects = ["Bug Fixed!", "Clean Code!", "Refactored!"]
                    text = random.choice(effects)
                    self.particles.append(Particle(x, y, NFACT_GREEN, text))
        
        def add_tetris_effect(self, grid_center_x: int, grid_center_y: int):
            # Эпичный эффект тетриса
            for _ in range(20):
                x = grid_center_x + random.randint(-100, 100)
                y = grid_center_y + random.randint(-50, 50)
                self.particles.append(Particle(x, y, random.choice([GOLD, NFACT_ORANGE, NFACT_GREEN])))
            
            # Текст "TETRIS!"
            self.particles.append(Particle(grid_center_x, grid_center_y, GOLD, "TETRIS!"))
        
        def update(self):
            self.particles = [p for p in self.particles if p.life > 0]
            for particle in self.particles:
                particle.update()
        
        def draw(self, surface):
            for particle in self.particles:
                particle.draw(surface)
    
    # Тетрис фигура
    class Tetromino:
        def __init__(self, shape_type: str):
            self.shape_type = shape_type
            self.shape_data = TETRIS_SHAPES[shape_type]
            self.color = self.shape_data['color']
            self.blocks = self.shape_data['blocks'][0].copy()
            self.x = GRID_WIDTH // 2 - 2
            self.y = 0
            self.rotation = 0
        
        def get_rotated_blocks(self):
            # Поворот фигуры
            rotated = []
            for bx, by in self.blocks:
                # Поворот на 90 градусов
                new_x = -by
                new_y = bx
                rotated.append((new_x, new_y))
            return rotated
        
        def can_move(self, dx: int, dy: int, grid, rotated_blocks=None):
            blocks_to_check = rotated_blocks if rotated_blocks else self.blocks
            
            for bx, by in blocks_to_check:
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
        
        def rotate(self, grid):
            rotated_blocks = self.get_rotated_blocks()
            if self.can_move(0, 0, grid, rotated_blocks):
                self.blocks = rotated_blocks
                return True
            return False
        
        def draw(self, surface, preview=False):
            for bx, by in self.blocks:
                block_x = GRID_X + (self.x + bx) * BLOCK_SIZE
                block_y = GRID_Y + (self.y + by) * BLOCK_SIZE
                
                if preview:
                    # Превью с прозрачностью
                    preview_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                    preview_surface.fill((*self.color, 100))
                    surface.blit(preview_surface, (block_x, block_y))
                else:
                    # Обычный блок
                    pygame.draw.rect(surface, self.color, (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, WHITE, (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE), 2)
                    
                    # Иконка кода
                    icon = self.shape_data['icon']
                    icon_surface = font_small.render(icon, True, BLACK)
                    icon_rect = icon_surface.get_rect(center=(block_x + BLOCK_SIZE//2, block_y + BLOCK_SIZE//2))
                    surface.blit(icon_surface, icon_rect)
    
    # Игровое состояние
    class GameState:
        def __init__(self):
            self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            self.current_piece = None
            self.next_piece = None
            self.score = 0
            self.lines_cleared = 0
            self.level = 1
            self.fall_time = 0
            self.fall_speed = 500  # миллисекунды
            self.game_over = False
            self.paused = False
            
            # Статистика
            self.pieces_placed = 0
            self.tetrises = 0
            self.combo = 0
            
            self.spawn_piece()
        
        def spawn_piece(self):
            if self.next_piece is None:
                self.next_piece = Tetromino(random.choice(list(TETRIS_SHAPES.keys())))
            
            self.current_piece = self.next_piece
            self.next_piece = Tetromino(random.choice(list(TETRIS_SHAPES.keys())))
            
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
            
            self.pieces_placed += 1
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
                self.combo += 1
                
                # Очки за линии
                line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
                base_score = line_scores.get(lines_count, 100)
                combo_bonus = self.combo * 50
                level_bonus = self.level * 10
                
                self.score += base_score + combo_bonus + level_bonus
                
                # Проверка тетриса
                if lines_count == 4:
                    self.tetrises += 1
                    particle_system.add_tetris_effect(
                        GRID_X + GRID_WIDTH * BLOCK_SIZE // 2,
                        GRID_Y + GRID_HEIGHT * BLOCK_SIZE // 2
                    )
                
                # Увеличение уровня
                new_level = self.lines_cleared // 10 + 1
                if new_level > self.level:
                    self.level = new_level
                    self.fall_speed = max(50, self.fall_speed - 50)
            else:
                self.combo = 0
        
        def update(self, dt: int):
            if self.game_over or self.paused:
                return
            
            self.fall_time += dt
            
            if self.fall_time >= self.fall_speed:
                if not self.current_piece.move(0, 1, self.grid):
                    self.place_piece()
                self.fall_time = 0
        
        def draw_grid(self, surface):
            # Сетка
            for x in range(GRID_WIDTH + 1):
                pygame.draw.line(surface, LIGHT_GRAY, 
                               (GRID_X + x * BLOCK_SIZE, GRID_Y), 
                               (GRID_X + x * BLOCK_SIZE, GRID_Y + GRID_HEIGHT * BLOCK_SIZE))
            
            for y in range(GRID_HEIGHT + 1):
                pygame.draw.line(surface, LIGHT_GRAY, 
                               (GRID_X, GRID_Y + y * BLOCK_SIZE), 
                               (GRID_X + GRID_WIDTH * BLOCK_SIZE, GRID_Y + y * BLOCK_SIZE))
            
            # Размещенные блоки
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.grid[y][x] is not None:
                        block_x = GRID_X + x * BLOCK_SIZE
                        block_y = GRID_Y + y * BLOCK_SIZE
                        
                        pygame.draw.rect(surface, self.grid[y][x], 
                                       (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(surface, WHITE, 
                                       (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE), 2)
        
        def draw_ui(self, surface):
            # Панель информации
            info_x = 50
            info_y = 100
            
            # Счет
            score_text = font_medium.render(f"Score: {self.score}", True, WHITE)
            surface.blit(score_text, (info_x, info_y))
            
            # Линии
            lines_text = font_medium.render(f"Lines: {self.lines_cleared}", True, WHITE)
            surface.blit(lines_text, (info_x, info_y + 30))
            
            # Уровень
            level_text = font_medium.render(f"Level: {self.level}", True, WHITE)
            surface.blit(level_text, (info_x, info_y + 60))
            
            # Комбо
            if self.combo > 0:
                combo_text = font_medium.render(f"Combo: {self.combo}", True, NFACT_ORANGE)
                surface.blit(combo_text, (info_x, info_y + 90))
            
            # Статистика
            stats_y = info_y + 140
            stats_text = [
                f"Pieces: {self.pieces_placed}",
                f"Tetrises: {self.tetrises}",
                f"Speed: {1000//self.fall_speed:.1f}/s"
            ]
            
            for i, stat in enumerate(stats_text):
                stat_surface = font_small.render(stat, True, LIGHT_GRAY)
                surface.blit(stat_surface, (info_x, stats_y + i * 20))
            
            # Следующая фигура
            next_x = W - 200
            next_y = 100
            
            next_title = font_medium.render("Next:", True, WHITE)
            surface.blit(next_title, (next_x, next_y))
            
            if self.next_piece:
                # Фон для следующей фигуры
                preview_bg = pygame.Rect(next_x, next_y + 30, 120, 120)
                pygame.draw.rect(surface, (50, 50, 50), preview_bg)
                pygame.draw.rect(surface, WHITE, preview_bg, 2)
                
                # Отрисовка следующей фигуры
                temp_x = self.next_piece.x
                temp_y = self.next_piece.y
                
                self.next_piece.x = (next_x - GRID_X) // BLOCK_SIZE + 1
                self.next_piece.y = (next_y + 50 - GRID_Y) // BLOCK_SIZE + 1
                
                self.next_piece.draw(surface)
                
                self.next_piece.x = temp_x
                self.next_piece.y = temp_y
                
                # Название фигуры
                name_text = font_small.render(self.next_piece.shape_data['name'], True, self.next_piece.color)
                surface.blit(name_text, (next_x, next_y + 160))
            
            # Управление
            controls_y = next_y + 220
            controls = [
                "← → - Move",
                "↓ - Soft Drop",
                "↑ - Rotate",
                "Space - Hard Drop",
                "P - Pause",
                "R - Restart"
            ]
            
            controls_title = font_medium.render("Controls:", True, WHITE)
            surface.blit(controls_title, (next_x, controls_y))
            
            for i, control in enumerate(controls):
                control_surface = font_small.render(control, True, LIGHT_GRAY)
                surface.blit(control_surface, (next_x, controls_y + 30 + i * 18))
    
    # Инициализация
    game_state = GameState()
    particle_system = ParticleSystem()
    
    def draw_gradient_background(surface):
        for y in range(H):
            ratio = y / H
            r = int(DARK_BG[0] * (1 - ratio) + NFACT_BLUE[0] * ratio * 0.1)
            g = int(DARK_BG[1] * (1 - ratio) + NFACT_BLUE[1] * ratio * 0.1)
            b = int(DARK_BG[2] * (1 - ratio) + NFACT_BLUE[2] * ratio * 0.2)
            pygame.draw.line(surface, (r, g, b), (0, y), (W, y))
    
    def draw_title(surface):
        title_text = font_large.render("nFactorial Tetris", True, NFACT_BLUE)
        subtitle_text = font_medium.render("Code Block Edition", True, NFACT_GREEN)
        
        surface.blit(logo, (W // 2 - 100, 10))
        surface.blit(title_text, (W // 2 - 120, 10))
        surface.blit(subtitle_text, (W // 2 - 80, 35))
    
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
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                
                if not game_state.game_over:
                    if event.key == pygame.K_LEFT:
                        game_state.current_piece.move(-1, 0, game_state.grid)
                    elif event.key == pygame.K_RIGHT:
                        game_state.current_piece.move(1, 0, game_state.grid)
                    elif event.key == pygame.K_DOWN:
                        if game_state.current_piece.move(0, 1, game_state.grid):
                            game_state.score += 1
                    elif event.key == pygame.K_UP:
                        game_state.current_piece.rotate(game_state.grid)
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        while game_state.current_piece.move(0, 1, game_state.grid):
                            game_state.score += 2
                        game_state.place_piece()
                    elif event.key == pygame.K_p:
                        game_state.paused = not game_state.paused
                
                if event.key == pygame.K_r:
                    # Restart
                    game_state = GameState()
                    particle_system = ParticleSystem()
        
        # Обновление
        game_state.update(dt)
        particle_system.update()
        
        # Отрисовка
        draw_gradient_background(window)
        draw_title(window)
        
        # Игровое поле
        game_state.draw_grid(window)
        
        # Текущая фигура
        if game_state.current_piece and not game_state.game_over:
            game_state.current_piece.draw(window)
        
        # Интерфейс
        game_state.draw_ui(window)
        
        # Частицы
        particle_system.draw(window)
        
        # Пауза
        if game_state.paused:
            pause_overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 150))
            window.blit(pause_overlay, (0, 0))
            
            pause_text = font_huge.render("PAUSED", True, NFACT_ORANGE)
            pause_rect = pause_text.get_rect(center=(W // 2, H // 2))
            window.blit(pause_text, pause_rect)
            
            resume_text = font_medium.render("Press P to resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(W // 2, H // 2 + 50))
            window.blit(resume_text, resume_rect)
        
        # Game Over
        if game_state.game_over:
            game_over_overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            game_over_overlay.fill((0, 0, 0, 180))
            window.blit(game_over_overlay, (0, 0))
            
            game_over_text = font_huge.render("GAME OVER", True, NFACT_RED)
            game_over_rect = game_over_text.get_rect(center=(W // 2, H // 2 - 100))
            window.blit(game_over_text, game_over_rect)
            
            final_score_text = font_large.render(f"Final Score: {game_state.score}", True, GOLD)
            final_score_rect = final_score_text.get_rect(center=(W // 2, H // 2 - 50))
            window.blit(final_score_text, final_score_rect)
            
            stats_text = [
                f"Lines Cleared: {game_state.lines_cleared}",
                f"Level Reached: {game_state.level}",
                f"Pieces Placed: {game_state.pieces_placed}",
                f"Tetrises: {game_state.tetrises}"
            ]
            
            for i, stat in enumerate(stats_text):
                stat_surface = font_medium.render(stat, True, WHITE)
                stat_rect = stat_surface.get_rect(center=(W // 2, H // 2 + i * 30))
                window.blit(stat_surface, stat_rect)
            
            restart_text = font_medium.render("Press R to restart or ESC to exit", True, LIGHT_GRAY)
            restart_rect = restart_text.get_rect(center=(W // 2, H // 2 + 150))
            window.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return False