import pygame
from settings import *
from typing import List

class Generic(pygame.sprite.Sprite):
    def __init__(self, position:tuple, surface:pygame.surface.Surface, groups:pygame.sprite.Group, z:int = LAYERS['main']):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.z = z

class Water(Generic):
    def __init__(self, position:tuple, frames:List[pygame.surface.Surface], groups:pygame.sprite.Group):
        # Animation Setup
        self.frames = frames
        self.frame_index = 0

        # Sprite Setup
        super().__init__(
            position=position,
            surface=self.frames[self.frame_index],
            groups=groups,
            z=LAYERS['water']
        )
    
    def animate(self, dt):
        # 5*dt means 5 frames per second, and the mod makes sure our frame index is always in range
        self.frame_index = (self.frame_index + 5*dt) % len(self.frames)
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, position:tuple, surface:pygame.surface.Surface, groups:pygame.sprite.Group):
        super().__init__(
            position=position,
            surface=surface,
            groups=groups,
            z=LAYERS['main']
        )

class Tree(Generic):
    def __init__(self, position:tuple, surface:pygame.surface.Surface, groups:pygame.sprite.Group, name:str):
        super().__init__(
            position=position,
            surface=surface,
            groups=groups,
            z=LAYERS['main']
        )