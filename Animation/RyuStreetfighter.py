from telnetlib import SE
import pygame
from pygame.constants import (QUIT, K_KP_PLUS, K_KP_MINUS, K_ESCAPE, KEYDOWN)
import os



class Settings(object):


    # Overlay
    window = {'width':300, 'height':200}
    fps = 60
    title = "Animation"

    #paths
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "fighter")

    # Dicgenery

    directions = {'stop':(0, 0), 'down':(0,  1), 'up':(0, -1), 'left':(-1, 0), 'right':(1, 0)}
    animations = {'jump': (0, 8), 'kick': (9, 17), 'punch': (18, 21), 'stand': (22, 30)}

    sprite_numb = 31
    images  = []
    
    @staticmethod
    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)

    @staticmethod
    def load_images():
        for i in range(Settings.sprite_numb):
            Settings.images.append(pygame.image.load(Settings.imagepath(f"{i}.png")))


class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0



class Animation(object):
    def __init__(self, animation):
        self.timer = Timer(100)
        self.images_for_animation = Settings.animations[animation]
        self.image_start = self.images_for_animation[0]
        self.image_end = self.images_for_animation[1]
        self.image_index = self.image_start

    def next(self):
        if self.timer.is_next_stop_reached() and self.image_index <= self.image_end:
            self.image_index += 1
            if self.image_index >= len(Settings.images):
                self.image_index = len(Settings.images) - 1
        return Settings.images[self.image_index]

    def is_ended(self):
        return self.image_index >= len(Settings.images) - 1



class Ryu(pygame.sprite.Sprite):
    def __init__(self,animations):
        super().__init__()
        self.animation = Animation(animations)        
        self.image = self.animation.next()
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)

    def update(self):
        self.image = self.animation.next()



class RyuGame(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        Settings.load_images()
        self.Ryu = pygame.sprite.GroupSingle(Ryu('kick'))
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_1:
                    self.Ryu = pygame.sprite.GroupSingle(Ryu('kick'))
                if event.key == pygame.K_2:
                    self.Ryu = pygame.sprite.GroupSingle(Ryu('jump'))
                if event.key == pygame.K_3:
                    self.Ryu = pygame.sprite.GroupSingle(Ryu('stand'))
                if event.key == pygame.K_4:
                    self.Ryu = pygame.sprite.GroupSingle(Ryu('punch'))


    def update(self) -> None:
        self.Ryu.update()

    def draw(self) -> None:
        self.screen.fill((200, 200, 200))
        self.Ryu.draw(self.screen)
        pygame.display.flip()



if __name__ == '__main__':
    anim = RyuGame()
    anim.run()

