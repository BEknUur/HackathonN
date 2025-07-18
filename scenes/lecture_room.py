import pygame
import os
import math
from .base_scene import BaseScene

class LectureRoomScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x = self.screen_width * 0.25
        self.player_y = self.screen_height * 0.7
        self.player_speed = 5
        self.door_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height * 0.4 - 75, 100, 150)
        self.player_rotation = 0
        self.is_spinning = False
        self.spin_timer = 0
        self.dialog_active = False
        self.current_dialog = None
        self.dialog_timer = 0
        
        # NPC персонажи
        self.npcs = [
            {'x': self.screen_width * 0.8, 'y': self.screen_height * 0.2, 'speed': 3, 'strategy': 'direct', 'knocked_back': False, 'knockback_timer': 0},
            {'x': self.screen_width * 0.8 + 80, 'y': self.screen_height * 0.2 + 30, 'speed': 4, 'strategy': 'right', 'knocked_back': False, 'knockback_timer': 0},
            {'x': self.screen_width * 0.8 + 160, 'y': self.screen_height * 0.2 + 60, 'speed': 5, 'strategy': 'left', 'knocked_back': False, 'knockback_timer': 0}
        ]
        
        # Загрузка изображений
        self.ceo_image = None
        self.lecture_343_image = None
        self.npc_images = []
        self.load_images()
        
    def load_images(self):
        try:
            self.ceo_image = pygame.image.load(os.path.join('public', 'ceo.png'))
            self.ceo_image = pygame.transform.scale(self.ceo_image, (250, 350))
            
            self.lecture_343_image = pygame.image.load(os.path.join('public', '343.jpg'))
            self.lecture_343_image = pygame.transform.scale(self.lecture_343_image, (self.screen_width, self.screen_height))
            
            # Загрузка NPC изображений
            npc_files = ['bakhredin.png', 'tamirlan.png', 'alikhan.png']
            for npc_file in npc_files:
                try:
                    npc_img = pygame.image.load(os.path.join('public', npc_file))
                    npc_img = pygame.transform.scale(npc_img, (300, 420))  # Увеличили с 200x280 до 300x420
                    self.npc_images.append(npc_img)
                except pygame.error:
                    # Создаем заглушку
                    placeholder = pygame.Surface((300, 420))  # Увеличили размер заглушки
                    placeholder.fill((150, 100, 200))
                    self.npc_images.append(placeholder)
                    
        except pygame.error as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки
            self.ceo_image = pygame.Surface((250, 350))
            self.ceo_image.fill((100, 150, 200))
            
            self.lecture_343_image = pygame.Surface((self.screen_width, self.screen_height))
            self.lecture_343_image.fill((60, 100, 140))
            
            for _ in range(3):
                placeholder = pygame.Surface((300, 420))  # Увеличили размер заглушки
                placeholder.fill((150, 100, 200))
                self.npc_images.append(placeholder)
    
    def reset(self, data=None):
        self.player_x = self.screen_width * 0.25
        self.player_y = self.screen_height * 0.7
        self.player_rotation = 0
        self.is_spinning = False
        self.spin_timer = 0
        self.dialog_active = False
        self.current_dialog = None
        self.dialog_timer = 0
        
        # Сброс позиций NPC
        self.npcs = [
            {'x': self.screen_width * 0.8, 'y': self.screen_height * 0.2, 'speed': 3, 'strategy': 'direct', 'knocked_back': False, 'knockback_timer': 0},
            {'x': self.screen_width * 0.8 + 80, 'y': self.screen_height * 0.2 + 30, 'speed': 4, 'strategy': 'right', 'knocked_back': False, 'knockback_timer': 0},
            {'x': self.screen_width * 0.8 + 160, 'y': self.screen_height * 0.2 + 60, 'speed': 5, 'strategy': 'left', 'knocked_back': False, 'knockback_timer': 0}
        ]
    
    def handle_event(self, event):
        pass
    
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
        
        # Обновление вращения игрока
        if self.is_spinning:
            self.player_rotation += 15  # Скорость вращения
            self.spin_timer -= 1
            if self.spin_timer <= 0:
                self.is_spinning = False
                self.player_rotation = 0
        
        # Ограничение движения игрока
        self.player_x = max(125, min(self.screen_width - 125, self.player_x))
        self.player_y = max(175, min(self.screen_height - 175, self.player_y))
        
        # Обновление NPC
        for i, npc in enumerate(self.npcs):
            # Проверка столкновения с игроком (точный радиус действия)
            player_rect = pygame.Rect(self.player_x - 125, self.player_y - 175, 250, 350)
            npc_rect = pygame.Rect(npc['x'] - 150, npc['y'] - 210, 300, 420)  # Точный радиус для NPC
            
            if player_rect.colliderect(npc_rect) and not npc['knocked_back']:
                # NPC касается игрока - улетает в сторону
                npc['knocked_back'] = True
                npc['knockback_timer'] = 60  # 1 секунда при 60 FPS
                
                # Запуск вращения игрока
                if not self.is_spinning:
                    self.is_spinning = True
                    self.spin_timer = 90  # 1.5 секунды при 60 FPS
                
                # Диалоговое окно
                if not self.dialog_active:
                    self.dialog_active = True
                    self.dialog_timer = 120  # 2 секунды
                    if i == 0:
                        self.current_dialog = "Bakhredin: Скажите ДААААА"
                    elif i == 1:
                        self.current_dialog = "Tamirlan: Мейсон марджела туфли купить 44 размер"
                    else:
                        self.current_dialog = "Alikhan: Ну и? Люблю плавать, ты да СЕО?"
                
                # Направление отлета для каждого NPC
                if i == 0:  # Первый NPC - улетает влево
                    npc['knockback_dx'] = -15
                    
                    npc['knockback_dy'] = -5
                elif i == 1:  # Второй NPC - улетает вправо
                    npc['knockback_dx'] = 15
                    npc['knockback_dy'] = -5
                else:  # Третий NPC - улетает вверх
                    npc['knockback_dx'] = 0
                    npc['knockback_dy'] = -20
            
            if npc['knocked_back']:
                # NPC в состоянии отлета
                npc['x'] += npc['knockback_dx']
                npc['y'] += npc['knockback_dy']
                npc['knockback_timer'] -= 1
                
                # Замедление отлета
                npc['knockback_dx'] *= 0.95
                npc['knockback_dy'] *= 0.95
                
                if npc['knockback_timer'] <= 0:
                    npc['knocked_back'] = False
            else:
                # Обычное преследование игрока
                target_x = self.player_x
                target_y = self.player_y
                
                # Разные стратегии для каждого NPC
                if npc['strategy'] == 'right':
                    target_x = self.player_x + 100
                elif npc['strategy'] == 'left':
                    target_x = self.player_x - 100
                
                # Направление к цели
                dx = target_x - npc['x']
                dy = target_y - npc['y']
                
                # Нормализация вектора
                distance = math.sqrt(dx * dx + dy * dy)
                if distance > 0:
                    npc['x'] += (dx / distance) * npc['speed']
                    npc['y'] += (dy / distance) * npc['speed']
            
            # Ограничение движения NPC
            npc['x'] = max(150, min(self.screen_width - 150, npc['x']))  # Точные границы
            npc['y'] = max(210, min(self.screen_height - 210, npc['y']))  # Точные границы
        
        # Проверка пересечения с дверью
        player_rect = pygame.Rect(self.player_x - 125, self.player_y - 175, 250, 350)
        if player_rect.colliderect(self.door_rect):
            self.change_scene('LectureHallScene')
        
        # Возврат назад по ESC
        if keys[pygame.K_ESCAPE]:
            self.go_back()
        
        # Диалог таймер
        if self.dialog_active:
            self.dialog_timer -= 1
            if self.dialog_timer <= 0:
                self.dialog_active = False
                self.current_dialog = None
    
    def draw(self, screen):
        # Фон
        if self.lecture_343_image:
            screen.blit(self.lecture_343_image, (0, 0))
        else:
            screen.fill((60, 100, 140))
        
        # Дверь
        # pygame.draw.rect(screen, (255, 255, 255, 128), self.door_rect, 2)  # Для отладки
        
        # Игрок
        if self.ceo_image:
            if self.is_spinning:
                # Повернутое изображение игрока
                rotated_image = pygame.transform.rotate(self.ceo_image, self.player_rotation)
                # Получаем новый прямоугольник для центрирования
                rotated_rect = rotated_image.get_rect(center=(self.player_x, self.player_y))
                screen.blit(rotated_image, rotated_rect)
            else:
                screen.blit(self.ceo_image, (self.player_x - 125, self.player_y - 175))
        else:
            if self.is_spinning:
                # Повернутый прямоугольник для заглушки
                rotated_surface = pygame.Surface((250, 350))
                rotated_surface.fill((100, 150, 200))
                rotated_surface = pygame.transform.rotate(rotated_surface, self.player_rotation)
                rotated_rect = rotated_surface.get_rect(center=(self.player_x, self.player_y))
                screen.blit(rotated_surface, rotated_rect)
            else:
                pygame.draw.rect(screen, (100, 150, 200), 
                               (self.player_x - 125, self.player_y - 175, 250, 350))
        
        # NPC персонажи
        for i, npc in enumerate(self.npcs):
            if i < len(self.npc_images):
                screen.blit(self.npc_images[i], (npc['x'] - 150, npc['y'] - 210))  # Обновили позицию отрисовки
            else:
                pygame.draw.rect(screen, (150, 100, 200), 
                               (npc['x'] - 150, npc['y'] - 210, 300, 420))  # Обновили размеры отрисовки
        
        # Текст на двери
        door_text = self.small_font.render('Войти в зал', True, (255, 255, 255))
        screen.blit(door_text, (self.screen_width // 2 - 50, self.screen_height * 0.4 + 5))
        
        # Диалоговое окно поверх всего
        if self.dialog_active and self.current_dialog:
            dialog_width = 600
            dialog_height = 120
            dialog_x = (self.screen_width - dialog_width) // 2
            dialog_y = self.screen_height - dialog_height - 40
            pygame.draw.rect(screen, (30, 30, 30), (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=16)
            pygame.draw.rect(screen, (180, 160, 100), (dialog_x, dialog_y, dialog_width, dialog_height), 4, border_radius=16)
            # Текст диалога
            dialog_font = pygame.font.Font(None, 36)
            lines = self.current_dialog.split("\n")
            for idx, line in enumerate(lines):
                text_surf = dialog_font.render(line, True, (230, 220, 180))
                screen.blit(text_surf, (dialog_x + 30, dialog_y + 30 + idx * 40))
        
        # Подсказка о клавише ESC
        self.draw_esc_hint(screen) 