import pygame
from random import randint
import pathlib

pygame.init()
path = pathlib.Path(__file__).parent.resolve()

fx = pygame.mixer.Sound(f"{path}/assets/mp3/blip.mp3")
fx.set_volume(0.5)

base = f"{path}/assets/students/"
students = [
    [f"{base}a1.png", f"{base}a2.png", f"{base}a3.png"],
    [f"{base}b1.png", f"{base}b2.png", f"{base}b3.png"],
    [f"{base}c1.png", f"{base}c2.png", f"{base}c3.png"],
    [f"{base}j1.png", f"{base}j2.png", f"{base}j3.png"],
    [f"{base}k1.png", f"{base}k2.png", f"{base}k3.png"]
]

class Student(pygame.sprite.Sprite):
    def __init__(self, x, y, id, a, b):
        super().__init__()
        self.status = 'awake'
        self.id = id
        self.i = randint(0, len(students)-1)
        self.image = pygame.image.load(students[self.i][0])
        self.rect = self.image.get_rect(center=(x, y))

        self.a, self.b = a, b
        self.energy = 125
        self.energy_speed = randint(a, b)
        self.next_time = pygame.time.get_ticks()

    def energy_drain(self):
        now = pygame.time.get_ticks()
        if now >= self.next_time and self.energy > 0:
            self.next_time += self.energy_speed
            self.energy -= 25
        if self.energy > 50:
            self.image = pygame.image.load(students[self.i][0]); self.status = 'awake'
        elif self.energy > 0:
            self.image = pygame.image.load(students[self.i][1]); self.status = 'half_sleepy'
        else:
            self.image = pygame.image.load(students[self.i][2]); self.status = 'asleep'

    def click_event(self, mx, my):
        if self.status == 'asleep' and self.rect.collidepoint(mx, my):
            self.energy = 125
            fx.play()

    def change_speed(self):
        if self.a > 3000 and self.b > 3000:
            self.a -= 3000; self.b -= 3000
        self.energy_speed = randint(self.a, self.b)
