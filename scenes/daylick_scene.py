import pygame
import os
from .base_scene import BaseScene

class DaylickScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x = self.screen_width * 0.5
        self.player_y = self.screen_height * 0.7
        self.player_speed = 5
        
        # Загрузка изображений
        self.ceo_image = None
        self.daylick_image = None
        self.load_images()
        
    def load_images(self):
        try:
            self.ceo_image = pygame.image.load(os.path.join('public', 'ceo.png'))
            self.ceo_image = pygame.transform.scale(self.ceo_image, (250, 350))
            
            self.daylick_image = pygame.image.load(os.path.join('public', 'daylick.jpeg'))
            self.daylick_image = pygame.transform.scale(self.daylick_image, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки
            self.ceo_image = pygame.Surface((250, 350))
            self.ceo_image.fill((100, 150, 200))
            
            self.daylick_image = pygame.Surface((self.screen_width, self.screen_height))
            self.daylick_image.fill((70, 110, 150))
    
    def reset(self, data=None):
        self.player_x = self.screen_width * 0.5
        self.player_y = self.screen_height * 0.7
    
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
        
        # Ограничение движения игрока
        self.player_x = max(125, min(self.screen_width - 125, self.player_x))
        self.player_y = max(175, min(self.screen_height - 175, self.player_y))
        
        # Возврат назад по ESC
        if keys[pygame.K_ESCAPE]:
            self.go_back()
    
    def draw(self, screen):
        # Фон
        if self.daylick_image:
            screen.blit(self.daylick_image, (0, 0))
        else:
            screen.fill((70, 110, 150))
        
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