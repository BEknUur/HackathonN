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
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Quiz Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
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
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Возврат в главное меню при нажатии ESC
                        self.running = False
                        return
                self.scenes[self.current_scene].handle_event(event)
            
            self.scenes[self.current_scene].update(dt)
            self.scenes[self.current_scene].draw(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 