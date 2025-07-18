import pygame
import os
from .base_scene import BaseScene

class Location1Scene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x = 100
        self.player_y = 100
        self.player_speed = 2
        self.quiz_trigger_rect = pygame.Rect(175, 175, 50, 50)
        
        # Загрузка изображений
        self.player_image = None
        self.bg_image = None
        self.load_images()
        
    def load_images(self):
        try:
            # Попытка загрузить изображения (если они есть)
            self.player_image = pygame.Surface((32, 32))
            self.player_image.fill((100, 150, 200))
            
            self.bg_image = pygame.Surface((800, 600))
            self.bg_image.fill((90, 130, 170))
        except pygame.error as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки
            self.player_image = pygame.Surface((32, 32))
            self.player_image.fill((100, 150, 200))
            
            self.bg_image = pygame.Surface((800, 600))
            self.bg_image.fill((90, 130, 170))
    
    def reset(self, data=None):
        self.player_x = 100
        self.player_y = 100
    
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed
        if keys[pygame.K_UP]:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player_y += self.player_speed
        
        # Ограничение движения игрока
        self.player_x = max(16, min(self.screen_width - 16, self.player_x))
        self.player_y = max(16, min(self.screen_height - 16, self.player_y))
        
        # Проверка пересечения с триггером квиза
        player_rect = pygame.Rect(self.player_x - 16, self.player_y - 16, 32, 32)
        if player_rect.colliderect(self.quiz_trigger_rect):
            self.change_scene('QuizScene', {'locationId': 'loc1'})
    
    def draw(self, screen):
        # Фон
        if self.bg_image:
            # Масштабируем фон под размер экрана
            scaled_bg = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
            screen.blit(scaled_bg, (0, 0))
        else:
            screen.fill((90, 130, 170))
        
        # Игрок
        if self.player_image:
            screen.blit(self.player_image, (self.player_x - 16, self.player_y - 16))
        else:
            pygame.draw.rect(screen, (100, 150, 200), 
                           (self.player_x - 16, self.player_y - 16, 32, 32))
        
        # Триггер для квиза (невидимый)
        # pygame.draw.rect(screen, (255, 255, 0), self.quiz_trigger_rect, 2)  # Для отладки
        
        # Подсказка о клавише ESC
        self.draw_esc_hint(screen) 