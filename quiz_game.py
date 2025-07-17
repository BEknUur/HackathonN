import pygame
import random
import math
import time
import pathlib
from typing import List, Dict, Tuple

def main(window):
    """
    Epic Quiz Game — nFactorial Edition
    Эпичная битва с ментором через вопросы с анимациями и эффектами!
    """
    pygame.display.set_caption("Epic Quiz Battle — nFactorial Edition")
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
    
    # Шрифты
    try:
        base = pathlib.Path(__file__).parent.resolve()
        font_path = str(base / "assets" / "dogica.ttf")
        font_small = pygame.font.Font(font_path, 20)
        font_medium = pygame.font.Font(font_path, 28)
        font_large = pygame.font.Font(font_path, 36)
        font_huge = pygame.font.Font(font_path, 48)
    except:
        font_small = pygame.font.Font(None, 24)
        font_medium = pygame.font.Font(None, 32)
        font_large = pygame.font.Font(None, 40)
        font_huge = pygame.font.Font(None, 56)
    
    # Логотип
    try:
        logo = pygame.image.load(str(base / "assets" / "logo.png")).convert_alpha()
        logo = pygame.transform.smoothscale(logo, (80, 80))
    except:
        logo = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(logo, NFACT_BLUE, (40, 40), 38)
        pygame.draw.circle(logo, WHITE, (40, 40), 28)
        text = font_medium.render("nF", True, NFACT_BLUE)
        logo.blit(text, (25, 25))
    
    # Система частиц
    class Particle:
        def __init__(self, x: float, y: float, vx: float, vy: float, color: Tuple[int, int, int], size: int = 3, life: int = 60):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.color = color
            self.size = size
            self.life = life
            self.max_life = life
            self.gravity = 0.1
        
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity
            self.life -= 1
            self.size = max(1, int(self.size * (self.life / self.max_life)))
        
        def draw(self, surface):
            if self.life > 0:
                alpha = int(255 * (self.life / self.max_life))
                try:
                    pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
                except:
                    pass
    
    class ParticleSystem:
        def __init__(self):
            self.particles = []
        
        def add_explosion(self, x: float, y: float, color: Tuple[int, int, int], count: int = 20):
            for _ in range(count):
                vx = random.uniform(-8, 8)
                vy = random.uniform(-12, -2)
                size = random.randint(2, 6)
                life = random.randint(40, 80)
                self.particles.append(Particle(x, y, vx, vy, color, size, life))
        
        def add_sparkle(self, x: float, y: float, color: Tuple[int, int, int]):
            for _ in range(10):
                vx = random.uniform(-4, 4)
                vy = random.uniform(-6, -1)
                self.particles.append(Particle(x, y, vx, vy, color, 2, 40))
        
        def update(self):
            self.particles = [p for p in self.particles if p.life > 0]
            for particle in self.particles:
                particle.update()
        
        def draw(self, surface):
            for particle in self.particles:
                particle.draw(surface)
    
    # Персонаж игрока
    class Player:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y
            self.max_hp = 5
            self.hp = self.max_hp
            self.attack_animation = 0
            self.hurt_animation = 0
            self.victory_animation = 0
            self.size = 80
            self.bounce = 0
        
        def take_damage(self):
            self.hp -= 1
            self.hurt_animation = 30
        
        def attack(self):
            self.attack_animation = 20
        
        def victory(self):
            self.victory_animation = 120
        
        def update(self):
            if self.attack_animation > 0:
                self.attack_animation -= 1
            if self.hurt_animation > 0:
                self.hurt_animation -= 1
            if self.victory_animation > 0:
                self.victory_animation -= 1
            
            self.bounce += 0.1
        
        def draw(self, surface):
            # Эффект атаки
            if self.attack_animation > 0:
                glow_size = int(self.size * 1.5)
                glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*NFACT_GREEN, 100), (glow_size//2, glow_size//2), glow_size//2)
                surface.blit(glow_surface, (self.x - glow_size//2, self.y - glow_size//2))
            
            # Эффект урона
            if self.hurt_animation > 0:
                if self.hurt_animation % 6 < 3:
                    color = NFACT_RED
                else:
                    color = NFACT_BLUE
            else:
                color = NFACT_BLUE
            
            # Подпрыгивание
            y_offset = int(math.sin(self.bounce) * 3)
            
            # Тело персонажа
            body_rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2 + y_offset, self.size, self.size)
            pygame.draw.ellipse(surface, color, body_rect)
            pygame.draw.ellipse(surface, WHITE, body_rect, 3)
            
            # Лицо
            eye_y = self.y - 10 + y_offset
            pygame.draw.circle(surface, BLACK, (self.x - 15, eye_y), 4)
            pygame.draw.circle(surface, BLACK, (self.x + 15, eye_y), 4)
            
            # Рот (меняется при атаке)
            if self.attack_animation > 0:
                mouth_points = [(self.x - 15, self.y + 10 + y_offset), (self.x, self.y + 5 + y_offset), (self.x + 15, self.y + 10 + y_offset)]
                pygame.draw.polygon(surface, BLACK, mouth_points)
            else:
                pygame.draw.arc(surface, BLACK, (self.x - 15, self.y + 5 + y_offset, 30, 15), 0, math.pi, 2)
    
    # Ментор-босс
    class Mentor:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y
            self.max_hp = 5
            self.hp = self.max_hp
            self.attack_animation = 0
            self.hurt_animation = 0
            self.death_animation = 0
            self.size = 100
            self.hover = 0
            self.angry_level = 0
        
        def take_damage(self):
            self.hp -= 1
            self.hurt_animation = 30
            self.angry_level = min(self.angry_level + 1, 3)
        
        def attack(self):
            self.attack_animation = 25
        
        def die(self):
            self.death_animation = 60
        
        def update(self):
            if self.attack_animation > 0:
                self.attack_animation -= 1
            if self.hurt_animation > 0:
                self.hurt_animation -= 1
            if self.death_animation > 0:
                self.death_animation -= 1
            
            self.hover += 0.08
        
        def draw(self, surface):
            # Эффект смерти
            if self.death_animation > 0:
                alpha = int(255 * (self.death_animation / 60))
                death_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.circle(death_surface, (*NFACT_RED, alpha), (self.size, self.size), self.size)
                surface.blit(death_surface, (self.x - self.size, self.y - self.size))
                return
            
            # Эффект атаки
            if self.attack_animation > 0:
                glow_size = int(self.size * 1.8)
                glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*NFACT_RED, 120), (glow_size//2, glow_size//2), glow_size//2)
                surface.blit(glow_surface, (self.x - glow_size//2, self.y - glow_size//2))
            
            # Цвет зависит от уровня злости
            if self.angry_level == 0:
                color = (100, 100, 200)
            elif self.angry_level == 1:
                color = (150, 100, 100)
            elif self.angry_level == 2:
                color = (200, 80, 80)
            else:
                color = NFACT_RED
            
            # Эффект урона
            if self.hurt_animation > 0 and self.hurt_animation % 6 < 3:
                color = WHITE
            
            # Парение
            y_offset = int(math.sin(self.hover) * 5)
            
            # Тело ментора
            body_rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2 + y_offset, self.size, self.size)
            pygame.draw.ellipse(surface, color, body_rect)
            pygame.draw.ellipse(surface, BLACK, body_rect, 4)
            
            # Страшные глаза
            eye_y = self.y - 20 + y_offset
            pygame.draw.circle(surface, NFACT_RED, (self.x - 20, eye_y), 6)
            pygame.draw.circle(surface, NFACT_RED, (self.x + 20, eye_y), 6)
            pygame.draw.circle(surface, BLACK, (self.x - 20, eye_y), 3)
            pygame.draw.circle(surface, BLACK, (self.x + 20, eye_y), 3)
            
            # Злой рот
            mouth_points = [(self.x - 25, self.y + 15 + y_offset), (self.x, self.y + 25 + y_offset), (self.x + 25, self.y + 15 + y_offset)]
            pygame.draw.polygon(surface, BLACK, mouth_points)
            
            # Рога при высокой злости
            if self.angry_level >= 2:
                horn_points1 = [(self.x - 30, self.y - 40 + y_offset), (self.x - 20, self.y - 60 + y_offset), (self.x - 10, self.y - 45 + y_offset)]
                horn_points2 = [(self.x + 30, self.y - 40 + y_offset), (self.x + 20, self.y - 60 + y_offset), (self.x + 10, self.y - 45 + y_offset)]
                pygame.draw.polygon(surface, BLACK, horn_points1)
                pygame.draw.polygon(surface, BLACK, horn_points2)
    
    # Эпичные вопросы про nFactorial
    QUESTIONS = [
        {
            "q": "Что означает 'pp2ease' в коде sleep_game.py?",
            "opts": ["Please Please To Ease", "Программирование для лентяев", "Просыпаться, пожалуйста!", "Покупай пиццу, товарищ!"],
            "correct": 2,
            "explanation": "Это игра слов: 'Please' звучит как 'pp2ease'!"
        },
        {
            "q": "Какой мем студенты nFactorial используют чаще всего?",
            "opts": ["Distracted Boyfriend", "This is Fine", "Это фиаско, братан", "Pepe the Frog"],
            "correct": 2,
            "explanation": "Классика российского мемоделия!"
        },
        {
            "q": "Что делает функция click_event() в student.py?",
            "opts": ["Удаляет студента", "Будит спящего студента", "Меняет спрайт", "Играет звук"],
            "correct": 1,
            "explanation": "Клик по спящему студенту восстанавливает его энергию!"
        },
        {
            "q": "Какой звук играет при успешном пробуждении студента?",
            "opts": ["blip.mp3", "success.mp3", "fail.mp3", "jojo.mp3"],
            "correct": 0,
            "explanation": "blip.mp3 - звук успешного действия!"
        },
        {
            "q": "Сколько кадров в анимации преподавателя?",
            "opts": ["24", "30", "42", "60"],
            "correct": 2,
            "explanation": "42 кадра - отсылка к 'Автостопом по галактике'!"
        },
        {
            "q": "Какая музыка НЕ играет в sleep_game.py?",
            "opts": ["C418 - Sweden", "Rick Roll", "Undertale Shop", "Megalovania"],
            "correct": 3,
            "explanation": "Megalovania не входит в плейлист игры!"
        },
        {
            "q": "Что происходит каждые 20 секунд в sleep_game.py?",
            "opts": ["Добавляется студент", "Увеличивается скорость", "Меняется музыка", "Появляется бонус"],
            "correct": 1,
            "explanation": "Игра становится сложнее со временем!"
        },
        {
            "q": "Как называется главное окно игры?",
            "opts": ["nFactorial Game", "Wake up, pp2ease!", "Sleep Simulator", "Student Manager"],
            "correct": 1,
            "explanation": "Заголовок окна содержит эпичное обращение!"
        },
        {
            "q": "Какой язык программирования используется в проекте?",
            "opts": ["JavaScript", "Java", "Python", "C++"],
            "correct": 2,
            "explanation": "Весь проект написан на Python с pygame!"
        },
        {
            "q": "Что означает победа в sleep_game.py?",
            "opts": ["Все студенты уснули", "Прошло 120 секунд", "Собрано 100 очков", "Нажата кнопка победы"],
            "correct": 1,
            "explanation": "Нужно продержаться 2 минуты!"
        },
        {
            "q": "Какой шрифт используется в играх?",
            "opts": ["Arial", "Times New Roman", "Dogica", "Comic Sans"],
            "correct": 2,
            "explanation": "Dogica - пиксельный шрифт для ретро-стиля!"
        },
        {
            "q": "Что за персонаж K в студентах?",
            "opts": ["Кот", "Кодер", "Kelgenbayev", "Король"],
            "correct": 2,
            "explanation": "Отсылка к создателю или преподавателю!"
        }
    ]
    
    # Инициализация
    particle_system = ParticleSystem()
    player = Player(W // 4, H // 2)
    mentor = Mentor(3 * W // 4, H // 2)
    
    # Перемешиваем вопросы
    random.shuffle(QUESTIONS)
    current_question = 0
    selected_option = 0
    question_phase = "question"  # question, answered, explanation
    answer_timer = 0
    
    def draw_gradient_bg(surface):
        for y in range(H):
            ratio = y / H
            r = int(DARK_BG[0] * (1 - ratio) + (DARK_BG[0] * 0.5) * ratio)
            g = int(DARK_BG[1] * (1 - ratio) + (DARK_BG[1] * 0.5) * ratio)
            b = int(DARK_BG[2] * (1 - ratio) + (DARK_BG[2] * 0.8) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (W, y))
    
    def draw_hp_bars(surface):
        # HP игрока
        bar_width = 200
        bar_height = 20
        player_hp_ratio = player.hp / player.max_hp
        
        # Фон полоски
        pygame.draw.rect(surface, BLACK, (50, 50, bar_width, bar_height))
        # Полоска HP
        pygame.draw.rect(surface, NFACT_GREEN, (50, 50, int(bar_width * player_hp_ratio), bar_height))
        # Рамка
        pygame.draw.rect(surface, WHITE, (50, 50, bar_width, bar_height), 2)
        
        # Текст
        hp_text = font_small.render(f"Игрок: {player.hp}/{player.max_hp}", True, WHITE)
        surface.blit(hp_text, (50, 25))
        
        # HP ментора
        mentor_hp_ratio = mentor.hp / mentor.max_hp
        mentor_x = W - 50 - bar_width
        
        # Фон полоски
        pygame.draw.rect(surface, BLACK, (mentor_x, 50, bar_width, bar_height))
        # Полоска HP
        pygame.draw.rect(surface, NFACT_RED, (mentor_x, 50, int(bar_width * mentor_hp_ratio), bar_height))
        # Рамка
        pygame.draw.rect(surface, WHITE, (mentor_x, 50, bar_width, bar_height), 2)
        
        # Текст
        mentor_hp_text = font_small.render(f"Ментор: {mentor.hp}/{mentor.max_hp}", True, WHITE)
        surface.blit(mentor_hp_text, (mentor_x, 25))
    
    def draw_question(surface):
        if current_question >= len(QUESTIONS):
            return
        
        question = QUESTIONS[current_question]
        
        # Фон вопроса
        question_bg = pygame.Surface((W - 100, 300), pygame.SRCALPHA)
        question_bg.fill((0, 0, 0, 180))
        surface.blit(question_bg, (50, H - 350))
        
        # Номер вопроса
        q_num_text = font_medium.render(f"Вопрос {current_question + 1}/{len(QUESTIONS)}", True, NFACT_ORANGE)
        surface.blit(q_num_text, (70, H - 330))
        
        # Текст вопроса
        q_text = font_medium.render(question["q"], True, WHITE)
        surface.blit(q_text, (70, H - 300))
        
        # Варианты ответов
        for i, option in enumerate(question["opts"]):
            color = WHITE
            bg_color = None
            
            if question_phase == "question":
                if i == selected_option:
                    color = NFACT_ORANGE
                    bg_color = (50, 50, 50)
            elif question_phase == "answered":
                if i == question["correct"]:
                    color = NFACT_GREEN
                    bg_color = (0, 100, 0)
                elif i == selected_option and i != question["correct"]:
                    color = NFACT_RED
                    bg_color = (100, 0, 0)
            
            y_pos = H - 250 + i * 35
            
            # Подсветка выбранного варианта
            if bg_color:
                highlight_rect = pygame.Rect(70, y_pos - 5, W - 140, 30)
                pygame.draw.rect(surface, bg_color, highlight_rect)
            
            opt_text = font_small.render(f"{i + 1}. {option}", True, color)
            surface.blit(opt_text, (90, y_pos))
        
        # Объяснение
        if question_phase == "explanation":
            explanation_text = font_small.render(question["explanation"], True, NFACT_BLUE)
            surface.blit(explanation_text, (70, H - 120))
    
    def draw_battle_effects(surface):
        # Молнии при атаке
        if player.attack_animation > 0:
            for _ in range(5):
                x1 = player.x + random.randint(-30, 30)
                y1 = player.y + random.randint(-30, 30)
                x2 = mentor.x + random.randint(-30, 30)
                y2 = mentor.y + random.randint(-30, 30)
                pygame.draw.line(surface, NFACT_GREEN, (x1, y1), (x2, y2), 3)
        
        if mentor.attack_animation > 0:
            for _ in range(5):
                x1 = mentor.x + random.randint(-30, 30)
                y1 = mentor.y + random.randint(-30, 30)
                x2 = player.x + random.randint(-30, 30)
                y2 = player.y + random.randint(-30, 30)
                pygame.draw.line(surface, NFACT_RED, (x1, y1), (x2, y2), 3)
    
    # Вступительная анимация
    intro_timer = 180
    
    # Главный игровой цикл
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                
                if intro_timer <= 0 and question_phase == "question":
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % 4
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        selected_option = event.key - pygame.K_1
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Ответ дан
                        question = QUESTIONS[current_question]
                        if selected_option == question["correct"]:
                            # Правильный ответ
                            player.attack()
                            mentor.take_damage()
                            particle_system.add_explosion(mentor.x, mentor.y, NFACT_GREEN)
                            particle_system.add_sparkle(player.x, player.y, NFACT_BLUE)
                        else:
                            # Неправильный ответ
                            mentor.attack()
                            player.take_damage()
                            particle_system.add_explosion(player.x, player.y, NFACT_RED)
                        
                        question_phase = "answered"
                        answer_timer = 120
                
                elif question_phase == "explanation":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        current_question += 1
                        selected_option = 0
                        question_phase = "question"
                        
                        # Проверка окончания игры
                        if player.hp <= 0:
                            # Поражение
                            return False
                        elif mentor.hp <= 0:
                            # Победа
                            player.victory()
                            mentor.die()
                            return True
                        elif current_question >= len(QUESTIONS):
                            # Ничья
                            return player.hp > mentor.hp
        
        # Обновления
        if intro_timer > 0:
            intro_timer -= 1
        
        if answer_timer > 0:
            answer_timer -= 1
            if answer_timer <= 0:
                question_phase = "explanation"
        
        player.update()
        mentor.update()
        particle_system.update()
        
        # Отрисовка
        draw_gradient_bg(window)
        
        # Логотип
        window.blit(logo, (W // 2 - 40, 10))
        
        # Заголовок
        if intro_timer > 0:
            title_text = font_huge.render("QUIZ BATTLE!", True, NFACT_ORANGE)
            window.blit(title_text, (W // 2 - title_text.get_width() // 2, 100))
            
            subtitle_text = font_medium.render("Сразитесь с Ментором в интеллектуальной битве!", True, WHITE)
            window.blit(subtitle_text, (W // 2 - subtitle_text.get_width() // 2, 160))
            
            controls_text = font_small.render("Управление: ↑/↓ или 1-4 для выбора, ENTER для подтверждения", True, LIGHT_GRAY)
            window.blit(controls_text, (W // 2 - controls_text.get_width() // 2, 200))
        
        # Боевые эффекты
        draw_battle_effects(window)
        
        # Персонажи
        player.draw(window)
        mentor.draw(window)
        
        # Частицы
        particle_system.draw(window)
        
        # HP бары
        draw_hp_bars(window)
        
        # Вопрос
        if intro_timer <= 0 and current_question < len(QUESTIONS):
            draw_question(window)
        
        # Проверка окончания игры
        if player.hp <= 0:
            # Экран поражения
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            window.blit(overlay, (0, 0))
            
            defeat_text = font_huge.render("ПОРАЖЕНИЕ!", True, NFACT_RED)
            window.blit(defeat_text, (W // 2 - defeat_text.get_width() // 2, H // 2 - 50))
            
            subtitle_text = font_medium.render("Ментор кикнул вас из инкубатора!", True, WHITE)
            window.blit(subtitle_text, (W // 2 - subtitle_text.get_width() // 2, H // 2 + 10))
            
            pygame.display.flip()
            pygame.time.wait(3000)
            return False
        
        elif mentor.hp <= 0:
            # Экран победы
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            window.blit(overlay, (0, 0))
            
            victory_text = font_huge.render("ПОБЕДА!", True, NFACT_GREEN)
            window.blit(victory_text, (W // 2 - victory_text.get_width() // 2, H // 2 - 50))
            
            subtitle_text = font_medium.render("Вы победили Ментора! Проходите на Demo Day!", True, WHITE)
            window.blit(subtitle_text, (W // 2 - subtitle_text.get_width() // 2, H // 2 + 10))
            
            pygame.display.flip()
            pygame.time.wait(3000)
            return True
        
        elif current_question >= len(QUESTIONS):
            # Ничья
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            window.blit(overlay, (0, 0))
            
            if player.hp > mentor.hp:
                result_text = font_huge.render("ТЕХНИЧЕСКАЯ ПОБЕДА!", True, NFACT_GREEN)
                window.blit(result_text, (W // 2 - result_text.get_width() // 2, H // 2 - 50))
                
                subtitle_text = font_medium.render("У вас больше HP! Проходите дальше!", True, WHITE)
                window.blit(subtitle_text, (W // 2 - subtitle_text.get_width() // 2, H // 2 + 10))
                
                pygame.display.flip()
                pygame.time.wait(3000)
                return True
            
            elif mentor.hp > player.hp:
                result_text = font_huge.render("ТЕХНИЧЕСКОЕ ПОРАЖЕНИЕ!", True, NFACT_RED)
                window.blit(result_text, (W // 2 - result_text.get_width() // 2, H // 2 - 50))
                
                subtitle_text = font_medium.render("У Ментора больше HP! Попробуйте еще раз!", True, WHITE)
                window.blit(subtitle_text, (W // 2 - subtitle_text.get_width() // 2, H // 2 + 10))
                
                pygame.display.flip()
                pygame.time.wait(3000)
                return False
            
            else:
                result_text = font_huge.render("НИЧЬЯ!", True, NFACT_ORANGE)
                window.blit(result_text, (W // 2 - result_text.get_width() // 2, H // 2 - 50))
                
                subtitle_text = font_medium.render("Равные силы! Халява проходит!", True, WHITE)
                window.blit(subtitle_text, (W // 2 - subtitle_text.get_width() // 2, H // 2 + 10))
                
                pygame.display.flip()
                pygame.time.wait(3000)
                return True
        
        # Подсказки во время игры
        if intro_timer <= 0 and question_phase == "question":
            hint_text = font_small.render("Используйте ↑/↓ или 1-4 для выбора, ENTER для ответа", True, LIGHT_GRAY)
            window.blit(hint_text, (W // 2 - hint_text.get_width() // 2, H - 50))
        
        elif question_phase == "explanation":
            hint_text = font_small.render("Нажмите ENTER для следующего вопроса", True, LIGHT_GRAY)
            window.blit(hint_text, (W // 2 - hint_text.get_width() // 2, H - 50))
        
        # Дополнительные эффекты
        if player.victory_animation > 0:
            # Фейерверк победы
            for _ in range(3):
                x = random.randint(100, W - 100)
                y = random.randint(100, H // 2)
                particle_system.add_explosion(x, y, random.choice([NFACT_GREEN, NFACT_BLUE, NFACT_ORANGE]))
        
        if mentor.death_animation > 0:
            # Эффект смерти ментора
            particle_system.add_explosion(mentor.x, mentor.y, NFACT_RED, 5)
        
        # Мигающие границы экрана при низком HP
        if player.hp <= 1:
            border_alpha = int(100 * abs(math.sin(pygame.time.get_ticks() * 0.01)))
            border_surface = pygame.Surface((W, H), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, (*NFACT_RED, border_alpha), (0, 0, W, H), 10)
            window.blit(border_surface, (0, 0))
        
        if mentor.hp <= 1:
            border_alpha = int(80 * abs(math.sin(pygame.time.get_ticks() * 0.008)))
            border_surface = pygame.Surface((W, H), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, (*NFACT_ORANGE, border_alpha), (0, 0, W, H), 8)
            window.blit(border_surface, (0, 0))
        
        # Счетчик очков в углу
        score_text = font_small.render(f"Правильных ответов: {5 - mentor.hp}/5", True, WHITE)
        window.blit(score_text, (10, H - 30))
        
        # Прогресс вопросов
        progress_text = font_small.render(f"Вопрос: {current_question + 1}/{len(QUESTIONS)}", True, WHITE)
        window.blit(progress_text, (W - 200, H - 30))
        
        pygame.display.flip()
    
    return False