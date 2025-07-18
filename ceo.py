import pygame
import sys
import os
from scenes.university_entrance import UniversityEntranceScene
from scenes.corridor import CorridorScene
from scenes.lecture_room import LectureRoomScene
from scenes.lecture_hall import LectureHallScene
from scenes.location1 import Location1Scene

from scenes.daylick_scene import DaylickScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Инициализация звуковой системы
        
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Quiz Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Инициализация музыки
        self.music_playing = False
        self.music_volume = 0.5
        self.load_music()
        
        # Инициализация сцен
        self.scenes = {
            'UniversityEntrance': UniversityEntranceScene(self),
            'CorridorScene': CorridorScene(self),
            'LectureRoom': LectureRoomScene(self),
            'LectureHallScene': LectureHallScene(self),
            'Location1': Location1Scene(self),
            'DaylickScene': DaylickScene(self)
        }
        
        self.current_scene = 'UniversityEntrance'
        self.scene_history = ['UniversityEntrance']  # История навигации
        
    def load_music(self):
        """Загрузка музыки"""
        try:
            music_path = os.path.join('assets', 'mp3', 'talap.mp3')
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                print(f"Музыка загружена: {music_path}")
            else:
                print(f"Файл музыки не найден: {music_path}")
        except Exception as e:
            print(f"Ошибка при загрузке музыки: {e}")
    
    def play_music(self):
        """Воспроизведение музыки"""
        try:
            if not self.music_playing:
                pygame.mixer.music.play(-1)  # -1 означает бесконечное воспроизведение
                self.music_playing = True
                print("Музыка начала играть")
        except Exception as e:
            print(f"Ошибка при воспроизведении музыки: {e}")
    
    def stop_music(self):
        """Остановка музыки"""
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
            print("Музыка остановлена")
        except Exception as e:
            print(f"Ошибка при остановке музыки: {e}")
    
    def pause_music(self):
        """Пауза музыки"""
        try:
            pygame.mixer.music.pause()
            self.music_playing = False
            print("Музыка поставлена на паузу")
        except Exception as e:
            print(f"Ошибка при паузе музыки: {e}")
    
    def unpause_music(self):
        """Возобновление музыки"""
        try:
            pygame.mixer.music.unpause()
            self.music_playing = True
            print("Музыка возобновлена")
        except Exception as e:
            print(f"Ошибка при возобновлении музыки: {e}")
    
    def set_music_volume(self, volume):
        """Установка громкости музыки (0.0 - 1.0)"""
        try:
            self.music_volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(self.music_volume)
            print(f"Громкость музыки установлена: {self.music_volume}")
        except Exception as e:
            print(f"Ошибка при установке громкости: {e}")
        
    def change_scene(self, scene_name, data=None):
        if scene_name in self.scenes:
            # Добавляем текущую сцену в историю, если это не возврат назад
            if scene_name != self.current_scene:
                self.scene_history.append(self.current_scene)
            self.current_scene = scene_name
            self.scenes[scene_name].reset(data)
    
    def go_back(self):
        """Возврат к предыдущей сцене"""
        if len(self.scene_history) > 0:
            previous_scene = self.scene_history.pop()
            self.current_scene = previous_scene
            self.scenes[previous_scene].reset()
        else:
            # Если нет предыдущих сцен, выходим из игры
            self.running = False
    
    def run(self):
        # Автоматически запускаем музыку при старте игры
        self.play_music()
        
        while self.running:
            try:
                dt = self.clock.tick(60) / 1000.0
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Возврат к предыдущей сцене при нажатии ESC
                            self.go_back()
                        elif event.key == pygame.K_m:
                            # Управление музыкой клавишей M
                            if self.music_playing:
                                self.pause_music()
                            else:
                                self.unpause_music()
                        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                            # Увеличение громкости
                            self.set_music_volume(self.music_volume + 0.1)
                        elif event.key == pygame.K_MINUS:
                            # Уменьшение громкости
                            self.set_music_volume(self.music_volume - 0.1)
                    try:
                        self.scenes[self.current_scene].handle_event(event)
                    except Exception as e:
                        print(f"Ошибка в handle_event: {e}")
                
                try:
                    self.scenes[self.current_scene].update(dt)
                except Exception as e:
                    print(f"Ошибка в update: {e}")
                
                try:
                    self.scenes[self.current_scene].draw(self.screen)
                except Exception as e:
                    print(f"Ошибка в draw: {e}")
                
                pygame.display.flip()
                
            except Exception as e:
                print(f"Критическая ошибка в игровом цикле: {e}")
                self.running = False
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 