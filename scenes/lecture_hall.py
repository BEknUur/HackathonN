import pygame
import os
from .base_scene import BaseScene

class LectureHallScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x = self.screen_width * 0.25
        self.player_y = self.screen_height * 0.7
        self.player_speed = 5
        
        # Диалоговая система
        self.dialog_active = False
        self.dialog_timer = 0
        self.dialog_stage = 0  # 0 - нет диалога, 1 - слова Дианы, 2 - ввод ответа, 3 - отображение ответа
        self.dialog_duration = 3000  # 3 секунды на каждую реплику
        self.player_response = ""
        self.input_active = False
        self.show_response = False
        
        # Загрузка изображений
        self.ceo_image = None
        self.lecture_image = None
        self.diana_image = None
        self.alikhan_image = None
        self.load_images()
        
    def load_images(self):
        try:
            self.ceo_image = pygame.image.load(os.path.join('public', 'ceo.png'))
            self.ceo_image = pygame.transform.scale(self.ceo_image, (250, 350))
            
            self.lecture_image = pygame.image.load(os.path.join('public', 'lecture.jpg'))
            self.lecture_image = pygame.transform.scale(self.lecture_image, (self.screen_width, self.screen_height))
            
            self.diana_image = pygame.image.load(os.path.join('public', 'diana.png'))
            self.diana_image = pygame.transform.scale(self.diana_image, (350, 525))
            
            self.alikhan_image = pygame.image.load(os.path.join('public', 'alikhan.png'))
            self.alikhan_image = pygame.transform.scale(self.alikhan_image, (200, 300))
        except pygame.error as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки
            self.ceo_image = pygame.Surface((250, 350))
            self.ceo_image.fill((100, 150, 200))
            
            self.lecture_image = pygame.Surface((self.screen_width, self.screen_height))
            self.lecture_image.fill((70, 110, 150))
            
            self.diana_image = pygame.Surface((350, 525))
            self.diana_image.fill((200, 150, 180))
            
            self.alikhan_image = pygame.Surface((200, 300))
            self.alikhan_image.fill((100, 100, 150))
    
    def reset(self, data=None):
        self.player_x = self.screen_width * 0.25
        self.player_y = self.screen_height * 0.7
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.dialog_active:
            # Проверка клика по кнопке закрытия
            mouse_pos = pygame.mouse.get_pos()
            dialog_x = (self.screen_width - 600) // 2
            dialog_y = self.screen_height - 250
            close_button_rect = pygame.Rect(dialog_x + 570, dialog_y + 10, 20, 20)
            
            print(f"Mouse click at: {mouse_pos}")
            print(f"Close button rect: {close_button_rect}")
            print(f"Dialog active: {self.dialog_active}, Stage: {self.dialog_stage}")
            
            if close_button_rect.collidepoint(mouse_pos):
                print("Close button clicked! Closing dialog...")
                self.dialog_active = False
                self.dialog_stage = 0
                self.dialog_timer = 0
                self.input_active = False
                self.show_response = False
                self.player_response = ""
                return
        
        if event.type == pygame.KEYDOWN and self.dialog_active:
            # ESC закрывает диалог на любом этапе
            if event.key == pygame.K_ESCAPE:
                self.dialog_active = False
                self.dialog_stage = 0
                self.dialog_timer = 0
                self.input_active = False
                self.show_response = False
                self.player_response = ""
                return
                
            if self.dialog_stage == 2:
                if event.key == pygame.K_RETURN:
                    # Сохраняем ответ и переходим к отображению
                    if self.player_response.strip():  # Проверяем, что ответ не пустой
                        print(f"Ответ игрока: '{self.player_response}'")
                        self.show_response = True
                        self.dialog_stage = 3
                        self.dialog_timer = 0
                        self.input_active = False
                        print("Переход к отображению ответа игрока")
                    else:
                        print("Ответ пустой, не переходим к отображению")
                elif event.key == pygame.K_BACKSPACE:
                    self.player_response = self.player_response[:-1]
                else:
                    # Добавляем символ к ответу
                    if event.unicode.isprintable() and len(self.player_response) < 50:
                        self.player_response += event.unicode
    
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
        
        # Проверка близости к Диане
        diana_x = self.screen_width * 0.4 + 175  # Центр Дианы (x + половина ширины)
        diana_y = self.screen_height * 0.35 + 262  # Центр Дианы (y + половина высоты)
        distance_diana = ((self.player_x - diana_x) ** 2 + (self.player_y - diana_y) ** 2) ** 0.5
        
        # Увеличенный радиус взаимодействия
        if distance_diana < 300 and not self.dialog_active and self.dialog_stage == 0:
            self.dialog_active = True
            self.dialog_timer = 0
            self.dialog_stage = 1
            print(f"Диалог активирован! Расстояние: {distance_diana}")
        
        # Проверка близости к Алихану
        alikhan_x = self.screen_width - 220 + 100  # Центр Алихана (x + половина ширины)
        alikhan_y = 20 + 150  # Центр Алихана (y + половина высоты)
        distance_alikhan = ((self.player_x - alikhan_x) ** 2 + (self.player_y - alikhan_y) ** 2) ** 0.5
        
        # Переход к Алихану
        if distance_alikhan < 150:
            print(f"Переход к Алихану! Расстояние: {distance_alikhan}")
            self.change_scene('DaylickScene')
        
        # Обновление диалога
        if self.dialog_active:
            self.dialog_timer += dt
            if self.dialog_timer >= self.dialog_duration:
                if self.dialog_stage == 1:
                    self.dialog_stage = 2
                    self.dialog_timer = 0
                    self.input_active = True
                    print("Переход к вводу ответа")
                elif self.dialog_stage == 3:
                    self.dialog_active = False
                    self.dialog_stage = 0
                    self.dialog_timer = 0
                    self.input_active = False
                    self.show_response = False
                    self.player_response = ""
                    print("Диалог завершен")
        
        # Возврат назад по ESC
        if keys[pygame.K_ESCAPE]:
            self.go_back()
    
    def draw(self, screen):
        # Фон
        if self.lecture_image:
            screen.blit(self.lecture_image, (0, 0))
        else:
            screen.fill((70, 110, 150))
        
        # Игрок
        if self.ceo_image:
            screen.blit(self.ceo_image, (self.player_x - 125, self.player_y - 175))
        else:
            pygame.draw.rect(screen, (100, 150, 200), 
                           (self.player_x - 125, self.player_y - 175, 250, 350))
        
        # Diana персонаж (среди стульев)
        diana_x = self.screen_width * 0.4
        diana_y = self.screen_height * 0.35
        if self.diana_image:
            screen.blit(self.diana_image, (diana_x, diana_y))
        else:
            pygame.draw.rect(screen, (200, 150, 180), 
                           (diana_x, diana_y, 350, 525))
        
        # Alikhan персонаж (правый верхний угол)
        alikhan_x = self.screen_width - 220  # 200px width + 20px margin
        alikhan_y = 20  # 20px from top
        if self.alikhan_image:
            screen.blit(self.alikhan_image, (alikhan_x, alikhan_y))
        else:
            pygame.draw.rect(screen, (100, 100, 150), 
                           (alikhan_x, alikhan_y, 200, 300))
        

        

        
        # Диалоговое окно
        if self.dialog_active:
            # Отладочная информация
            debug_text = self.small_font.render(f"Stage: {self.dialog_stage}, Response: '{self.player_response}'", True, (255, 255, 0))
            screen.blit(debug_text, (10, 30))
            # Фон диалогового окна (темный фэнтези стиль)
            dialog_width = 600
            dialog_height = 200
            dialog_x = (self.screen_width - dialog_width) // 2
            dialog_y = self.screen_height - dialog_height - 50
            
            # Темный фон с градиентом
            dialog_surface = pygame.Surface((dialog_width, dialog_height))
            dialog_surface.fill((20, 20, 30))
            
            # Рамка
            pygame.draw.rect(dialog_surface, (100, 80, 120), (0, 0, dialog_width, dialog_height), 3)
            pygame.draw.rect(dialog_surface, (60, 40, 80), (3, 3, dialog_width-6, dialog_height-6), 2)
            
            screen.blit(dialog_surface, (dialog_x, dialog_y))
            
            # Кнопка закрытия (X)
            close_button_rect = pygame.Rect(dialog_x + dialog_width - 30, dialog_y + 10, 20, 20)
            pygame.draw.rect(screen, (150, 50, 50), close_button_rect)
            pygame.draw.rect(screen, (255, 255, 0), close_button_rect, 2)  # Желтая рамка для видимости
            close_text = self.small_font.render("X", True, (255, 255, 255))
            screen.blit(close_text, (dialog_x + dialog_width - 25, dialog_y + 12))
            

            
            # Текст диалога
            if self.dialog_stage == 1:
                # Слова Дианы
                name_text = self.small_font.render("Диана:", True, (255, 200, 100))
                dialog_text = self.small_font.render("Почему опаздываем?", True, (220, 220, 220))
                screen.blit(name_text, (dialog_x + 20, dialog_y + 20))
                screen.blit(dialog_text, (dialog_x + 20, dialog_y + 50))
                
            elif self.dialog_stage == 2:
                # Поле ввода ответа
                name_text = self.small_font.render("Вы:", True, (100, 200, 255))
                screen.blit(name_text, (dialog_x + 20, dialog_y + 20))
                
                # Поле ввода
                input_rect = pygame.Rect(dialog_x + 20, dialog_y + 50, dialog_width - 40, 30)
                pygame.draw.rect(screen, (40, 40, 50), input_rect)
                pygame.draw.rect(screen, (100, 100, 120), input_rect, 2)
                
                # Текст в поле ввода с курсором
                cursor = "|" if self.input_active else ""
                input_text = self.small_font.render(self.player_response + cursor, True, (220, 220, 220))
                screen.blit(input_text, (dialog_x + 25, dialog_y + 55))
                
                # Инструкция
                instruction_text = self.small_font.render("Напишите ответ и нажмите Enter (ESC для отмены)", True, (150, 150, 150))
                screen.blit(instruction_text, (dialog_x + 20, dialog_y + 90))
                
            elif self.dialog_stage == 3:
                # Отображение ответа игрока
                name_text = self.small_font.render("Вы:", True, (100, 200, 255))
                response_text = self.small_font.render(self.player_response, True, (220, 220, 220))
                screen.blit(name_text, (dialog_x + 20, dialog_y + 20))
                screen.blit(response_text, (dialog_x + 20, dialog_y + 50))
                
                # Инструкция для закрытия
                close_instruction = self.small_font.render("Нажмите ESC или X для закрытия", True, (150, 150, 150))
                screen.blit(close_instruction, (dialog_x + 20, dialog_y + 90))
        
        # Текст подсказки
        hint_text = self.small_font.render('ESC - Вернуться назад', True, (255, 255, 255))
        screen.blit(hint_text, (10, 10))
        
        # Подсказка о клавише ESC
        self.draw_esc_hint(screen) 