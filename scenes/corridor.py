import pygame
import os
from .base_scene import BaseScene

class CorridorScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x = self.screen_width * 0.1
        self.player_y = self.screen_height // 2
        self.player_speed = 5
        self.door_rect = pygame.Rect(self.screen_width * 0.75 - 40, self.screen_height // 2 - 60, 80, 120)
        self.dialog_active = False
        self.current_dialog = None
        self.dialog_timer = 0
        
        # Загрузка изображений
        self.ceo_image = None
        self.hall_image = None
        self.tuka_image = None
        self.kenzhe_image = None
        self.aliba_image = None
        self.load_images()
        
    def load_images(self):
        try:
            self.ceo_image = pygame.image.load(os.path.join('public', 'ceo.png'))
            self.ceo_image = pygame.transform.scale(self.ceo_image, (250, 350))
            
            self.hall_image = pygame.image.load(os.path.join('public', 'hall1.jpeg'))
            self.hall_image = pygame.transform.scale(self.hall_image, (self.screen_width, self.screen_height))
            
            self.tuka_image = pygame.image.load(os.path.join('public', 'tuka.png'))
            self.tuka_image = pygame.transform.scale(self.tuka_image, (200, 300))
            
            self.kenzhe_image = pygame.image.load(os.path.join('public', 'kenzhe.png'))
            self.kenzhe_image = pygame.transform.scale(self.kenzhe_image, (200, 300))
            
            self.aliba_image = pygame.image.load(os.path.join('public', 'aliba.webp'))
            self.aliba_image = pygame.transform.scale(self.aliba_image, (200, 300))
        except pygame.error as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки
            self.ceo_image = pygame.Surface((250, 350))
            self.ceo_image.fill((100, 150, 200))
            
            self.hall_image = pygame.Surface((self.screen_width, self.screen_height))
            self.hall_image.fill((80, 120, 160))
            
            self.tuka_image = pygame.Surface((200, 300))
            self.tuka_image.fill((120, 180, 220))
            
            self.kenzhe_image = pygame.Surface((200, 300))
            self.kenzhe_image.fill((140, 160, 200))
            
            self.aliba_image = pygame.Surface((200, 300))
            self.aliba_image.fill((160, 140, 180))
    
    def reset(self, data=None):
        self.player_x = self.screen_width * 0.1
        self.player_y = self.screen_height // 2
        self.dialog_active = False
        self.current_dialog = None
        self.dialog_timer = 0
    
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
            self.change_scene('LectureRoom')
        
        # Возврат назад по ESC
        if keys[pygame.K_ESCAPE]:
            self.go_back()
        
        # Проверка пересечения с персонажами (более точные области)
        player_rect = pygame.Rect(self.player_x - 125, self.player_y - 175, 250, 350)
        
        # Более точные области для каждого персонажа
        kenzhe_rect = pygame.Rect(self.screen_width * 0.3 - 75, self.screen_height * 0.3 - 75, 250, 350)
        tuka_rect = pygame.Rect(self.screen_width * 0.5 - 75, self.screen_height * 0.3 - 75, 250, 350)
        aliba_rect = pygame.Rect(self.screen_width * 0.8 - 75, self.screen_height * 0.3 - 75, 250, 350)
        
        if not self.dialog_active:
            # Проверяем в порядке приоритета (ближайший к игроку)
            if player_rect.colliderect(tuka_rect):
                self.dialog_active = True
                self.current_dialog = "Tuka: Ішпедік па родной"
                self.dialog_timer = 120
            elif player_rect.colliderect(kenzhe_rect):
                self.dialog_active = True
                self.current_dialog = "Kenzhe: Ассалаумағалейкум СЕО ағай"
                self.dialog_timer = 120
            elif player_rect.colliderect(aliba_rect):
                self.dialog_active = True
                self.current_dialog = "Aliba: "
                self.dialog_timer = 120
        if self.dialog_active:
            self.dialog_timer -= 1
            if self.dialog_timer <= 0:
                self.dialog_active = False
                self.current_dialog = None
    
    def draw(self, screen):
        # Фон
        if self.hall_image:
            screen.blit(self.hall_image, (0, 0))
        else:
            screen.fill((80, 120, 160))
        
        # Дверь в лекционный зал
        pygame.draw.rect(screen, (222, 184, 135), self.door_rect)
        
        # Игрок
        if self.ceo_image:
            screen.blit(self.ceo_image, (self.player_x - 125, self.player_y - 175))
        else:
            pygame.draw.rect(screen, (100, 150, 200), 
                           (self.player_x - 125, self.player_y - 175, 250, 350))
        
        # Kenzhe персонаж (слева)
        if self.kenzhe_image:
            screen.blit(self.kenzhe_image, (self.screen_width * 0.3, self.screen_height * 0.3))
        else:
            pygame.draw.rect(screen, (140, 160, 200), 
                           (self.screen_width * 0.3, self.screen_height * 0.3, 200, 300))
        
        # Tuka персонаж (в центре)
        if self.tuka_image:
            screen.blit(self.tuka_image, (self.screen_width * 0.5, self.screen_height * 0.3))
        else:
            pygame.draw.rect(screen, (120, 180, 220), 
                           (self.screen_width * 0.5, self.screen_height * 0.3, 200, 300))
        
        # Aliba персонаж (справа, на край)
        if self.aliba_image:
            screen.blit(self.aliba_image, (self.screen_width * 0.8, self.screen_height * 0.3))
        else:
            pygame.draw.rect(screen, (160, 140, 180), 
                           (self.screen_width * 0.8, self.screen_height * 0.3, 200, 300))
        
        # Диалоговое окно поверх всего
        if self.dialog_active and self.current_dialog:
            dialog_width = 600
            dialog_height = 120
            dialog_x = (self.screen_width - dialog_width) // 2
            dialog_y = self.screen_height - dialog_height - 40
            pygame.draw.rect(screen, (30, 30, 30), (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=16)
            pygame.draw.rect(screen, (180, 160, 100), (dialog_x, dialog_y, dialog_width, dialog_height), 4, border_radius=16)
            dialog_font = pygame.font.Font(None, 36)
            lines = self.current_dialog.split("\n")
            for idx, line in enumerate(lines):
                text_surf = dialog_font.render(line, True, (230, 220, 180))
                screen.blit(text_surf, (dialog_x + 30, dialog_y + 30 + idx * 40))
        
        # Текст на двери
        door_text = self.small_font.render('Лекционный зал', True, (255, 255, 255))
        screen.blit(door_text, (self.screen_width * 0.75 - 50, self.screen_height // 2 + 30))
        
        # Подсказка о клавише ESC
        self.draw_esc_hint(screen) 