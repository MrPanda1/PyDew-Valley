from json import load
import pygame
from helper import import_folder
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self) -> None:
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite Groups
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self) -> None:
        # Get all data from Tile
        tmx_data = load_pygame('../assets/data/map.tmx')
        tmx_layers_to_sprites = [       # Create a list of all the sprites to be drawn: (tmx_layer, z_layer)
            ('HouseFloor', 'house_bottom'),
            ('HouseFurnitureBottom', 'house_bottom'),
            ('HouseWalls', 'main'),
            ('HouseFurnitureTop', 'main'),
            ('Fence', 'main')
        ]

        # House and Fence
        for tmx_layer, z_layer in tmx_layers_to_sprites:
            for x, y, surface in tmx_data.get_layer_by_name(tmx_layer).tiles():
                Generic(
                    position=(x * TILE_SIZE, y * TILE_SIZE),
                    surface=surface,
                    groups=self.all_sprites,
                    z=LAYERS[z_layer]
                )
        
        # Water
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water(
                position=(x * TILE_SIZE, y * TILE_SIZE),
                frames=import_folder('../assets/graphics/water'),
                groups=self.all_sprites
            )
        
        # Wild Flowers
        for object in tmx_data.get_layer_by_name('Decoration'):
            WildFlower(
                position=(object.x, object.y),
                surface=object.image,
                groups=self.all_sprites
            )
        
        # Trees
        for object in tmx_data.get_layer_by_name('Trees'):
            Tree(
                position=(object.x, object.y),
                surface=object.image,
                groups=self.all_sprites,
                name=object.name
            )

        # Draw the world map
        Generic(
            position=(0, 0),
            surface=pygame.image.load('../assets/graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground']
        )

        # Draw the player
        self.player = Player((950, 500), self.all_sprites)

    def run(self, dt) -> None:
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)
    
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.display_surface.get_width()/2
        self.offset.y = player.rect.centery - self.display_surface.get_height()/2

        for layer in LAYERS.values():       # Python 3.7+ guarantees the order of these to be deterministic, otherwise we would do: sorted(LAYERS.values(), key=lambda x: x)
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    # Create offset to move everything in relation to the player (aka camera)
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset

                    # Draw the sprite
                    self.display_surface.blit(sprite.image, offset_rect)
