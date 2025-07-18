import pygame

class BaseScene:
    def __init__(self, game):
        self.game = game
        self.screen_width = game.screen_width
        self.screen_height = game.screen_height
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def reset(self, data=None):
        """Сброс сцены при переходе к ней"""
        pass
        
    def handle_event(self, event):
        """Обработка событий pygame"""
        pass
        
    def update(self, dt):
        """Обновление логики сцены"""
        pass
        
    def draw(self, screen):
        """Отрисовка сцены"""
        pass
        
    def draw_esc_hint(self, screen):
        """Отрисовка подсказки о клавише ESC"""
        esc_text = self.small_font.render('ESC - Вернуться в меню', True, (255, 255, 255))
        # Добавляем полупрозрачный фон для лучшей читаемости
        text_rect = esc_text.get_rect()
        text_rect.bottomright = (self.screen_width - 10, self.screen_height - 10)
        
        # Фон для текста
        bg_rect = pygame.Rect(text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 128))  # Полупрозрачный черный
        screen.blit(bg_surface, bg_rect)
        
        # Текст
        screen.blit(esc_text, text_rect)
        
    def change_scene(self, scene_name, data=None):
        """Переход к другой сцене"""
        self.game.change_scene(scene_name, data)
    
    def go_back(self):
        """Возврат к предыдущей сцене"""
        self.game.go_back() 