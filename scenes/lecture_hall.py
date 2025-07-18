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
        
        # Система сообщений над головой Дианы
        self.diana_message_active = False
        self.diana_message_timer = 0
        self.diana_message_duration = 5000  # 5 секунд на сообщение
        self.diana_message = ""
        self.diana_message_input_active = False
        self.diana_message_input = ""
        
        # Система сообщений игрока (CEO)
        self.player_message_active = False
        self.player_message_timer = 0
        self.player_message_duration = 5000  # 5 секунд на сообщение
        self.player_message = ""
        self.player_message_input_active = False
        self.player_message_input = ""
        
        # Система квиза для Армана
        self.quiz_active = False
        self.quiz_stage = 0  # 0 - нет квиза, 1 - приветствие, 2 - вопросы, 3 - показ ответа, 4 - результаты
        self.current_question = 0
        self.selected_answer = 0
        self.correct_answers = 0
        self.total_questions = 0
        self.answer_shown = False  # Флаг для показа ответа
        self.answer_timer = 0  # Таймер для показа ответа
        self.answer_duration = 2000  # 2 секунды на показ ответа
        
        # Вопросы для квиза
        self.quiz_questions = [
            {
                "question": "С какого начался нфакториал инкубатор?",
                "answers": ["2014", "2015", "2016", "2017"],
                "correct": 2
            },
            {
                "question": "СКОЛЬКО ЮЗЕРОВ У НУРМУХАММЕДА",
                "answers": ["600", "800", "400", "1000"],
                "correct": 4
            },
            {
                "question": "Кто больше спит",
                "answers": ["НУРГИСА", "АЛИБЕК", "БЕКНУР", "АСХАТ"],
                "correct": 1
            },
            {
                "question": "Кто главный СЕО",
                "answers": ["Бекжан", "Арман Сулейменов", "Тұрарбек ", "Мади ейеай Батыр ейай"],
                "correct": 1
            }
        ]
        
        # Загрузка изображений
        self.ceo_image = None
        self.lecture_image = None
        self.diana_image = None
        self.alikhan_image = None
        self.armansu_image = None
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
            
            self.armansu_image = pygame.image.load(os.path.join('public', 'armansu.png'))
            self.armansu_image = pygame.transform.scale(self.armansu_image, (250, 375))  # Увеличил размер
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
            
            self.armansu_image = pygame.Surface((250, 375))
            self.armansu_image.fill((100, 100, 100))
    
    def reset(self, data=None):
        self.player_x = self.screen_width * 0.25
        self.player_y = self.screen_height * 0.7
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка клика по кнопке квиза
            # if self.quiz_button_rect and self.quiz_button_rect.collidepoint(event.pos):
            #     if not self.quiz_active and not self.dialog_active:
            #         print("Кнопка квиза нажата! Запуск квиза...")
            #         self.quiz_active = True
            #         self.quiz_stage = 1
            #         self.current_question = 0
            #         self.selected_answer = 0
            #         self.correct_answers = 0
            #         return
            
            # Проверка клика по кнопке закрытия
            if self.dialog_active:
                mouse_pos = pygame.mouse.get_pos()
                dialog_x = (self.screen_width - 600) // 2
                dialog_y = self.screen_height - 250
                close_button_rect = pygame.Rect(dialog_x + 565, dialog_y + 10, 25, 25)  # Та же позиция, что и в draw
                
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
                
                # Альтернативный способ: клик в любом месте диалогового окна закрывает его
                dialog_rect = pygame.Rect(dialog_x, dialog_y, 600, 200)
                if dialog_rect.collidepoint(mouse_pos):
                    print("Dialog area clicked! Closing dialog...")
                    self.dialog_active = False
                    self.dialog_stage = 0
                    self.dialog_timer = 0
                    self.input_active = False
                    self.show_response = False
                    self.player_response = ""
                    return
        
        if event.type == pygame.KEYDOWN:
            # Обработка сообщений игрока (CEO)
            if self.player_message_input_active:
                if event.key == pygame.K_RETURN:
                    # Сохраняем сообщение и показываем его над головой игрока
                    if self.player_message_input.strip():
                        self.player_message = self.player_message_input
                        self.player_message_active = True
                        self.player_message_timer = 0
                        self.player_message_input_active = False
                        self.player_message_input = ""
                        print(f"Сообщение игрока: '{self.player_message}'")
                    return
                elif event.key == pygame.K_ESCAPE:
                    # Отмена ввода
                    self.player_message_input_active = False
                    self.player_message_input = ""
                    return
                elif event.key == pygame.K_BACKSPACE:
                    self.player_message_input = self.player_message_input[:-1]
                else:
                    # Добавляем символ к сообщению
                    if event.unicode.isprintable() and len(self.player_message_input) < 30:
                        self.player_message_input += event.unicode
                return
            
            # Обработка сообщений Дианы
            if self.diana_message_input_active:
                if event.key == pygame.K_RETURN:
                    # Сохраняем сообщение и показываем его над головой Дианы
                    if self.diana_message_input.strip():
                        self.diana_message = self.diana_message_input
                        self.diana_message_active = True
                        self.diana_message_timer = 0
                        self.diana_message_input_active = False
                        self.diana_message_input = ""
                        print(f"Сообщение Диане: '{self.diana_message}'")
                    return
                elif event.key == pygame.K_ESCAPE:
                    # Отмена ввода
                    self.diana_message_input_active = False
                    self.diana_message_input = ""
                    return
                elif event.key == pygame.K_BACKSPACE:
                    self.diana_message_input = self.diana_message_input[:-1]
                else:
                    # Добавляем символ к сообщению
                    if event.unicode.isprintable() and len(self.diana_message_input) < 30:
                        self.diana_message_input += event.unicode
                return
            
            if self.dialog_active:
                print(f"Key event received: {event.key}, dialog_active: {self.dialog_active}")
                # ESC или X (любой регистр) закрывает диалог на любом этапе
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_x:
                    print(f"Key pressed: {event.key}, closing dialog...")
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
            
            # Активация ввода сообщения игрока по клавише Y
            if event.key == pygame.K_y and not self.quiz_active and not self.diana_message_input_active and not self.player_message_input_active:
                print("Активация ввода сообщения игрока")
                self.player_message_input_active = True
                self.player_message_input = ""
                return
            
            # Активация ввода сообщения Диане по клавише T
            if event.key == pygame.K_t and not self.quiz_active and not self.diana_message_input_active and not self.player_message_input_active:
                print("Активация ввода сообщения Диане")
                self.diana_message_input_active = True
                self.diana_message_input = ""
                return
        
        # Обработка событий квиза
        if event.type == pygame.KEYDOWN and self.quiz_active:
            if event.key == pygame.K_ESCAPE:
                # Закрытие квиза
                self.quiz_active = False
                self.quiz_stage = 0
                self.current_question = 0
                self.selected_answer = 0
                self.correct_answers = 0
                self.answer_shown = False
                self.answer_timer = 0
                return
            
            if self.quiz_stage == 1:  # Приветствие
                if event.key == pygame.K_RETURN:
                    self.quiz_stage = 2
                    self.current_question = 0
                    self.selected_answer = 0
                    self.correct_answers = 0
                    self.total_questions = len(self.quiz_questions)
                    return
            
            elif self.quiz_stage == 2:  # Вопросы
                if event.key == pygame.K_UP:
                    self.selected_answer = (self.selected_answer - 1) % 4
                elif event.key == pygame.K_DOWN:
                    self.selected_answer = (self.selected_answer + 1) % 4
                elif event.key == pygame.K_RETURN:
                    # Проверяем ответ и переходим к показу результата
                    if self.selected_answer == self.quiz_questions[self.current_question]["correct"]:
                        self.correct_answers += 1
                    
                    self.quiz_stage = 3  # Переходим к показу ответа
                    self.answer_shown = True
                    self.answer_timer = 0
                    return
            
            elif self.quiz_stage == 3:  # Показ ответа
                if event.key == pygame.K_RETURN:
                    # Переходим к следующему вопросу или результатам
                    self.current_question += 1
                    if self.current_question >= len(self.quiz_questions):
                        self.quiz_stage = 4  # Переходим к результатам
                    else:
                        self.quiz_stage = 2  # Возвращаемся к вопросам
                        self.selected_answer = 0  # Сбрасываем выбор для следующего вопроса
                    self.answer_shown = False
                    self.answer_timer = 0
                    return
            
            elif self.quiz_stage == 4:  # Результаты
                if event.key == pygame.K_RETURN:
                    # Закрытие квиза
                    self.quiz_active = False
                    self.quiz_stage = 0
                    self.current_question = 0
                    self.selected_answer = 0
                    self.correct_answers = 0
                    self.answer_shown = False
                    self.answer_timer = 0
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
            return  # Прерываем выполнение после перехода
        
        # Проверка близости к Арману
        arman_x = 20 + 125  # Центр Армана (x + половина ширины)
        arman_y = 20 + 187  # Центр Армана (y + половина высоты)
        distance_arman = ((self.player_x - arman_x) ** 2 + (self.player_y - arman_y) ** 2) ** 0.5
        
        # Активация квиза от Армана (убираем автоматическую активацию, теперь только через кнопку)
        if distance_arman < 200 and not self.quiz_active and not self.dialog_active:
            print(f"Квиз от Армана активирован! Расстояние: {distance_arman}")
            self.quiz_active = True
            self.quiz_stage = 1
            self.current_question = 0
            self.selected_answer = 0
            self.correct_answers = 0
        
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
        
        # Обновление таймера сообщений Дианы
        if self.diana_message_active:
            self.diana_message_timer += dt
            if self.diana_message_timer >= self.diana_message_duration:
                # Автоматическое скрытие сообщения через 5 секунд
                self.diana_message_active = False
                self.diana_message_timer = 0
                self.diana_message = ""
        
        # Обновление таймера сообщений игрока (CEO)
        if self.player_message_active:
            self.player_message_timer += dt
            if self.player_message_timer >= self.player_message_duration:
                # Автоматическое скрытие сообщения через 5 секунд
                self.player_message_active = False
                self.player_message_timer = 0
                self.player_message = ""
        
        # Обновление таймера показа ответа квиза
        if self.quiz_active and self.quiz_stage == 3:
            self.answer_timer += dt
            if self.answer_timer >= self.answer_duration:
                # Автоматически переходим к следующему вопросу через 2 секунды
                self.current_question += 1
                if self.current_question >= len(self.quiz_questions):
                    self.quiz_stage = 4  # Переходим к результатам
                else:
                    self.quiz_stage = 2  # Возвращаемся к вопросам
                    self.selected_answer = 0  # Сбрасываем выбор для следующего вопроса
                self.answer_shown = False
                self.answer_timer = 0
        
        # Возврат назад по ESC
        if keys[pygame.K_ESCAPE]:
            self.go_back()
        
        # Резервное закрытие диалога по X (если handle_event не сработал)
        if keys[pygame.K_x]:
            if self.dialog_active and not hasattr(self, '_x_pressed'):
                print("X key pressed in update (reserve), closing dialog...")
                self.dialog_active = False
                self.dialog_stage = 0
                self.dialog_timer = 0
                self.input_active = False
                self.show_response = False
                self.player_response = ""
                self._x_pressed = True
        else:
            # Сбрасываем флаг когда клавиша отпущена
            if hasattr(self, '_x_pressed'):
                delattr(self, '_x_pressed')
    
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
        
        # Сообщение над головой игрока (CEO)
        if self.player_message_active and self.player_message:
            # Позиция сообщения над головой игрока
            message_x = self.player_x  # Центр игрока
            message_y = self.player_y - 200  # Выше головы игрока
            
            # Фон сообщения
            message_text = self.small_font.render(self.player_message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=(message_x, message_y))
            
            # Расширяем фон для лучшей читаемости
            bg_rect = pygame.Rect(message_rect.x - 10, message_rect.y - 5, 
                                 message_rect.width + 20, message_rect.height + 10)
            
            # Полупрозрачный фон
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            screen.blit(bg_surface, bg_rect)
            
            # Рамка (синий цвет для игрока)
            pygame.draw.rect(screen, (100, 200, 255), bg_rect, 2)
            
            # Текст сообщения
            screen.blit(message_text, message_rect)
            
            # Таймер (показывает оставшееся время)
            remaining_time = max(0, (self.player_message_duration - self.player_message_timer) / 1000)
            timer_text = self.small_font.render(f"{remaining_time:.1f}с", True, (150, 150, 150))
            timer_rect = timer_text.get_rect(center=(message_x, message_y + 20))
            screen.blit(timer_text, timer_rect)
        
        # Diana персонаж (среди стульев)
        diana_x = self.screen_width * 0.4
        diana_y = self.screen_height * 0.35
        if self.diana_image:
            screen.blit(self.diana_image, (diana_x, diana_y))
        else:
            pygame.draw.rect(screen, (200, 150, 180), 
                           (diana_x, diana_y, 350, 525))
        
        # Сообщение над головой Дианы
        if self.diana_message_active and self.diana_message:
            # Позиция сообщения над головой Дианы
            message_x = diana_x + 175  # Центр Дианы (x + половина ширины)
            message_y = diana_y - 50   # Выше головы Дианы
            
            # Фон сообщения
            message_text = self.small_font.render(self.diana_message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=(message_x, message_y))
            
            # Расширяем фон для лучшей читаемости
            bg_rect = pygame.Rect(message_rect.x - 10, message_rect.y - 5, 
                                 message_rect.width + 20, message_rect.height + 10)
            
            # Полупрозрачный фон
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            screen.blit(bg_surface, bg_rect)
            
            # Рамка
            pygame.draw.rect(screen, (255, 200, 100), bg_rect, 2)
            
            # Текст сообщения
            screen.blit(message_text, message_rect)
            
            # Таймер (показывает оставшееся время)
            remaining_time = max(0, (self.diana_message_duration - self.diana_message_timer) / 1000)
            timer_text = self.small_font.render(f"{remaining_time:.1f}с", True, (150, 150, 150))
            timer_rect = timer_text.get_rect(center=(message_x, message_y + 20))
            screen.blit(timer_text, timer_rect)
        
        # Alikhan персонаж (правый верхний угол)
        alikhan_x = self.screen_width - 220  # 200px width + 20px margin
        alikhan_y = 20  # 20px from top
        if self.alikhan_image:
            screen.blit(self.alikhan_image, (alikhan_x, alikhan_y))
        else:
            pygame.draw.rect(screen, (100, 100, 150), 
                           (alikhan_x, alikhan_y, 200, 300))
        
        # Arman персонаж (левый верхний угол)
        arman_x = 20  # 20px from left
        arman_y = 20  # 20px from top
        if self.armansu_image:
            screen.blit(self.armansu_image, (arman_x, arman_y))
        else:
            pygame.draw.rect(screen, (100, 100, 100), 
                           (arman_x, arman_y, 250, 375))
        
        # Кнопка для квиза Армана
        # if self.quiz_button_rect and not self.quiz_active:
        #     if self.quiz_button_hover:
        #         pygame.draw.rect(screen, (200, 80, 80), self.quiz_button_rect)
        #         pygame.draw.rect(screen, (255, 255, 255), self.quiz_button_rect, 3)  # Белая рамка при наведении
        #     else:
        #         pygame.draw.rect(screen, (150, 50, 50), self.quiz_button_rect)
        #         pygame.draw.rect(screen, (255, 255, 0), self.quiz_button_rect, 2)  # Желтая рамка
            
            # Текст кнопки
        #     quiz_text = self.small_font.render("Квиз", True, (255, 255, 255))
        #     quiz_text_rect = quiz_text.get_rect(center=self.quiz_button_rect.center)
        #     screen.blit(quiz_text, quiz_text_rect)
        

        

        
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
            
            # Кнопка закрытия (X) - улучшенная версия
            close_button_rect = pygame.Rect(dialog_x + dialog_width - 35, dialog_y + 10, 25, 25)
            
            # Проверяем, находится ли мышь над кнопкой для эффекта наведения
            mouse_pos = pygame.mouse.get_pos()
            if close_button_rect.collidepoint(mouse_pos):
                # Эффект наведения - более яркий цвет
                pygame.draw.rect(screen, (200, 80, 80), close_button_rect)
                pygame.draw.rect(screen, (255, 255, 255), close_button_rect, 3)  # Белая рамка при наведении
            else:
                # Обычный вид кнопки
                pygame.draw.rect(screen, (150, 50, 50), close_button_rect)
                pygame.draw.rect(screen, (255, 255, 0), close_button_rect, 2)  # Желтая рамка
            
            # Текст X в центре кнопки
            close_text = self.small_font.render("X", True, (255, 255, 255))
            close_text_rect = close_text.get_rect(center=close_button_rect.center)
            screen.blit(close_text, close_text_rect)
            
            # Подсказка для закрытия
            if self.dialog_stage == 1:
                close_hint = self.small_font.render("Нажмите X или ESC для закрытия", True, (150, 150, 150))
                screen.blit(close_hint, (dialog_x + 20, dialog_y + dialog_height - 25))
            

            
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
        
        # Поле ввода сообщения Диане
        if self.diana_message_input_active:
            # Фон поля ввода
            input_width = 400
            input_height = 80
            input_x = (self.screen_width - input_width) // 2
            input_y = self.screen_height - input_height - 50
            
            # Темный фон
            input_surface = pygame.Surface((input_width, input_height))
            input_surface.fill((20, 20, 30))
            
            # Рамка
            pygame.draw.rect(input_surface, (100, 80, 120), (0, 0, input_width, input_height), 3)
            pygame.draw.rect(input_surface, (60, 40, 80), (3, 3, input_width-6, input_height-6), 2)
            
            screen.blit(input_surface, (input_x, input_y))
            
            # Заголовок
            title_text = self.small_font.render("Сообщение Диане:", True, (255, 200, 100))
            screen.blit(title_text, (input_x + 15, input_y + 15))
            
            # Поле ввода
            input_rect = pygame.Rect(input_x + 15, input_y + 35, input_width - 30, 25)
            pygame.draw.rect(screen, (40, 40, 50), input_rect)
            pygame.draw.rect(screen, (100, 100, 120), input_rect, 2)
            
            # Текст в поле ввода с курсором
            cursor = "|" if int(pygame.time.get_ticks() / 500) % 2 else ""
            input_text = self.small_font.render(self.diana_message_input + cursor, True, (220, 220, 220))
            screen.blit(input_text, (input_x + 20, input_y + 40))
            
            # Инструкция
            instruction_text = self.small_font.render("Enter для отправки, ESC для отмены", True, (150, 150, 150))
            screen.blit(instruction_text, (input_x + 15, input_y + 60))
        
        # Поле ввода сообщения игрока (CEO)
        if self.player_message_input_active:
            # Фон поля ввода
            input_width = 400
            input_height = 80
            input_x = (self.screen_width - input_width) // 2
            input_y = self.screen_height - input_height - 50
            
            # Темный фон
            input_surface = pygame.Surface((input_width, input_height))
            input_surface.fill((20, 20, 30))
            
            # Рамка (синий цвет для игрока)
            pygame.draw.rect(input_surface, (100, 80, 120), (0, 0, input_width, input_height), 3)
            pygame.draw.rect(input_surface, (60, 40, 80), (3, 3, input_width-6, input_height-6), 2)
            
            screen.blit(input_surface, (input_x, input_y))
            
            # Заголовок
            title_text = self.small_font.render("Ваше сообщение:", True, (100, 200, 255))
            screen.blit(title_text, (input_x + 15, input_y + 15))
            
            # Поле ввода
            input_rect = pygame.Rect(input_x + 15, input_y + 35, input_width - 30, 25)
            pygame.draw.rect(screen, (40, 40, 50), input_rect)
            pygame.draw.rect(screen, (100, 100, 120), input_rect, 2)
            
            # Текст в поле ввода с курсором
            cursor = "|" if int(pygame.time.get_ticks() / 500) % 2 else ""
            input_text = self.small_font.render(self.player_message_input + cursor, True, (220, 220, 220))
            screen.blit(input_text, (input_x + 20, input_y + 40))
            
            # Инструкция
            instruction_text = self.small_font.render("Enter для отправки, ESC для отмены", True, (150, 150, 150))
            screen.blit(instruction_text, (input_x + 15, input_y + 60))
        
        # Подсказки о клавишах
        if not self.quiz_active and not self.diana_message_input_active and not self.player_message_input_active:
            t_hint_text = self.small_font.render('T - Написать сообщение Диане', True, (255, 255, 255))
            screen.blit(t_hint_text, (10, 50))
            y_hint_text = self.small_font.render('Y - Написать свое сообщение', True, (255, 255, 255))
            screen.blit(y_hint_text, (10, 70))
        
        # Отрисовка квиза
        if self.quiz_active:
            # Фон квиза
            quiz_width = 800
            quiz_height = 600
            quiz_x = (self.screen_width - quiz_width) // 2
            quiz_y = (self.screen_height - quiz_height) // 2
            
            # Темный фон
            quiz_surface = pygame.Surface((quiz_width, quiz_height))
            quiz_surface.fill((20, 20, 40))
            
            # Рамка
            pygame.draw.rect(quiz_surface, (100, 80, 120), (0, 0, quiz_width, quiz_height), 3)
            pygame.draw.rect(quiz_surface, (60, 40, 80), (3, 3, quiz_width-6, quiz_height-6), 2)
            
            screen.blit(quiz_surface, (quiz_x, quiz_y))
            
            if self.quiz_stage == 1:  # Приветствие
                title_text = self.font.render("Квиз от Армана", True, (255, 200, 100))
                welcome_text = self.small_font.render("Привет! Готов проверить свои знания Python?", True, (220, 220, 220))
                instruction_text = self.small_font.render("Нажмите Enter для начала квиза", True, (150, 150, 150))
                escape_text = self.small_font.render("ESC для выхода", True, (150, 150, 150))
                
                screen.blit(title_text, (quiz_x + (quiz_width - title_text.get_width()) // 2, quiz_y + 50))
                screen.blit(welcome_text, (quiz_x + (quiz_width - welcome_text.get_width()) // 2, quiz_y + 150))
                screen.blit(instruction_text, (quiz_x + (quiz_width - instruction_text.get_width()) // 2, quiz_y + 200))
                screen.blit(escape_text, (quiz_x + (quiz_width - escape_text.get_width()) // 2, quiz_y + 250))
            
            elif self.quiz_stage == 2:  # Вопросы
                current_q = self.quiz_questions[self.current_question]
                
                # Заголовок
                question_num = self.small_font.render(f"Вопрос {self.current_question + 1} из {len(self.quiz_questions)}", True, (255, 200, 100))
                screen.blit(question_num, (quiz_x + 20, quiz_y + 20))
                
                # Вопрос
                question_text = self.small_font.render(current_q["question"], True, (220, 220, 220))
                screen.blit(question_text, (quiz_x + 20, quiz_y + 60))
                
                # Варианты ответов
                for i, answer in enumerate(current_q["answers"]):
                    color = (255, 255, 255) if i == self.selected_answer else (150, 150, 150)
                    bg_color = (100, 80, 120) if i == self.selected_answer else (40, 40, 60)
                    
                    # Фон для выбранного ответа
                    answer_rect = pygame.Rect(quiz_x + 20, quiz_y + 120 + i * 50, quiz_width - 40, 40)
                    pygame.draw.rect(screen, bg_color, answer_rect)
                    pygame.draw.rect(screen, color, answer_rect, 2)
                    
                    answer_text = self.small_font.render(f"{chr(65 + i)}. {answer}", True, color)
                    screen.blit(answer_text, (quiz_x + 30, quiz_y + 130 + i * 50))
                
                # Инструкции
                instruction_text = self.small_font.render("↑↓ для выбора, Enter для ответа, ESC для выхода", True, (150, 150, 150))
                screen.blit(instruction_text, (quiz_x + 20, quiz_y + quiz_height - 40))
            
            elif self.quiz_stage == 3:  # Показ ответа
                current_q = self.quiz_questions[self.current_question]
                
                # Заголовок
                result_title = self.font.render("Результат ответа", True, (255, 200, 100))
                screen.blit(result_title, (quiz_x + (quiz_width - result_title.get_width()) // 2, quiz_y + 50))
                
                # Вопрос
                question_text = self.small_font.render(current_q["question"], True, (220, 220, 220))
                screen.blit(question_text, (quiz_x + 20, quiz_y + 100))
                
                # Ваш ответ
                your_answer = current_q["answers"][self.selected_answer]
                your_answer_text = self.small_font.render(f"Ваш ответ: {chr(65 + self.selected_answer)}. {your_answer}", True, (150, 150, 150))
                screen.blit(your_answer_text, (quiz_x + 20, quiz_y + 140))
                
                # Правильный ответ
                correct_answer = current_q["answers"][current_q["correct"]]
                correct_answer_text = self.small_font.render(f"Правильный ответ: {chr(65 + current_q['correct'])}. {correct_answer}", True, (100, 255, 100))
                screen.blit(correct_answer_text, (quiz_x + 20, quiz_y + 170))
                
                # Результат
                if self.selected_answer == current_q["correct"]:
                    result_text = self.small_font.render("✅ Правильно!", True, (100, 255, 100))
                else:
                    result_text = self.small_font.render("❌ Неправильно!", True, (255, 100, 100))
                screen.blit(result_text, (quiz_x + 20, quiz_y + 200))
                
                # Инструкция
                instruction_text = self.small_font.render("Нажмите Enter для продолжения (автоматически через 2 сек)", True, (150, 150, 150))
                screen.blit(instruction_text, (quiz_x + 20, quiz_y + quiz_height - 40))
            
            elif self.quiz_stage == 4:  # Результаты
                # Заголовок
                result_title = self.font.render("Результаты квиза", True, (255, 200, 100))
                screen.blit(result_title, (quiz_x + (quiz_width - result_title.get_width()) // 2, quiz_y + 50))
                
                # Результат
                score_text = self.small_font.render(f"Правильных ответов: {self.correct_answers} из {self.total_questions}", True, (220, 220, 220))
                screen.blit(score_text, (quiz_x + (quiz_width - score_text.get_width()) // 2, quiz_y + 150))
                
                # Процент
                percentage = (self.correct_answers / self.total_questions) * 100
                percentage_text = self.small_font.render(f"Процент правильных ответов: {percentage:.1f}%", True, (220, 220, 220))
                screen.blit(percentage_text, (quiz_x + (quiz_width - percentage_text.get_width()) // 2, quiz_y + 200))
                
                # Оценка
                if percentage >= 80:
                    grade = "Отлично! 🎉"
                    grade_color = (100, 255, 100)
                elif percentage >= 60:
                    grade = "Хорошо! 👍"
                    grade_color = (255, 255, 100)
                elif percentage >= 40:
                    grade = "Удовлетворительно 😊"
                    grade_color = (255, 200, 100)
                else:
                    grade = "Нужно подучиться 📚"
                    grade_color = (255, 100, 100)
                
                grade_text = self.small_font.render(grade, True, grade_color)
                screen.blit(grade_text, (quiz_x + (quiz_width - grade_text.get_width()) // 2, quiz_y + 250))
                
                # Инструкция
                instruction_text = self.small_font.render("Нажмите Enter для выхода", True, (150, 150, 150))
                screen.blit(instruction_text, (quiz_x + (quiz_width - instruction_text.get_width()) // 2, quiz_y + 320)) 