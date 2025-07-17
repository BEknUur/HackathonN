import pygame
import sys
import time
import pathlib
import math
import random
from typing import List, Tuple, Optional

# Импорт игр
import sleep_game
import runner_game
import quiz_game
import incubator_game
import tetris_game

# Инициализация
pygame.init()
path = pathlib.Path(__file__).parent.resolve()

# Настройки окна
WINDOW_SIZE = (1280, 720)
window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
center_x = WINDOW_SIZE[0] // 2
center_y = WINDOW_SIZE[1] // 2

# Цвета nFactorial
NFACT_BLUE = (13, 71, 161)
NFACT_GREEN = (0, 230, 118)
NFACT_ORANGE = (255, 111, 0)
NFACT_RED = (226, 35, 26)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BG = (15, 15, 35)
LIGHT_GRAY = (200, 200, 200)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)

# Загрузка ресурсов
def load_resources():
    global bg, logo, title_font, menu_font, subtitle_font, info_font
    
    # Фон
    try:
        bg = pygame.image.load(str(path / "assets" / "menu.jpg")).convert()
        bg = pygame.transform.scale(bg, WINDOW_SIZE)
    except:
        # Создаем эпичный градиентный фон
        bg = pygame.Surface(WINDOW_SIZE)
        for y in range(WINDOW_SIZE[1]):
            ratio = y / WINDOW_SIZE[1]
            # Многоцветный градиент
            r = int(DARK_BG[0] * (1 - ratio) + NFACT_BLUE[0] * ratio * 0.2 + NFACT_GREEN[0] * math.sin(ratio * 3.14) * 0.1)
            g = int(DARK_BG[1] * (1 - ratio) + NFACT_BLUE[1] * ratio * 0.2 + NFACT_GREEN[1] * math.sin(ratio * 3.14) * 0.1)
            b = int(DARK_BG[2] * (1 - ratio) + NFACT_BLUE[2] * ratio * 0.3 + NFACT_GREEN[2] * math.sin(ratio * 3.14) * 0.1)
            pygame.draw.line(bg, (r, g, b), (0, y), (WINDOW_SIZE[0], y))
    
    # Логотип
    try:
        logo = pygame.image.load(str(path / "assets" / "logo.png")).convert_alpha()
        logo = pygame.transform.smoothscale(logo, (120, 120))
    except:
        # Создаем эпичный логотип
        logo = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(logo, NFACT_BLUE, (60, 60), 58)
        pygame.draw.circle(logo, WHITE, (60, 60), 45)
        pygame.draw.circle(logo, NFACT_GREEN, (60, 60), 35)
        pygame.draw.circle(logo, NFACT_ORANGE, (60, 60), 25)
        font_logo = pygame.font.Font(None, 24)
        text = font_logo.render("nF", True, WHITE)
        logo.blit(text, (52, 52))
    
    # Шрифты - увеличиваем размеры для лучшей читаемости
    try:
        dogica_path = str(path / "assets" / "dogica.ttf")
        title_font = pygame.font.Font(dogica_path, 84)      # Было 72
        menu_font = pygame.font.Font(dogica_path, 42)       # Было 32
        subtitle_font = pygame.font.Font(dogica_path, 28)   # Было 20
        info_font = pygame.font.Font(dogica_path, 22)       # Было 16
    except:
        title_font = pygame.font.Font(None, 96)       # Было 80
        menu_font = pygame.font.Font(None, 48)        # Было 38
        subtitle_font = pygame.font.Font(None, 32)    # Было 24
        info_font = pygame.font.Font(None, 28)        # Было 20

# Система частиц
class Particle:
    def __init__(self, x: float, y: float, vx: float, vy: float, color: Tuple[int, int, int], size: int = 2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = 120
        self.max_life = 120
        self.rotation = 0
        self.rotation_speed = random.uniform(-0.1, 0.1)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # Гравитация
        self.vx *= 0.99  # Трение
        self.life -= 1
        self.rotation += self.rotation_speed
        
        # Отскок от границ
        if self.x <= 0 or self.x >= WINDOW_SIZE[0]:
            self.vx *= -0.8
        if self.y >= WINDOW_SIZE[1]:
            self.vy *= -0.8
            self.y = WINDOW_SIZE[1] - 1
    
    def draw(self, surface):
        if self.life > 0:
            alpha = self.life / self.max_life
            current_size = max(1, int(self.size * alpha))
            
            # Рисуем звездочку вместо круга
            if current_size > 2:
                points = []
                for i in range(5):
                    angle = i * 2 * math.pi / 5 + self.rotation
                    outer_x = self.x + math.cos(angle) * current_size
                    outer_y = self.y + math.sin(angle) * current_size
                    points.append((outer_x, outer_y))
                    
                    angle += math.pi / 5
                    inner_x = self.x + math.cos(angle) * current_size * 0.5
                    inner_y = self.y + math.sin(angle) * current_size * 0.5
                    points.append((inner_x, inner_y))
                
                try:
                    pygame.draw.polygon(surface, self.color, points)
                except:
                    pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), current_size)
            else:
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), current_size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.spawn_timer = 0
        self.fireworks_timer = 0
    
    def add_particles(self, x: float, y: float, count: int = 5, color: Tuple[int, int, int] = NFACT_GREEN):
        for _ in range(count):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-5, -1)
            size = random.randint(1, 4)
            self.particles.append(Particle(x, y, vx, vy, color, size))
    
    def add_firework(self, x: float, y: float):
        colors = [NFACT_BLUE, NFACT_GREEN, NFACT_ORANGE, NFACT_RED, GOLD, PURPLE]
        color = random.choice(colors)
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.randint(2, 5)
            self.particles.append(Particle(x, y, vx, vy, color, size))
    
    def update(self):
        # Обновление частиц
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
        # Спавн новых частиц
        self.spawn_timer += 1
        if self.spawn_timer >= 60:
            self.spawn_timer = 0
            x = random.randint(0, WINDOW_SIZE[0])
            y = random.randint(0, WINDOW_SIZE[1] // 3)
            self.add_particles(x, y, 1, random.choice([NFACT_BLUE, NFACT_GREEN, NFACT_ORANGE]))
        
        # Случайные фейерверки
        self.fireworks_timer += 1
        if self.fireworks_timer >= 300:  # Каждые 5 секунд
            self.fireworks_timer = 0
            if random.random() < 0.3:  # 30% шанс
                x = random.randint(100, WINDOW_SIZE[0] - 100)
                y = random.randint(100, WINDOW_SIZE[1] // 2)
                self.add_firework(x, y)
    
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

# Элемент меню
class MenuItem:
    def __init__(self, text: str, action, y_pos: int, description: str = "", icon: str = ""):
        self.text = text
        self.action = action
        self.target_y = y_pos
        self.current_y = y_pos + 100
        self.description = description
        self.icon = icon
        self.selected = False
        self.hover_scale = 1.0
        self.glow_intensity = 0
        self.particle_timer = 0
        self.pulse = 0
    
    def update(self):
        # Убираем все анимации, только плавное движение к позиции
        self.current_y += (self.target_y - self.current_y) * 0.2
    
    def draw(self, surface, particle_system):
        # Пульсирующий эффект
        pulse_offset = int(math.sin(self.pulse) * 5)
        
        # Эффект свечения
        if self.glow_intensity > 0:
            glow_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
            glow_surface.fill((0, 0, 0, 0))
            
            # Градиентное свечение
            glow_color = NFACT_ORANGE if self.selected else NFACT_BLUE
            for i in range(5):
                alpha = int(self.glow_intensity * (1 - i/5))
                pygame.draw.ellipse(glow_surface, (*glow_color, alpha), 
                                  (i*20, i*10, 700-i*40, 100-i*20))
            
            surface.blit(glow_surface, (center_x - 350, self.current_y - 50 + pulse_offset))
        
        # Темный фон для текста - для лучшей читаемости
        text_bg_width = 500
        text_bg_height = 60
        text_bg = pygame.Surface((text_bg_width, text_bg_height), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 180))  # Полупрозрачный черный
        text_bg_rect = text_bg.get_rect(center=(center_x, self.current_y + pulse_offset))
        surface.blit(text_bg, text_bg_rect)
        
        # Дополнительная рамка для выделения
        if self.selected:
            pygame.draw.rect(surface, NFACT_ORANGE, text_bg_rect, 3)
        
        # Иконка
        if self.icon:
            icon_surface = menu_font.render(self.icon, True, GOLD if self.selected else WHITE)
            surface.blit(icon_surface, (center_x - 200, self.current_y - 15 + pulse_offset))
        
        # Основной текст с тенью для лучшей читаемости
        color = GOLD if self.selected else WHITE
        scale = self.hover_scale
        
        # Создаем увеличенный шрифт если выбран
        if scale > 1.0:
            font_size = int(32 * scale)
            try:
                scaled_font = pygame.font.Font(str(path / "assets" / "dogica.ttf"), font_size)
            except:
                scaled_font = pygame.font.Font(None, int(38 * scale))
        else:
            scaled_font = menu_font
        
        # Тень текста
        shadow_surface = scaled_font.render(self.text, True, BLACK)
        shadow_rect = shadow_surface.get_rect(center=(center_x + 2, self.current_y + pulse_offset + 2))
        surface.blit(shadow_surface, shadow_rect)
        
        # Основной текст
        text_surface = scaled_font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=(center_x, self.current_y + pulse_offset))
        surface.blit(text_surface, text_rect)
        
        # Анимированная стрелка
        if self.selected:
            arrow_x = text_rect.left - 80
            arrow_y = self.current_y + pulse_offset
            
            # Двойная стрелка с эффектом
            offset1 = int(math.sin(pygame.time.get_ticks() * 0.01) * 15)
            offset2 = int(math.sin(pygame.time.get_ticks() * 0.01 + 1) * 10)
            
            # Тени стрелок
            arrow1_shadow = menu_font.render("▶", True, BLACK)
            arrow2_shadow = subtitle_font.render("▶", True, BLACK)
            surface.blit(arrow1_shadow, (arrow_x + offset1 + 2, arrow_y - 15 + 2))
            surface.blit(arrow2_shadow, (arrow_x + offset2 + 20 + 2, arrow_y - 10 + 2))
            
            # Основные стрелки
            arrow1 = menu_font.render("▶", True, NFACT_GREEN)
            arrow2 = subtitle_font.render("▶", True, NFACT_ORANGE)
            surface.blit(arrow1, (arrow_x + offset1, arrow_y - 15))
            surface.blit(arrow2, (arrow_x + offset2 + 20, arrow_y - 10))
        
        # Описание с фоном
        if self.selected and self.description:
            desc_bg = pygame.Surface((600, 30), pygame.SRCALPHA)
            desc_bg.fill((0, 0, 0, 150))
            desc_bg_rect = desc_bg.get_rect(center=(center_x, self.current_y + 45 + pulse_offset))
            surface.blit(desc_bg, desc_bg_rect)
            
            # Тень описания
            desc_shadow = subtitle_font.render(self.description, True, BLACK)
            desc_shadow_rect = desc_shadow.get_rect(center=(center_x + 1, self.current_y + 45 + pulse_offset + 1))
            surface.blit(desc_shadow, desc_shadow_rect)
            
            # Основное описание
            desc_surface = subtitle_font.render(self.description, True, LIGHT_GRAY)
            desc_rect = desc_surface.get_rect(center=(center_x, self.current_y + 45 + pulse_offset))
            surface.blit(desc_surface, desc_rect)
        
        # Частицы при выборе
        if self.selected and self.particle_timer % 8 == 0:
            particle_system.add_particles(
                center_x + random.randint(-150, 150),
                self.current_y + random.randint(-30, 30),
                3,
                random.choice([NFACT_GREEN, NFACT_ORANGE, GOLD])
            )

# Главное меню
class MainMenu:
    def __init__(self):
        self.menu_items = [
            MenuItem("Wake Up", sleep_game, 260, ),
            MenuItem("Deadline Dash", runner_game, 310, ),
            MenuItem("Mentor Quiz", quiz_game, 360, ),
            MenuItem("Incubator Journey", incubator_game, 410, ),
            MenuItem("nFactorial Tetris", tetris_game, 460, ),
            MenuItem("Exit", None, 510, )
        ]
        self.selected_index = 0
        self.menu_items[0].selected = True
        self.particle_system = ParticleSystem()
        self.background_animation = 0
        self.intro_animation = 240
        self.title_bounce = 0
        self.rainbow_shift = 0
    
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.menu_items[self.selected_index].selected = False
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)
                    self.menu_items[self.selected_index].selected = True
                    self.particle_system.add_particles(center_x, self.menu_items[self.selected_index].current_y, 12, NFACT_BLUE)
                
                elif event.key == pygame.K_UP:
                    self.menu_items[self.selected_index].selected = False
                    self.selected_index = (self.selected_index - 1) % len(self.menu_items)
                    self.menu_items[self.selected_index].selected = True
                    self.particle_system.add_particles(center_x, self.menu_items[self.selected_index].current_y, 12, NFACT_BLUE)
                
                elif event.key == pygame.K_RETURN:
                    # Эффект выбора
                    selected_item = self.menu_items[self.selected_index]
                    self.particle_system.add_firework(center_x, selected_item.current_y)
                    return selected_item.action
                
                elif event.key == pygame.K_SPACE:
                    # Секретный фейерверк
                    for _ in range(5):
                        x = random.randint(100, WINDOW_SIZE[0] - 100)
                        y = random.randint(100, WINDOW_SIZE[1] - 100)
                        self.particle_system.add_firework(x, y)
        
        return "continue"
    
    def update(self):
        # Убираем большинство анимаций, оставляем только обновление частиц
        for item in self.menu_items:
            item.update()
        
        self.particle_system.update()
    
    def draw(self, surface):
        # Фон
        surface.blit(bg, (0, 0))
        
        # Дополнительные эффекты фона
        overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        
       
        
        surface.blit(overlay, (0, 0))
        
        # Частицы
        self.particle_system.draw(surface)
        
        # Логотип статичный
        logo_rect = logo.get_rect(center=(center_x, 70))
        surface.blit(logo, logo_rect)
        
        # Заголовок с радужным эффектом и контрастным фоном
        title_y = 200 + int(math.sin(self.title_bounce) * 5)
        if self.intro_animation > 0:
            title_y += self.intro_animation * 1.5
        
       
        title_bg = pygame.Surface((600, 120), pygame.SRCALPHA)
        title_bg.fill((0, 0, 0, 200))
        title_bg_rect = title_bg.get_rect(center=(center_x, title_y + 40))
        surface.blit(title_bg, title_bg_rect)
        
       
        
        
        # Элементы меню статичные
        for item in self.menu_items:
            item.draw(surface, self.particle_system)
        
        
        
      
     

# Основной игровой цикл
def main():
    load_resources()
    menu = MainMenu()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        events = pygame.event.get()
        
        # Обработка событий
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # Переключение полноэкранного режима
                    pygame.display.toggle_fullscreen()
        
        # Обработка ввода меню
        choice = menu.handle_input(events)
        
        if choice == "continue":
            # Обновление
            menu.update()
            
            # Отрисовка
            menu.draw(window)
            pygame.display.flip()
            clock.tick(60)
        
        elif choice is None:
            # Выход с эффектом
            for alpha in range(0, 255, 5):
                fade_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
                fade_surface.fill((0, 0, 0, 0))
                fade_surface.set_alpha(alpha)
                menu.draw(window)
                window.blit(fade_surface, (0, 0))
                pygame.display.flip()
                clock.tick(60)
            running = False
        else:
            try:
                # Эффект перехода
                transition_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
                for alpha in range(0, 255, 8):
                    transition_surface.fill((0, 0, 0, 0))
                    transition_surface.set_alpha(alpha)
                    menu.draw(window)
                    window.blit(transition_surface, (0, 0))
                    
                    # Текст загрузки
                    if alpha > 100:
                        loading_text = subtitle_font.render("Загрузка игры...", True, WHITE)
                        loading_rect = loading_text.get_rect(center=(center_x, center_y))
                        window.blit(loading_text, loading_rect)
                    
                    pygame.display.flip()
                    clock.tick(60)
                
                # Запуск игры
                result = choice.main(window)
                
                # Эффект возврата
                for alpha in range(255, 0, -8):
                    transition_surface.fill((0, 0, 0, 0))
                    transition_surface.set_alpha(alpha)
                    menu.draw(window)
                    window.blit(transition_surface, (0, 0))
                    pygame.display.flip()
                    clock.tick(60)
                
                # Фейерверк при успешном завершении
                if result:
                    for _ in range(10):
                        x = random.randint(100, WINDOW_SIZE[0] - 100)
                        y = random.randint(100, WINDOW_SIZE[1] - 100)
                        menu.particle_system.add_firework(x, y)
                
                # Пауза после игры
                time.sleep(0.5)
            except Exception as e:
                print(f"Ошибка при запуске игры: {e}")
                # Показать ошибку
                error_surface = subtitle_font.render(f"Ошибка: {str(e)}", True, NFACT_RED)
                error_rect = error_surface.get_rect(center=(center_x, center_y))
                window.blit(error_surface, error_rect)
                pygame.display.flip()
                time.sleep(2)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()