import pygame

class Timer:
    def __init__(self, duration:int, func:callable = None) -> None:
        # Initialize variables
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
    
    def activate(self) -> None:
        self.start_time = pygame.time.get_ticks()
        self.active = True
    
    def deactivate(self) -> None:
        self.active = False
    
    def update(self) -> None:
        if self.active:
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                self.deactivate()
                if self.func:
                    self.func()