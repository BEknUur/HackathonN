import pygame
import random
import pathlib
import math
from enum import Enum
from typing import Dict, List, Tuple

def main(window):
    """
    Epic Deadline Dash — nFactorial Edition
    Многоэтапный раннер с прогрессией, ресурсами и комбо-системой
    """
    # Инициализация
    pygame.display.set_caption("Epic Deadline Dash — nFactorial Edition")
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
    
    # Загрузка ресурсов
    base = pathlib.Path(__file__).parent.resolve()
    try:
        logo = pygame.image.load(str(base / "assets" / "logo.png")).convert_alpha()
        logo = pygame.transform.smoothscale(logo, (60, 60))
    except:
        # Создаем логотип если файл не найден
        logo = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(logo, NFACT_BLUE, (30, 30), 28)
        pygame.draw.circle(logo, WHITE, (30, 30), 20)
        font_logo = pygame.font.Font(None, 24)
        text = font_logo.render("nF", True, NFACT_BLUE)
        logo.blit(text, (18, 18))
    
    # Шрифты
    font_small = pygame.font.Font(None, 24)
    font_medium = pygame.font.Font(None, 32)
    font_big = pygame.font.Font(None, 48)
    font_huge = pygame.font.Font(None, 72)
    
    # Игровые состояния
    class GameStage(Enum):
        INTERVIEW = 1
        BOOTCAMP = 2
        DEMO_DAY = 3
        UNICORN = 4
    
    # Конфигурация этапов
    STAGE_CONFIG = {
        GameStage.INTERVIEW: {
            'name': 'Собеседование',
            'duration': 20,
            'bg_color': (50, 50, 80),
            'obstacle_speed': 6,
            'obstacle_freq': 1200,
            'required_resources': {'code': 15, 'coffee': 10, 'motivation': 8}
        },
        GameStage.BOOTCAMP: {
            'name': 'Буткемп',
            'duration': 25,
            'bg_color': (80, 50, 50),
            'obstacle_speed': 8,
            'obstacle_freq': 900,
            'required_resources': {'code': 30, 'coffee': 20, 'motivation': 15}
        },
        GameStage.DEMO_DAY: {
            'name': 'Demo Day',
            'duration': 30,
            'bg_color': (50, 80, 50),
            'obstacle_speed': 10,
            'obstacle_freq': 700,
            'required_resources': {'code': 50, 'coffee': 35, 'motivation': 25}
        },
        GameStage.UNICORN: {
            'name': 'Единорог',
            'duration': 40,
            'bg_color': (80, 50, 80),
            'obstacle_speed': 12,
            'obstacle_freq': 500,
            'required_resources': {'code': 100, 'coffee': 75, 'motivation': 50}
        }
    }
    
    # Полосы движения
    lanes = [W * 0.2, W * 0.5, W * 0.8]
    GRAVITY = 1.5
    JUMP_V = -22
    
    # Менеджер ресурсов
    class ResourceManager:
        def __init__(self):
            self.resources = {'code': 0, 'coffee': 0, 'motivation': 0}
            self.collection_multiplier = 1.0
            self.effects = {
                'code': 0,      # Иммунитет к препятствиям
                'coffee': 0,    # Ускорение
                'motivation': 0  # Больше очков
            }
        
        def add_resource(self, resource_type: str, amount: int):
            if resource_type in self.resources:
                self.resources[resource_type] += int(amount * self.collection_multiplier)
        
        def use_resource(self, resource_type: str, amount: int) -> bool:
            if self.resources[resource_type] >= amount:
                self.resources[resource_type] -= amount
                return True
            return False
        
        def apply_effect(self, resource_type: str, duration: int):
            self.effects[resource_type] = max(self.effects[resource_type], duration)
        
        def update(self):
            for effect in self.effects:
                if self.effects[effect] > 0:
                    self.effects[effect] -= 1
        
        def has_immunity(self) -> bool:
            return self.effects['code'] > 0
        
        def has_speed_boost(self) -> bool:
            return self.effects['coffee'] > 0
        
        def has_score_boost(self) -> bool:
            return self.effects['motivation'] > 0
    
    # Система комбо
    class ComboSystem:
        def __init__(self):
            self.combo_count = 0
            self.combo_multiplier = 1.0
            self.combo_timer = 0
            self.max_combo_time = 3.0
            self.combo_decay = 0.02
        
        def add_combo(self, points: int = 1):
            self.combo_count += points
            self.combo_multiplier = min(1.0 + (self.combo_count * 0.05), 3.0)
            self.combo_timer = self.max_combo_time
        
        def update(self, dt: float):
            if self.combo_timer > 0:
                self.combo_timer -= dt
                if self.combo_timer <= 0:
                    self.reset_combo()
        
        def reset_combo(self):
            self.combo_count = 0
            self.combo_multiplier = 1.0
            self.combo_timer = 0
        
        def get_multiplier(self) -> float:
            return self.combo_multiplier
    
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
            color = (*self.color, alpha)
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
    
    # Игрок
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.create_sprite()
            self.lane_idx = 1
            self.rect = self.image.get_rect(midbottom=(lanes[self.lane_idx], GROUND_Y - 5))
            self.vy = 0
            self.jumping = False
            self.animation_frame = 0
            self.animation_timer = 0
            self.invulnerable = 0
            self.dash_cooldown = 0
            self.trail_positions = []
        
        def create_sprite(self):
            self.image = pygame.Surface((45, 75), pygame.SRCALPHA)
            # Тело
            pygame.draw.ellipse(self.image, NFACT_BLUE, (5, 20, 35, 50))
            # Голова
            pygame.draw.circle(self.image, WHITE, (22, 15), 12)
            # Глаза
            pygame.draw.circle(self.image, BLACK, (18, 12), 2)
            pygame.draw.circle(self.image, BLACK, (26, 12), 2)
            # Ноги
            pygame.draw.rect(self.image, DARK_GRAY, (15, 65, 6, 10))
            pygame.draw.rect(self.image, DARK_GRAY, (24, 65, 6, 10))
        
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
            if self.dash_cooldown > 0:
                self.dash_cooldown -= 1
            
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
        
        def dash(self):
            if self.dash_cooldown <= 0:
                self.invulnerable = 30
                self.dash_cooldown = 120
                return True
            return False
        
        def draw_trail(self, surface):
            for i, pos in enumerate(self.trail_positions):
                alpha = int(255 * (i / len(self.trail_positions)) * 0.3)
                color = (*NFACT_GREEN, alpha)
                try:
                    pygame.draw.circle(surface, NFACT_GREEN, pos, 3)
                except:
                    pass
    
    # Препятствия
    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, obstacle_type: str, speed: float):
            super().__init__()
            self.type = obstacle_type
            self.speed = speed
            self.lane_idx = random.randint(0, 2)
            self.create_sprite()
            self.rect = self.image.get_rect(midbottom=(lanes[self.lane_idx], -50))
            self.rotation = 0
        
        def create_sprite(self):
            if self.type == 'bug':
                self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (200, 50, 50), (0, 0, 50, 50))
                pygame.draw.rect(self.image, (255, 100, 100), (5, 5, 40, 40))
                # Глитч эффект
                for _ in range(10):
                    x, y = random.randint(0, 45), random.randint(0, 45)
                    pygame.draw.rect(self.image, (255, 0, 0), (x, y, 5, 2))
            elif self.type == 'server':
                self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
                pygame.draw.rect(self.image, DARK_GRAY, (0, 0, 60, 40))
                pygame.draw.rect(self.image, (100, 100, 100), (5, 5, 50, 30))
                # Индикаторы
                for i in range(3):
                    color = random.choice([NFACT_GREEN, (255, 0, 0), NFACT_ORANGE])
                    pygame.draw.circle(self.image, color, (15 + i*15, 20), 3)
            elif self.type == 'deadline':
                self.image = pygame.Surface((45, 60), pygame.SRCALPHA)
                pygame.draw.polygon(self.image, (255, 200, 0), [(22, 0), (45, 60), (0, 60)])
                pygame.draw.polygon(self.image, (255, 255, 0), [(22, 5), (40, 55), (5, 55)])
        
        def update(self):
            self.rect.y += self.speed
            self.rotation += 2
            if self.rect.top > H:
                self.kill()
    
    # Ресурсы для сбора
    class Collectible(pygame.sprite.Sprite):
        def __init__(self, resource_type: str):
            super().__init__()
            self.type = resource_type
            self.lane_idx = random.randint(0, 2)
            self.create_sprite()
            self.rect = self.image.get_rect(center=(lanes[self.lane_idx], -30))
            self.float_offset = 0
            self.collected = False
        
        def create_sprite(self):
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            if self.type == 'code':
                pygame.draw.rect(self.image, NFACT_GREEN, (0, 0, 30, 30))
                pygame.draw.rect(self.image, WHITE, (3, 3, 24, 24))
                # Символ кода
                font = pygame.font.Font(None, 20)
                text = font.render("<>", True, NFACT_GREEN)
                self.image.blit(text, (6, 8))
            elif self.type == 'coffee':
                pygame.draw.ellipse(self.image, (139, 69, 19), (0, 0, 30, 30))
                pygame.draw.ellipse(self.image, (160, 82, 45), (3, 3, 24, 24))
                # Пар
                for i in range(3):
                    pygame.draw.circle(self.image, WHITE, (10 + i*5, 8), 2)
            elif self.type == 'motivation':
                pygame.draw.polygon(self.image, NFACT_ORANGE, 
                                  [(15, 0), (30, 10), (22, 15), (30, 20), (15, 30), (0, 20), (8, 15), (0, 10)])
                pygame.draw.polygon(self.image, (255, 200, 0), 
                                  [(15, 3), (27, 11), (21, 15), (27, 19), (15, 27), (3, 19), (9, 15), (3, 11)])
        
        def update(self):
            self.rect.y += 5
            self.float_offset += 0.2
            self.rect.x += math.sin(self.float_offset) * 0.5
            if self.rect.top > H:
                self.kill()
    
    # Инициализация системы
    resource_manager = ResourceManager()
    combo_system = ComboSystem()
    particle_system = ParticleSystem()
    
    # Игровые объекты
    player = Player()
    obstacles = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    
    # Игровые переменные
    current_stage = GameStage.INTERVIEW
    stage_start_time = pygame.time.get_ticks()
    score = 0
    distance = 0
    
    # События
    OBSTACLE_EVENT = pygame.USEREVENT + 1
    COLLECTIBLE_EVENT = pygame.USEREVENT + 2
    
    def update_stage_events():
        config = STAGE_CONFIG[current_stage]
        pygame.time.set_timer(OBSTACLE_EVENT, config['obstacle_freq'])
        pygame.time.set_timer(COLLECTIBLE_EVENT, 2000)
    
    update_stage_events()
    
    def draw_gradient_background(surface, color1, color2):
        for y in range(H):
            ratio = y / H
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (W, y))
    
    def draw_hud(surface):
        # Фон HUD
        hud_surface = pygame.Surface((W, 120), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 150))
        surface.blit(hud_surface, (0, 0))
        
        # Логотип
        surface.blit(logo, (10, 10))
        
        # Текущий этап
        stage_text = font_medium.render(f"Этап: {STAGE_CONFIG[current_stage]['name']}", True, WHITE)
        surface.blit(stage_text, (80, 15))
        
        # Прогресс этапа
        elapsed = (pygame.time.get_ticks() - stage_start_time) // 1000
        duration = STAGE_CONFIG[current_stage]['duration']
        progress = min(elapsed / duration, 1.0)
        
        # Полоса прогресса
        progress_rect = pygame.Rect(80, 45, 200, 10)
        pygame.draw.rect(surface, DARK_GRAY, progress_rect)
        pygame.draw.rect(surface, NFACT_GREEN, (80, 45, int(200 * progress), 10))
        
        # Время
        time_text = font_small.render(f"{elapsed}/{duration}s", True, WHITE)
        surface.blit(time_text, (290, 42))
        
        # Ресурсы
        resources_y = 70
        for i, (resource, amount) in enumerate(resource_manager.resources.items()):
            color = NFACT_GREEN if resource == 'code' else (139, 69, 19) if resource == 'coffee' else NFACT_ORANGE
            
            # Иконка ресурса
            icon_rect = pygame.Rect(80 + i * 80, resources_y, 20, 20)
            pygame.draw.rect(surface, color, icon_rect)
            
            # Количество
            amount_text = font_small.render(str(amount), True, WHITE)
            surface.blit(amount_text, (105 + i * 80, resources_y + 2))
            
            # Эффект
            if resource_manager.effects[resource] > 0:
                effect_text = font_small.render(f"({resource_manager.effects[resource]})", True, color)
                surface.blit(effect_text, (105 + i * 80, resources_y + 20))
        
        # Комбо
        if combo_system.combo_count > 0:
            combo_text = font_medium.render(f"COMBO x{combo_system.combo_count:.0f}", True, NFACT_ORANGE)
            surface.blit(combo_text, (400, 15))
            
            # Полоса комбо
            combo_progress = combo_system.combo_timer / combo_system.max_combo_time
            combo_rect = pygame.Rect(400, 45, 150, 8)
            pygame.draw.rect(surface, DARK_GRAY, combo_rect)
            pygame.draw.rect(surface, NFACT_ORANGE, (400, 45, int(150 * combo_progress), 8))
        
        # Счет
        score_text = font_medium.render(f"Счет: {score}", True, WHITE)
        surface.blit(score_text, (W - 150, 15))
        
        # Дистанция
        distance_text = font_small.render(f"Дистанция: {distance}м", True, WHITE)
        surface.blit(distance_text, (W - 150, 45))
    
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
    
    def handle_stage_progression():
        nonlocal current_stage, stage_start_time
        
        elapsed = (pygame.time.get_ticks() - stage_start_time) // 1000
        duration = STAGE_CONFIG[current_stage]['duration']
        
        # Проверка требований к ресурсам
        required = STAGE_CONFIG[current_stage]['required_resources']
        has_resources = all(resource_manager.resources[res] >= required[res] for res in required)
        
        if elapsed >= duration and has_resources:
            # Переход к следующему этапу
            if current_stage == GameStage.INTERVIEW:
                current_stage = GameStage.BOOTCAMP
            elif current_stage == GameStage.BOOTCAMP:
                current_stage = GameStage.DEMO_DAY
            elif current_stage == GameStage.DEMO_DAY:
                current_stage = GameStage.UNICORN
            elif current_stage == GameStage.UNICORN:
                # Победа!
                return "victory"
            
            stage_start_time = pygame.time.get_ticks()
            update_stage_events()
            
            # Бонус за прохождение этапа
            combo_system.add_combo(10)
            particle_system.add_explosion(player.rect.centerx, player.rect.centery, NFACT_GREEN)
        
        elif elapsed >= duration and not has_resources:
            # Провал из-за нехватки ресурсов
            return "failure"
        
        return "continue"
    
    # Основной игровой цикл
    running = True
    dt = 0
    
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time в секундах
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_x:
                    if player.dash():
                        particle_system.add_explosion(player.rect.centerx, player.rect.centery, NFACT_BLUE)
                elif event.key == pygame.K_1:
                    if resource_manager.use_resource('code', 5):
                        resource_manager.apply_effect('code', 180)
                elif event.key == pygame.K_2:
                    if resource_manager.use_resource('coffee', 3):
                        resource_manager.apply_effect('coffee', 120)
                elif event.key == pygame.K_3:
                    if resource_manager.use_resource('motivation', 4):
                        resource_manager.apply_effect('motivation', 150)
            
            elif event.type == OBSTACLE_EVENT:
                obstacle_types = ['bug', 'server', 'deadline']
                obstacle_type = random.choice(obstacle_types)
                speed = STAGE_CONFIG[current_stage]['obstacle_speed']
                obstacle = Obstacle(obstacle_type, speed)
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
            
            elif event.type == COLLECTIBLE_EVENT:
                resource_types = ['code', 'coffee', 'motivation']
                resource_type = random.choice(resource_types)
                collectible = Collectible(resource_type)
                collectibles.add(collectible)
                all_sprites.add(collectible)
        
        # Обновление объектов
        all_sprites.update()
        resource_manager.update()
        combo_system.update(dt)
        particle_system.update()
        
        # Увеличение дистанции
        distance += 1
        
        # Столкновения с препятствиями
        if not resource_manager.has_immunity() and player.invulnerable <= 0:
            hit_obstacles = pygame.sprite.spritecollide(player, obstacles, True)
            if hit_obstacles:
                # Потеря ресурсов при столкновении
                for resource in resource_manager.resources:
                    loss = min(resource_manager.resources[resource], 5)
                    resource_manager.resources[resource] -= loss
                
                combo_system.reset_combo()
                particle_system.add_explosion(player.rect.centerx, player.rect.centery, (255, 0, 0))
                player.invulnerable = 60
        
        # Сбор ресурсов
        collected = pygame.sprite.spritecollide(player, collectibles, True)
        for collectible in collected:
            resource_manager.add_resource(collectible.type, 3)
            combo_system.add_combo(2)
            particle_system.add_explosion(collectible.rect.centerx, collectible.rect.centery, NFACT_GREEN)
            
            # Увеличение счета
            points = int(10 * combo_system.get_multiplier())
            if resource_manager.has_score_boost():
                points *= 2
            score += points
        
        # Прогрессия этапов
        stage_result = handle_stage_progression()
        if stage_result == "victory":
            # Экран победы
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            window.blit(overlay, (0, 0))
            
            victory_text = font_huge.render("ПОЗДРАВЛЯЕМ!", True, NFACT_GREEN)
            subtitle_text = font_medium.render("Вы создали единорога!", True, WHITE)
            score_text = font_medium.render(f"Финальный счет: {score}", True, WHITE)
            
            window.blit(victory_text, (W//2 - victory_text.get_width()//2, H//2 - 100))
            window.blit(subtitle_text, (W//2 - subtitle_text.get_width()//2, H//2 - 50))
            window.blit(score_text, (W//2 - score_text.get_width()//2, H//2))
            
            pygame.display.flip()
            pygame.time.wait(3000)
            return True
        
        elif stage_result == "failure":
            # Экран поражения
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            window.blit(overlay, (0, 0))
            
            failure_text = font_huge.render("ИСКЛЮЧЕН!", True, (255, 0, 0))
            subtitle_text = font_medium.render("Не хватило ресурсов для прохождения этапа", True, WHITE)
            
            window.blit(failure_text, (W//2 - failure_text.get_width()//2, H//2 - 50))
            window.blit(subtitle_text, (W//2 - subtitle_text.get_width()//2, H//2))
            
            pygame.display.flip()
            pygame.time.wait(3000)
            return False
        
        # Отрисовка
        # Фон с градиентом
        bg_color = STAGE_CONFIG[current_stage]['bg_color']
        draw_gradient_background(window, bg_color, (bg_color[0]//2, bg_color[1]//2, bg_color[2]//2))
        
        # Дорога
        draw_lanes(window)
        
        # След игрока
        player.draw_trail(window)
        
        # Эффекты
        if resource_manager.has_immunity():
            # Эффект неуязвимости
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 30))
            window.blit(overlay, (0, 0))
        
        if resource_manager.has_speed_boost():
            # Эффект ускорения - линии движения
            for i in range(10):
                y = random.randint(0, H)
                pygame.draw.line(window, NFACT_ORANGE, (0, y), (W//4, y), 2)
        
        # Мигание при неуязвимости
        if player.invulnerable > 0 and player.invulnerable % 10 < 5:
            pass  # Не рисуем игрока
        else:
            all_sprites.draw(window)
        
        # Частицы
        particle_system.draw(window)
        
        # HUD
        draw_hud(window)
        
        # Дополнительные эффекты интерфейса
        if combo_system.combo_count > 5:
            # Эффект при большом комбо
            combo_glow = pygame.Surface((W, H), pygame.SRCALPHA)
            alpha = int(50 * math.sin(pygame.time.get_ticks() * 0.01))
            combo_glow.fill((255, 165, 0, alpha))
            window.blit(combo_glow, (0, 0))
        
        # Подсказки управления
        if pygame.time.get_ticks() < 10000:  # Первые 10 секунд
            hints = [
                "Стрелки - движение по полосам",
                "SPACE - прыжок",
                "X - рывок (иммунитет)",
                "1/2/3 - использовать ресурсы"
            ]
            
            for i, hint in enumerate(hints):
                hint_text = font_small.render(hint, True, WHITE)
                window.blit(hint_text, (W - 250, H - 100 + i * 20))
        
        # Индикатор рывка
        if player.dash_cooldown > 0:
            dash_text = font_small.render(f"Рывок: {player.dash_cooldown//60 + 1}s", True, LIGHT_GRAY)
            window.blit(dash_text, (W - 150, H - 40))
        else:
            dash_text = font_small.render("Рывок: готов", True, NFACT_GREEN)
            window.blit(dash_text, (W - 150, H - 40))
        
        pygame.display.flip()
    
    return False