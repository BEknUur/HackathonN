import pygame
import os
from .base_scene import BaseScene

class UniversityEntranceScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x = self.screen_width * 0.25
        self.player_y = self.screen_height * 0.7
        self.player_speed = 5
        self.door_rect = pygame.Rect(self.screen_width // 2 - 60, self.screen_height * 0.7 - 90, 120, 180)
        
        # Загрузка изображений
        self.ceo_image = None
        self.satbayev_image = None
        self.load_images()
        
    def load_images(self):
        try:
            self.ceo_image = pygame.image.load(os.path.join('public', 'ceo.png'))
            self.ceo_image = pygame.transform.scale(self.ceo_image, (250, 350))
            
            self.satbayev_image = pygame.image.load(os.path.join('public', 'satbayev.jpg'))
            self.satbayev_image = pygame.transform.scale(self.satbayev_image, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки
            self.ceo_image = pygame.Surface((250, 350))
            self.ceo_image.fill((100, 150, 200))
            
            self.satbayev_image = pygame.Surface((self.screen_width, self.screen_height))
            self.satbayev_image.fill((50, 100, 150))
    
    def reset(self, data=None):
        self.player_x = self.screen_width * 0.25
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
        
        # Проверка пересечения с дверью
        player_rect = pygame.Rect(self.player_x - 125, self.player_y - 175, 250, 350)
        if player_rect.colliderect(self.door_rect):
            self.change_scene('CorridorScene')
    
    def draw(self, screen):
        # Фон
        if self.satbayev_image:
            screen.blit(self.satbayev_image, (0, 0))
        else:
            screen.fill((50, 100, 150))
        
        # Игрок
        if self.ceo_image:
            screen.blit(self.ceo_image, (self.player_x - 125, self.player_y - 175))
        else:
            pygame.draw.rect(screen, (100, 150, 200), 
                           (self.player_x - 125, self.player_y - 175, 250, 350))
        
        # Дверь (невидимая зона)
        # pygame.draw.rect(screen, (255, 255, 255, 128), self.door_rect, 2)  # Для отладки
        
        # Текст подсказки
        hint_text = self.small_font.render('Двигайтесь к двери для входа', True, (255, 255, 255))
        screen.blit(hint_text, (10, 10))
        
        # Текст на двери
        door_text = self.small_font.render('Вход в университет', True, (255, 255, 255))
        screen.blit(door_text, (self.screen_width // 2 - 60, self.screen_height * 0.7 + 10))
        
        # Подсказка о клавише ESC
        self.draw_esc_hint(screen) 