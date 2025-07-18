import pygame
import os
import math
from .base_scene import BaseScene

class DaylickScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x = self.screen_width * 0.5
        self.player_y = self.screen_height * 0.7
        self.player_speed = 5
        
        # Система уведомлений от Алихана
        self.notification_active = False
        self.notification_timer = 0
        self.notification_duration = 5000  # 5 секунд на уведомление
        self.notification_shown = False
        
        # Система сообщений от персонажей
        self.character_message_active = False
        self.character_message_timer = 0
        self.character_message_duration = 3000  # 3 секунды на сообщение
        self.current_character = None
        self.character_messages = {
            'ochkarik': "",
            'omar': "я тот самый школьник из Каскелена",
            'taqyrbas': "Мен Асхат 137 БАЛЛ",
            'tuka': "Ішеміз ба? ",
            'armansu': "Армансу! Всегда готов к работе!"
        }
        
        # Загрузка изображений
        self.ceo_image = None
        self.daylick_image = None
        self.alikhan_image = None
        self.ochkarik_image = None
        self.omar_image = None
        self.taqyrbas_image = None
        self.tuka_image = None
        self.armansu_image = None
        self.load_images()
        
    def load_images(self):
        try:
            self.ceo_image = pygame.image.load(os.path.join('public', 'ceo.png'))
            self.ceo_image = pygame.transform.scale(self.ceo_image, (250, 350))
            
            self.daylick_image = pygame.image.load(os.path.join('public', 'daylick.jpeg'))
            self.daylick_image = pygame.transform.scale(self.daylick_image, (self.screen_width, self.screen_height))
            
            # Загрузка новых изображений
            self.alikhan_image = pygame.image.load(os.path.join('public', 'alikhan.png'))
            self.alikhan_image = pygame.transform.scale(self.alikhan_image, (300, 450))  # Увеличил Алихана
            
            self.ochkarik_image = pygame.image.load(os.path.join('public', 'ochkarik.png'))
            self.ochkarik_image = pygame.transform.scale(self.ochkarik_image, (100, 150))  # Уменьшил
            
            self.omar_image = pygame.image.load(os.path.join('public', 'omar.png'))
            self.omar_image = pygame.transform.scale(self.omar_image, (100, 150))  # Уменьшил
            
            self.taqyrbas_image = pygame.image.load(os.path.join('public', 'taqyrbas.png'))
            self.taqyrbas_image = pygame.transform.scale(self.taqyrbas_image, (100, 150))  # Уменьшил
            
            self.tuka_image = pygame.image.load(os.path.join('public', 'tuka.png'))
            self.tuka_image = pygame.transform.scale(self.tuka_image, (100, 150))  # Уменьшил
            
            self.armansu_image = pygame.image.load(os.path.join('public', 'armansu.png'))
            self.armansu_image = pygame.transform.scale(self.armansu_image, (100, 150))  # Добавил Армансу
            
        except pygame.error as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки
            self.ceo_image = pygame.Surface((250, 350))
            self.ceo_image.fill((100, 150, 200))
            
            self.daylick_image = pygame.Surface((self.screen_width, self.screen_height))
            self.daylick_image.fill((70, 110, 150))
            
            self.alikhan_image = pygame.Surface((300, 450))
            self.alikhan_image.fill((150, 100, 100))
            
            self.ochkarik_image = pygame.Surface((100, 150))
            self.ochkarik_image.fill((100, 150, 100))
            
            self.omar_image = pygame.Surface((100, 150))
            self.omar_image.fill((100, 100, 150))
            
            self.taqyrbas_image = pygame.Surface((100, 150))
            self.taqyrbas_image.fill((150, 150, 100))
            
            self.tuka_image = pygame.Surface((100, 150))
            self.tuka_image.fill((150, 100, 150))
            
            self.armansu_image = pygame.Surface((100, 150))
            self.armansu_image.fill((100, 100, 100))
    
    def reset(self, data=None):
        self.player_x = self.screen_width * 0.5
        self.player_y = self.screen_height * 0.7
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.notification_active:
                # ESC или X закрывает уведомление
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_x:
                    self.notification_active = False
                    self.notification_timer = 0
                    self.notification_shown = False
                    return
            
            if self.character_message_active:
                # ESC или X закрывает сообщение персонажа
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_x:
                    self.character_message_active = False
                    self.character_message_timer = 0
                    self.current_character = None
                    return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.notification_active:
                # Клик в любом месте закрывает уведомление
                self.notification_active = False
                self.notification_timer = 0
                self.notification_shown = False
                return
            
            if self.character_message_active:
                # Клик в любом месте закрывает сообщение персонажа
                self.character_message_active = False
                self.character_message_timer = 0
                self.current_character = None
                return
            
            # Проверка клика по персонажам
            mouse_pos = pygame.mouse.get_pos()
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            radius = 200
            
            # Проверяем клик по каждому персонажу
            characters = [
                ('ochkarik', 0),      # Вверху
                ('omar', 60),         # Справа-вверх
                ('taqyrbas', 120),    # Справа-вниз
                ('tuka', 180),        # Внизу
                ('armansu', 240),     # Слева-вниз
            ]
            
            for character_name, angle in characters:
                import math
                rad_angle = math.radians(angle)
                char_x = center_x + radius * math.cos(rad_angle) - 50  # 50 = половина ширины персонажа
                char_y = center_y + radius * math.sin(rad_angle) - 75  # 75 = половина высоты персонажа
                
                # Проверяем, попал ли клик в область персонажа
                if (char_x <= mouse_pos[0] <= char_x + 100 and 
                    char_y <= mouse_pos[1] <= char_y + 150):
                    print(f"Клик по персонажу: {character_name}")
                    self.character_message_active = True
                    self.character_message_timer = 0
                    self.current_character = character_name
                    return
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_y += self.player_speed
        
        # Ограничение движения игрока
        self.player_x = max(125, min(self.screen_width - 125, self.player_x))
        self.player_y = max(175, min(self.screen_height - 175, self.player_y))
        
        # Проверка близости к Алихану для активации уведомления
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        alikhan_center_x = center_x
        alikhan_center_y = center_y
        
        distance_alikhan = ((self.player_x - alikhan_center_x) ** 2 + (self.player_y - alikhan_center_y) ** 2) ** 0.5
        
        # Активация уведомления при приближении к Алихану
        if distance_alikhan < 300 and not self.notification_active and not self.notification_shown:
            print(f"Уведомление от Алихана активировано! Расстояние: {distance_alikhan}")
            self.notification_active = True
            self.notification_timer = 0
            self.notification_shown = True
        
        # Обновление таймера уведомления
        if self.notification_active:
            self.notification_timer += dt
            if self.notification_timer >= self.notification_duration:
                # Автоматическое закрытие уведомления через 5 секунд
                self.notification_active = False
                self.notification_timer = 0
        
        # Обновление таймера сообщений персонажей
        if self.character_message_active:
            self.character_message_timer += dt
            if self.character_message_timer >= self.character_message_duration:
                # Автоматическое закрытие сообщения через 3 секунды
                self.character_message_active = False
                self.character_message_timer = 0
                self.current_character = None
        
        # Возврат назад по ESC
        if keys[pygame.K_ESCAPE]:
            self.go_back()
    
    def draw(self, screen):
        # Фон
        if self.daylick_image:
            screen.blit(self.daylick_image, (0, 0))
        else:
            screen.fill((70, 110, 150))
        
        # Центр экрана для размещения персонажей
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Алихан в центре
        if self.alikhan_image:
            alikhan_x = center_x - self.alikhan_image.get_width() // 2
            alikhan_y = center_y - self.alikhan_image.get_height() // 2
            screen.blit(self.alikhan_image, (alikhan_x, alikhan_y))
        
        # Персонажи вокруг Алихана (по кругу)
        radius = 200  # Радиус круга
        characters = [
            (self.ochkarik_image, 0),      # Вверху
            (self.omar_image, 60),         # Справа-вверх
            (self.taqyrbas_image, 120),    # Справа-вниз
            (self.tuka_image, 180),        # Внизу
            (self.armansu_image, 240),     # Слева-вниз
        ]
        
        for character_image, angle in characters:
            if character_image:
                # Вычисляем позицию на круге
                rad_angle = math.radians(angle)
                char_x = center_x + radius * math.cos(rad_angle) - character_image.get_width() // 2
                char_y = center_y + radius * math.sin(rad_angle) - character_image.get_height() // 2
                screen.blit(character_image, (char_x, char_y))
        
        # Игрок
        if self.ceo_image:
            screen.blit(self.ceo_image, (self.player_x - 125, self.player_y - 175))
        else:
            pygame.draw.rect(screen, (100, 150, 200), 
                           (self.player_x - 125, self.player_y - 175, 250, 350))
        
        # Текст подсказки
        hint_text = self.small_font.render('ESC - Вернуться назад', True, (255, 255, 255))
        screen.blit(hint_text, (10, 10))
        
        # Подсказка о клавише ESC
        self.draw_esc_hint(screen)
        
        # Отрисовка уведомления от Алихана
        if self.notification_active:
            # Фон уведомления (уменьшенный размер)
            notification_width = 400
            notification_height = 120
            notification_x = (self.screen_width - notification_width) // 2
            notification_y = center_y - 300  # Выше Алихана
            
            # Темный фон с градиентом
            notification_surface = pygame.Surface((notification_width, notification_height))
            notification_surface.fill((20, 20, 30))
            
            # Рамка
            pygame.draw.rect(notification_surface, (100, 80, 120), (0, 0, notification_width, notification_height), 3)
            pygame.draw.rect(notification_surface, (60, 40, 80), (3, 3, notification_width-6, notification_height-6), 2)
            
            screen.blit(notification_surface, (notification_x, notification_y))
            
            # Заголовок
            title_text = self.small_font.render("Алихан:", True, (255, 200, 100))
            screen.blit(title_text, (notification_x + 15, notification_y + 15))
            
            # Сообщение
            message_text = self.small_font.render("Кто че сделал рассказывайте", True, (220, 220, 220))
            screen.blit(message_text, (notification_x + 15, notification_y + 40))
            
            # Инструкция для закрытия
            instruction_text = self.small_font.render("ESC, X или клик для закрытия", True, (150, 150, 150))
            screen.blit(instruction_text, (notification_x + 15, notification_y + 65))
            
            # Таймер (показывает оставшееся время)
            remaining_time = max(0, (self.notification_duration - self.notification_timer) / 1000)
            timer_text = self.small_font.render(f"Автозакрытие: {remaining_time:.1f}с", True, (150, 150, 150))
            screen.blit(timer_text, (notification_x + 15, notification_y + 85))
        
        # Отрисовка сообщений от персонажей
        if self.character_message_active and self.current_character:
            # Фон сообщения (компактный размер)
            message_width = 350
            message_height = 100
            message_x = (self.screen_width - message_width) // 2
            message_y = center_y - 200  # Выше персонажей
            
            # Темный фон с градиентом
            message_surface = pygame.Surface((message_width, message_height))
            message_surface.fill((20, 20, 30))
            
            # Рамка
            pygame.draw.rect(message_surface, (100, 80, 120), (0, 0, message_width, message_height), 3)
            pygame.draw.rect(message_surface, (60, 40, 80), (3, 3, message_width-6, message_height-6), 2)
            
            screen.blit(message_surface, (message_x, message_y))
            
            # Имя персонажа
            character_names = {
                'ochkarik': 'Очкарик',
                'omar': 'Омар',
                'taqyrbas': 'Тақырбас',
                'tuka': 'Тука',
                'armansu': 'Армансу'
            }
            
            name_text = self.small_font.render(f"{character_names[self.current_character]}:", True, (255, 200, 100))
            screen.blit(name_text, (message_x + 15, message_y + 15))
            
            # Сообщение персонажа
            message_text = self.small_font.render(self.character_messages[self.current_character], True, (220, 220, 220))
            screen.blit(message_text, (message_x + 15, message_y + 40))
            
            # Инструкция для закрытия
            instruction_text = self.small_font.render("ESC, X или клик для закрытия", True, (150, 150, 150))
            screen.blit(instruction_text, (message_x + 15, message_y + 65))
            
            # Таймер
            remaining_time = max(0, (self.character_message_duration - self.character_message_timer) / 1000)
            timer_text = self.small_font.render(f"Автозакрытие: {remaining_time:.1f}с", True, (150, 150, 150))
            screen.blit(timer_text, (message_x + 15, message_y + 80)) 