import pygame
from timer import Timer
from settings import *
from helper import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group) -> None:
        super().__init__(group)

        # Initalize sprites
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # General Setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=position)
        self.z = LAYERS['main']     # z = what order to render in

        # Movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Timers
        self.timers = {
            'tool_use': Timer(500, self.use_tool),  # 500 ms = 0.5 seconds, bc there are 2 frames taking .25 seconds each
            'tool_switch': Timer(250),
            'seed_use': Timer(500, self.use_seed),
            'seed_switch': Timer(250),
        }

        # Tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
    
    def use_tool(self) -> None:
        print(self.selected_tool)
    
    def use_seed(self) -> None:
        print(self.selected_seed)

    def import_assets(self) -> None:
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
            'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
            'up_water': [], 'down_water': [], 'left_water': [], 'right_water': []
        }

        for animation in self.animations:
            full_path = '../assets/graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt) -> None:
        # 4*dt means 4 frames per second, and the mod makes sure our frame index is always in range
        self.frame_index = (self.frame_index + 4*dt) % len(self.animations[self.status])
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self) -> None:
        # Do not allow any other input while tool is active
        if self.timers['tool_use'].active:
            return
        
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        # Tool Use
        if keys[pygame.K_SPACE]:
            self.direction = pygame.math.Vector2(0, 0)
            self.frame_index = 0
            self.timers['tool_use'].activate()
        
        # Switch Tools
        if keys[pygame.K_q] and not self.timers['tool_switch'].active:
            self.timers['tool_switch'].activate()
            self.tool_index = (self.tool_index + 1) % len(self.tools)
            self.selected_tool = self.tools[self.tool_index]
        
        # Seed Use
        if keys[pygame.K_LCTRL]:
            self.direction = pygame.math.Vector2(0, 0)
            self.frame_index = 0
            self.timers['seed_use'].activate()
        
        # Switch Seeds
        if keys[pygame.K_e] and not self.timers['seed_switch'].active:
            self.timers['seed_switch'].activate()
            self.seed_index = (self.seed_index + 1) % len(self.seeds)
            self.selected_seed = self.seeds[self.seed_index]
    
    def get_status(self) -> None:
        # Movement
        if self.direction.y < 0:
            self.status = 'up'
        elif self.direction.y > 0:
            self.status = 'down'
        
        if self.direction.x < 0:
            self.status = 'left'
        elif self.direction.x > 0:
            self.status = 'right'

        # Idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        # Tool
        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()

    def move(self, dt) -> None:
        # Normalize vector so diagonal movement is not faster
        if self.direction.magnitude() != 0:
            self.direction.normalize_ip()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt) -> None:
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)