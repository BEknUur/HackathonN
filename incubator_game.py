import pygame
import random
import math
import time
import pathlib
from enum import Enum
from typing import Dict, List, Tuple, Optional

def main(window):
    """
    Incubator Journey — nFactorial Edition
    Пройди путь от идеи до единорога в инкубаторе!
    Управляй ресурсами, командой и принимай важные решения.
    """
    pygame.display.set_caption("Incubator Journey — nFactorial Edition")
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
    
    # Загрузка ресурсов
    base = pathlib.Path(__file__).parent.resolve()
    try:
        logo = pygame.image.load(str(base / "assets" / "logo.png")).convert_alpha()
        logo = pygame.transform.smoothscale(logo, (60, 60))
    except:
        logo = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(logo, NFACT_BLUE, (30, 30), 28)
        pygame.draw.circle(logo, WHITE, (30, 30), 20)
    
    # Шрифты
    try:
        font_path = str(base / "assets" / "dogica.ttf")
        font_small = pygame.font.Font(font_path, 16)
        font_medium = pygame.font.Font(font_path, 24)
        font_large = pygame.font.Font(font_path, 32)
        font_huge = pygame.font.Font(font_path, 48)
    except:
        font_small = pygame.font.Font(None, 20)
        font_medium = pygame.font.Font(None, 28)
        font_large = pygame.font.Font(None, 36)
        font_huge = pygame.font.Font(None, 52)
    
    # Игровые фазы
    class GamePhase(Enum):
        IDEA = 1
        TEAM_BUILDING = 2
        DEVELOPMENT = 3
        TESTING = 4
        PITCH = 5
        SCALING = 6
        DEMO_DAY = 7
    
    # Конфигурация фаз
    PHASE_CONFIG = {
        GamePhase.IDEA: {
            'name': 'Генерация идеи',
            'duration': 10,
            'description': 'Придумай революционную идею!',
            'challenges': ['Слишком сложно', 'Уже существует', 'Нет рынка'],
            'color': NFACT_BLUE
        },
        GamePhase.TEAM_BUILDING: {
            'name': 'Сборка команды',
            'duration': 15,
            'description': 'Найди идеальную команду!',
            'challenges': ['Нет CTO', 'Конфликты', 'Мало опыта'],
            'color': NFACT_GREEN
        },
        GamePhase.DEVELOPMENT: {
            'name': 'Разработка MVP',
            'duration': 20,
            'description': 'Создай минимальный продукт!',
            'challenges': ['Технический долг', 'Баги', 'Нет времени'],
            'color': NFACT_ORANGE
        },
        GamePhase.TESTING: {
            'name': 'Тестирование',
            'duration': 12,
            'description': 'Найди и исправь все баги!',
            'challenges': ['Критический баг', 'Плохой UX', 'Медленно'],
            'color': NFACT_RED
        },
        GamePhase.PITCH: {
            'name': 'Питч менторам',
            'duration': 8,
            'description': 'Убеди менторов в своей идее!',
            'challenges': ['Нервозность', 'Сложные вопросы', 'Техпроблемы'],
            'color': GOLD
        },
        GamePhase.SCALING: {
            'name': 'Масштабирование',
            'duration': 18,
            'description': 'Привлеки первых пользователей!',
            'challenges': ['Нет пользователей', 'Конкуренты', 'Нехватка денег'],
            'color': (128, 0, 128)
        },
        GamePhase.DEMO_DAY: {
            'name': 'Demo Day',
            'duration': 10,
            'description': 'Финальная презентация!',
            'challenges': ['Жесткое жюри', 'Волнение', 'Техсбой'],
            'color': (255, 20, 147)
        }
    }
    
    # Игровое состояние
    class GameState:
        def __init__(self):
            self.current_phase = GamePhase.IDEA
            self.phase_progress = 0
            self.phase_start_time = pygame.time.get_ticks()
            
            # Ресурсы
            self.resources = {
                'money': 1000,
                'time': 100,
                'energy': 100,
                'team_morale': 100,
                'product_quality': 0,
                'market_fit': 0,
                'investor_interest': 0
            }
            
            # Команда
            self.team = []
            self.team_size = 1  # Только основатель
            
            # События и достижения
            self.events = []
            self.achievements = []
            self.score = 0
            
            # Активные модификаторы
            self.modifiers = {}
            
            # Статистика
            self.decisions_made = 0
            self.challenges_solved = 0
            self.bugs_fixed = 0
    
    # Система событий
    class Event:
        def __init__(self, title: str, description: str, choices: List[Dict], phase: GamePhase):
            self.title = title
            self.description = description
            self.choices = choices
            self.phase = phase
            self.active = True
    
    # Создание событий
    def create_events():
        events = []
        
        # События для разных фаз
        events.append(Event(
            "Выбор технологии",
            "Какую технологию использовать для MVP?",
            [
                {"text": "Python + Django", "effects": {"time": -10, "product_quality": +15}},
                {"text": "JavaScript + React", "effects": {"time": -5, "product_quality": +10}},
                {"text": "No-code решение", "effects": {"time": +5, "product_quality": -5}}
            ],
            GamePhase.DEVELOPMENT
        ))
        
        events.append(Event(
            "Конфликт в команде",
            "Возник конфликт между разработчиками!",
            [
                {"text": "Провести тимбилдинг", "effects": {"money": -100, "team_morale": +20}},
                {"text": "Поговорить лично", "effects": {"time": -5, "team_morale": +10}},
                {"text": "Игнорировать", "effects": {"team_morale": -15}}
            ],
            GamePhase.TEAM_BUILDING
        ))
        
        events.append(Event(
            "Критический баг",
            "Найден критический баг перед демо!",
            [
                {"text": "Работать всю ночь", "effects": {"energy": -30, "product_quality": +15}},
                {"text": "Показать как фичу", "effects": {"investor_interest": -10}},
                {"text": "Отложить демо", "effects": {"time": -20}}
            ],
            GamePhase.TESTING
        ))
        
        events.append(Event(
            "Инвестор заинтересован",
            "Инвестор хочет встретиться!",
            [
                {"text": "Согласиться немедленно", "effects": {"investor_interest": +15, "time": -5}},
                {"text": "Подготовиться неделю", "effects": {"time": -10, "investor_interest": +25}},
                {"text": "Отказаться", "effects": {"investor_interest": -5}}
            ],
            GamePhase.PITCH
        ))
        
        return events
    
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
        
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.life -= 1
        
        def draw(self, surface):
            if self.life > 0:
                alpha = self.life / self.max_life
                if self.text:
                    text_surface = font_small.render(self.text, True, self.color)
                    surface.blit(text_surface, (int(self.x), int(self.y)))
                else:
                    pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)
    
    class ParticleSystem:
        def __init__(self):
            self.particles = []
        
        def add_effect(self, x: float, y: float, effect_type: str, value: int = 0):
            if effect_type == "money":
                color = GOLD
                text = f"+{value}$" if value > 0 else f"{value}$"
            elif effect_type == "energy":
                color = NFACT_GREEN if value > 0 else NFACT_RED
                text = f"+{value}" if value > 0 else f"{value}"
            elif effect_type == "quality":
                color = NFACT_BLUE
                text = f"+{value}%" if value > 0 else f"{value}%"
            else:
                color = WHITE
                text = ""
            
            self.particles.append(Particle(x, y, color, text))
        
        def update(self):
            self.particles = [p for p in self.particles if p.life > 0]
            for particle in self.particles:
                particle.update()
        
        def draw(self, surface):
            for particle in self.particles:
                particle.draw(surface)
    
    # Инициализация
    game_state = GameState()
    events = create_events()
    particle_system = ParticleSystem()
    current_event = None
    event_timer = 0
    selected_choice = 0
    
    # Функции отрисовки
    def draw_gradient_background(surface):
        phase_color = PHASE_CONFIG[game_state.current_phase]['color']
        for y in range(H):
            ratio = y / H
            r = int(DARK_BG[0] * (1 - ratio) + phase_color[0] * ratio * 0.1)
            g = int(DARK_BG[1] * (1 - ratio) + phase_color[1] * ratio * 0.1)
            b = int(DARK_BG[2] * (1 - ratio) + phase_color[2] * ratio * 0.1)
            pygame.draw.line(surface, (r, g, b), (0, y), (W, y))
    
    def draw_phase_info(surface):
        phase_info = PHASE_CONFIG[game_state.current_phase]
        
        # Фаза и прогресс
        phase_text = font_large.render(f"Фаза: {phase_info['name']}", True, WHITE)
        surface.blit(phase_text, (20, 20))
        
        # Описание
        desc_text = font_small.render(phase_info['description'], True, LIGHT_GRAY)
        surface.blit(desc_text, (20, 50))
        
        # Прогресс-бар
        progress_width = 300
        progress_height = 20
        progress_x = 20
        progress_y = 80
        
        # Фон прогресса
        pygame.draw.rect(surface, BLACK, (progress_x, progress_y, progress_width, progress_height))
        # Заполнение прогресса
        fill_width = int(progress_width * (game_state.phase_progress / 100))
        pygame.draw.rect(surface, phase_info['color'], (progress_x, progress_y, fill_width, progress_height))
        # Рамка
        pygame.draw.rect(surface, WHITE, (progress_x, progress_y, progress_width, progress_height), 2)
        
        # Процент
        progress_text = font_small.render(f"{game_state.phase_progress:.1f}%", True, WHITE)
        surface.blit(progress_text, (progress_x + progress_width + 10, progress_y + 2))
    
    def draw_resources(surface):
        resources_x = W - 300
        resources_y = 20
        
        # Фон панели ресурсов
        panel_rect = pygame.Rect(resources_x - 10, resources_y - 10, 290, 220)
        panel_surface = pygame.Surface((290, 220), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 150))
        surface.blit(panel_surface, (resources_x - 10, resources_y - 10))
        
        # Заголовок
        title_text = font_medium.render("Ресурсы", True, WHITE)
        surface.blit(title_text, (resources_x, resources_y))
        
        # Ресурсы
        resource_icons = {
            'money': '$',
            'time': '⏰',
            'energy': '⚡',
            'team_morale': '😊',
            'product_quality': '🔧',
            'market_fit': '📊',
            'investor_interest': '💰'
        }
        
        resource_colors = {
            'money': GOLD,
            'time': NFACT_BLUE,
            'energy': NFACT_GREEN,
            'team_morale': NFACT_ORANGE,
            'product_quality': (128, 128, 255),
            'market_fit': (255, 128, 128),
            'investor_interest': (128, 255, 128)
        }
        
        y_offset = 0
        for resource, value in game_state.resources.items():
            y_pos = resources_y + 30 + y_offset
            
            # Иконка
            icon = resource_icons.get(resource, '?')
            icon_text = font_small.render(icon, True, resource_colors[resource])
            surface.blit(icon_text, (resources_x, y_pos))
            
            # Название
            name_text = font_small.render(resource.replace('_', ' ').title(), True, WHITE)
            surface.blit(name_text, (resources_x + 30, y_pos))
            
            # Значение
            value_text = font_small.render(str(int(value)), True, resource_colors[resource])
            surface.blit(value_text, (resources_x + 180, y_pos))
            
            # Полоска для процентных ресурсов
            if resource in ['energy', 'team_morale', 'product_quality', 'market_fit', 'investor_interest']:
                bar_width = 60
                bar_height = 5
                bar_x = resources_x + 220
                bar_y = y_pos + 8
                
                # Фон
                pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height))
                # Заполнение
                fill_width = int(bar_width * (value / 100))
                pygame.draw.rect(surface, resource_colors[resource], (bar_x, bar_y, fill_width, bar_height))
                # Рамка
                pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
            
            y_offset += 25
    
    def draw_event(surface, event):
        if not event:
            return
        
        # Фон события
        event_width = W - 100
        event_height = 250
        event_x = 50
        event_y = H - event_height - 50
        
        event_surface = pygame.Surface((event_width, event_height), pygame.SRCALPHA)
        event_surface.fill((0, 0, 0, 200))
        surface.blit(event_surface, (event_x, event_y))
        
        # Рамка
        pygame.draw.rect(surface, NFACT_ORANGE, (event_x, event_y, event_width, event_height), 3)
        
        # Заголовок события
        title_text = font_medium.render(event.title, True, NFACT_ORANGE)
        surface.blit(title_text, (event_x + 20, event_y + 20))
        
        # Описание
        desc_text = font_small.render(event.description, True, WHITE)
        surface.blit(desc_text, (event_x + 20, event_y + 50))
        
        # Варианты выбора
        for i, choice in enumerate(event.choices):
            choice_y = event_y + 90 + i * 40
            
            # Подсветка выбранного варианта
            if i == selected_choice:
                highlight_rect = pygame.Rect(event_x + 15, choice_y - 5, event_width - 30, 30)
                pygame.draw.rect(surface, (50, 50, 50), highlight_rect)
                pygame.draw.rect(surface, NFACT_GREEN, highlight_rect, 2)
            
            # Текст выбора
            choice_text = font_small.render(f"{i + 1}. {choice['text']}", True, WHITE)
            surface.blit(choice_text, (event_x + 30, choice_y))
            
            # Эффекты
            effects_text = []
            for effect, value in choice['effects'].items():
                if value > 0:
                    effects_text.append(f"+{value} {effect}")
                else:
                    effects_text.append(f"{value} {effect}")
            
            if effects_text:
                effects_str = " | ".join(effects_text)
                effects_surface = font_small.render(effects_str, True, LIGHT_GRAY)
                surface.blit(effects_surface, (event_x + 30, choice_y + 15))
        
        # Подсказка
        hint_text = font_small.render("Используйте ↑/↓ для выбора, ENTER для подтверждения", True, LIGHT_GRAY)
        surface.blit(hint_text, (event_x + 20, event_y + event_height - 30))
    
    def draw_team_info(surface):
        team_x = 50
        team_y = 150
        
        # Заголовок
        team_title = font_medium.render("Команда", True, WHITE)
        surface.blit(team_title, (team_x, team_y))
        
        # Размер команды
        team_size_text = font_small.render(f"Размер: {game_state.team_size} человек", True, LIGHT_GRAY)
        surface.blit(team_size_text, (team_x, team_y + 30))
        
        # Мораль команды
        morale_text = font_small.render(f"Мораль: {game_state.resources['team_morale']:.0f}%", True, LIGHT_GRAY)
        surface.blit(morale_text, (team_x, team_y + 50))
    
    def draw_score(surface):
        score_text = font_medium.render(f"Счет: {game_state.score}", True, GOLD)
        surface.blit(score_text, (W // 2 - 100, 20))
    
    def apply_choice_effects(choice):
        effects = choice['effects']
        
        for effect, value in effects.items():
            if effect in game_state.resources:
                old_value = game_state.resources[effect]
                game_state.resources[effect] = max(0, min(1000, old_value + value))
                
                # Эффект частиц
                particle_system.add_effect(W // 2, H // 2, effect, value)
        
        game_state.decisions_made += 1
        game_state.score += 10
    
    def update_game_state():
        # Обновление прогресса фазы
        elapsed_time = (pygame.time.get_ticks() - game_state.phase_start_time) / 1000
        phase_duration = PHASE_CONFIG[game_state.current_phase]['duration']
        
        # Автоматическое уменьшение ресурсов
        game_state.resources['energy'] = max(0, game_state.resources['energy'] - 0.02)
        game_state.resources['time'] = max(0, game_state.resources['time'] - 0.01)
        
        # Увеличение прогресса
        progress_rate = 1.0
        if game_state.resources['energy'] < 30:
            progress_rate *= 0.5
        if game_state.resources['team_morale'] < 30:
            progress_rate *= 0.7
        
        game_state.phase_progress += progress_rate * 0.5
        
        # Переход к следующей фазе
        if game_state.phase_progress >= 100:
            next_phase = {
                GamePhase.IDEA: GamePhase.TEAM_BUILDING,
                GamePhase.TEAM_BUILDING: GamePhase.DEVELOPMENT,
                GamePhase.DEVELOPMENT: GamePhase.TESTING,
                GamePhase.TESTING: GamePhase.PITCH,
                GamePhase.PITCH: GamePhase.SCALING,
                GamePhase.SCALING: GamePhase.DEMO_DAY,
                GamePhase.DEMO_DAY: None
            }
            
            if next_phase[game_state.current_phase]:
                game_state.current_phase = next_phase[game_state.current_phase]
                game_state.phase_progress = 0
                game_state.phase_start_time = pygame.time.get_ticks()
                game_state.score += 100
                
                # Бонусы за прохождение фазы
                game_state.resources['energy'] = min(100, game_state.resources['energy'] + 20)
                game_state.resources['team_morale'] = min(100, game_state.resources['team_morale'] + 10)
            else:
                # Игра завершена
                return "completed"
        
        # Проверка условий поражения
        if game_state.resources['energy'] <= 0:
            return "exhausted"
        if game_state.resources['team_morale'] <= 0:
            return "team_quit"
        if game_state.resources['money'] <= 0:
            return "bankrupt"
        
        return "continue"
    
    def get_random_event():
        available_events = [e for e in events if e.phase == game_state.current_phase and e.active]
        if available_events and random.random() < 0.3:  # 30% шанс события
            return random.choice(available_events)
        return None
    
    # Главный игровой цикл
    running = True
    intro_timer = 120
    
    while running:
        dt = clock.tick(60)
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                
                # Обработка выбора в событии
                if current_event:
                    if event.key == pygame.K_UP:
                        selected_choice = (selected_choice - 1) % len(current_event.choices)
                    elif event.key == pygame.K_DOWN:
                        selected_choice = (selected_choice + 1) % len(current_event.choices)
                    elif event.key == pygame.K_RETURN:
                        # Применить выбранный эффект
                        apply_choice_effects(current_event.choices[selected_choice])
                        current_event = None
                        selected_choice = 0
        
        # Обновление
        if intro_timer > 0:
            intro_timer -= 1
        else:
            # Обновление игрового состояния
            game_result = update_game_state()
            
            if game_result != "continue":
                # Конец игры
                overlay = pygame.Surface((W, H), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 200))
                window.blit(overlay, (0, 0))
                
                if game_result == "completed":
                    # Победа
                    final_score = (game_state.score + 
                                 int(game_state.resources['product_quality']) * 10 +
                                 int(game_state.resources['market_fit']) * 15 +
                                 int(game_state.resources['investor_interest']) * 20)
                    
                    victory_text = font_huge.render("ЕДИНОРОГ СОЗДАН!", True, NFACT_GREEN)
                    window.blit(victory_text, (W // 2 - victory_text.get_width() // 2, H // 2 - 100))
                    
                    score_text = font_large.render(f"Финальный счет: {final_score}", True, GOLD)
                    window.blit(score_text, (W // 2 - score_text.get_width() // 2, H // 2 - 50))
                    
                    success_text = font_medium.render("Поздравляем с успешным прохождением инкубатора!", True, WHITE)
                    window.blit(success_text, (W // 2 - success_text.get_width() // 2, H // 2))
                    
                    pygame.display.flip()
                    pygame.time.wait(4000)
                    return True
                
                else:
                    # Поражение
                    failure_reasons = {
                        "exhausted": "Вы выгорели от переработок!",
                        "team_quit": "Команда покинула проект!",
                        "bankrupt": "Закончились деньги!"
                    }
                    
                    failure_text = font_huge.render("ПРОВАЛ!", True, NFACT_RED)
                    window.blit(failure_text, (W // 2 - failure_text.get_width() // 2, H // 2 - 100))
                    
                    reason_text = font_large.render(failure_reasons[game_result], True, WHITE)
                    window.blit(reason_text, (W // 2 - reason_text.get_width() // 2, H // 2 - 50))
                    
                    score_text = font_medium.render(f"Финальный счет: {game_state.score}", True, LIGHT_GRAY)
                    window.blit(score_text, (W // 2 - score_text.get_width() // 2, H // 2))
                    
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    return False
            
            # Генерация случайных событий
            if not current_event:
                event_timer += 1
                if event_timer >= 300:  # Каждые 5 секунд
                    event_timer = 0
                    current_event = get_random_event()
        
        # Обновление частиц
        particle_system.update()
        
        # Отрисовка
        draw_gradient_background(window)
        
        # Логотип
        window.blit(logo, (W // 2 - 30, H - 80))
        
        # Интро
        if intro_timer > 0:
            intro_text = font_huge.render("INCUBATOR JOURNEY", True, NFACT_ORANGE)
            window.blit(intro_text, (W // 2 - intro_text.get_width() // 2, H // 2 - 100))
            
            subtitle_text = font_large.render("Пройди путь от идеи до единорога!", True, WHITE)
            window.blit(subtitle_text, (W // 2 - subtitle_text.get_width() // 2, H // 2 - 50))
            
            loading_text = font_medium.render("Загрузка...", True, LIGHT_GRAY)
            window.blit(loading_text, (W // 2 - loading_text.get_width() // 2, H // 2 + 50))
        
        else:
            # Основной интерфейс
            draw_phase_info(window)
            draw_resources(window)
            draw_team_info(window)
            draw_score(window)
            
            # Событие
            if current_event:
                draw_event(window, current_event)
            
            # Частицы
            particle_system.draw(window)
            
            # Индикаторы критических состояний
            if game_state.resources['energy'] < 30:
                warning_text = font_small.render("⚠️ НИЗКАЯ ЭНЕРГИЯ", True, NFACT_RED)
                window.blit(warning_text, (20, H - 100))
            
            if game_state.resources['team_morale'] < 30:
                warning_text = font_small.render("⚠️ НИЗКАЯ МОРАЛЬ КОМАНДЫ", True, NFACT_RED)
                window.blit(warning_text, (20, H - 80))
            
            if game_state.resources['money'] < 100:
                warning_text = font_small.render("⚠️ МАЛО ДЕНЕГ", True, NFACT_RED)
                window.blit(warning_text, (20, H - 60))
            
            # Подсказки для новичков
            if game_state.decisions_made < 3:
                hint_text = font_small.render("Принимайте решения в событиях для прогресса!", True, LIGHT_GRAY)
                window.blit(hint_text, (W // 2 - hint_text.get_width() // 2, H - 40))
            
            # Прогресс через все фазы
            total_phases = len(GamePhase)
            current_phase_num = list(GamePhase).index(game_state.current_phase) + 1
            
            phase_progress_text = font_small.render(f"Фаза {current_phase_num}/{total_phases}", True, WHITE)
            window.blit(phase_progress_text, (W // 2 - phase_progress_text.get_width() // 2, 60))
            
            # Мини-карта прогресса
            minimap_x = 50
            minimap_y = 120
            minimap_width = 400
            phase_width = minimap_width // total_phases
            
            for i, phase in enumerate(GamePhase):
                rect_x = minimap_x + i * phase_width
                rect_y = minimap_y
                rect_width = phase_width - 2
                rect_height = 20
                
                if i < current_phase_num - 1:
                    # Завершенные фазы
                    color = NFACT_GREEN
                elif i == current_phase_num - 1:
                    # Текущая фаза
                    color = PHASE_CONFIG[game_state.current_phase]['color']
                    # Показать прогресс внутри фазы
                    progress_width = int(rect_width * (game_state.phase_progress / 100))
                    pygame.draw.rect(window, color, (rect_x, rect_y, progress_width, rect_height))
                    pygame.draw.rect(window, DARK_BG, (rect_x + progress_width, rect_y, rect_width - progress_width, rect_height))
                else:
                    # Будущие фазы
                    color = DARK_BG
                
                if i != current_phase_num - 1:
                    pygame.draw.rect(window, color, (rect_x, rect_y, rect_width, rect_height))
                
                # Рамка
                pygame.draw.rect(window, WHITE, (rect_x, rect_y, rect_width, rect_height), 1)
                
                # Название фазы (сокращенно)
                phase_names = {
                    GamePhase.IDEA: "Идея",
                    GamePhase.TEAM_BUILDING: "Команда",
                    GamePhase.DEVELOPMENT: "Разработка",
                    GamePhase.TESTING: "Тесты",
                    GamePhase.PITCH: "Питч",
                    GamePhase.SCALING: "Рост",
                    GamePhase.DEMO_DAY: "Demo"
                }
                
                phase_name = phase_names[phase]
                name_text = font_small.render(phase_name, True, WHITE)
                text_rect = name_text.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height + 15))
                window.blit(name_text, text_rect)
            
            # Достижения
            achievements_to_check = [
                ("Первые шаги", "Сделайте первое решение", game_state.decisions_made >= 1),
                ("Командный игрок", "Соберите команду из 3+ человек", game_state.team_size >= 3),
                ("Качественный продукт", "Достигните 80% качества продукта", game_state.resources['product_quality'] >= 80),
                ("Рыночное соответствие", "Достигните 70% market fit", game_state.resources['market_fit'] >= 70),
                ("Привлекательный для инвесторов", "Достигните 60% интереса инвесторов", game_state.resources['investor_interest'] >= 60),
                ("Решитель проблем", "Решите 10 проблем", game_state.decisions_made >= 10),
                ("Энергичный", "Поддерживайте энергию выше 70%", game_state.resources['energy'] > 70),
                ("Мотиватор", "Поддерживайте мораль команды выше 80%", game_state.resources['team_morale'] > 80)
            ]
            
            # Проверка новых достижений
            for name, desc, condition in achievements_to_check:
                if condition and name not in game_state.achievements:
                    game_state.achievements.append(name)
                    game_state.score += 50
                    particle_system.add_effect(W // 2, H // 2, "quality", 50)
            
            # Отображение достижений
            if game_state.achievements:
                achievement_text = font_small.render(f"Достижения: {len(game_state.achievements)}/8", True, GOLD)
                window.blit(achievement_text, (W - 200, H - 40))
            
            # Специальные эффекты для критических моментов
            if game_state.current_phase == GamePhase.DEMO_DAY:
                # Эффект для Demo Day
                demo_glow = pygame.Surface((W, H), pygame.SRCALPHA)
                alpha = int(30 * abs(math.sin(pygame.time.get_ticks() * 0.005)))
                demo_glow.fill((255, 20, 147, 0))
                demo_glow.set_alpha(alpha)
                window.blit(demo_glow, (0, 0))
            
            # Мигание при критически низких ресурсах
            if game_state.resources['energy'] < 20 or game_state.resources['team_morale'] < 20:
                danger_overlay = pygame.Surface((W, H), pygame.SRCALPHA)
                danger_alpha = int(50 * abs(math.sin(pygame.time.get_ticks() * 0.01)))
                danger_overlay.fill((255, 0, 0, 0))
                danger_overlay.set_alpha(danger_alpha)
                window.blit(danger_overlay, (0, 0))
            
            # Статистика в углу
            stats_y = H - 120
            stats_text = [
                f"Решений принято: {game_state.decisions_made}",
                f"Размер команды: {game_state.team_size}",
                f"Время в игре: {(pygame.time.get_ticks() - game_state.phase_start_time) // 1000}с"
            ]
            
            for i, stat in enumerate(stats_text):
                stat_surface = font_small.render(stat, True, LIGHT_GRAY)
                window.blit(stat_surface, (W - 250, stats_y + i * 20))
        
        pygame.display.flip()
    
    return False