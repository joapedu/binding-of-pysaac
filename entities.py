import pygame
import math
from typing import Tuple

class Entity:
    def __init__(self, x: float, y: float, size: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.health = 100
        self.max_health = 100
    
    @property
    def alive(self) -> bool:
        return self.health > 0
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.size)

        bar_width = self.size * 2
        bar_height = 4
        bar_x = screen_x - bar_width // 2
        bar_y = screen_y - self.size - 8
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))

class Player(Entity):
    def __init__(self, x: float, y: float, config: dict):
        super().__init__(x, y, config['size'], config['color'])
        self.max_health = config['max_health']
        self.health = self.max_health
        self.speed = config['speed']
        self.direction = 0
        self.health_items = 0
        self.ammo_items = 0
    
    def move(self, dx: float, dy: float, dt: float):
        if dx != 0 or dy != 0:
            self.direction = math.atan2(dy, dx)
        
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
    
    def take_damage(self, damage: int):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount: int):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    
    def use_health_item(self):
        if self.health_items > 0:
            self.heal(30)
            self.health_items -= 1
            return True
        return False
    
    def use_ammo_item(self, enemies, damage, radius):
        if self.ammo_items > 0:
            killed_enemies = []
            for enemy in enemies:
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= radius:
                    enemy.take_damage(damage)
                    if enemy.health <= 0:
                        killed_enemies.append(enemy)
            self.ammo_items -= 1
            return killed_enemies
        return []

class Enemy(Entity):
    def __init__(self, x: float, y: float, config: dict):
        super().__init__(x, y, config['size'], config['color'])
        self.max_health = config['health']
        self.health = self.max_health
        self.speed = config['speed']
        self.damage = config['damage']
        self.damage_interval = config['damage_interval']
        self.last_damage_time = 0
    
    def update(self, player: Player, dt: float) -> bool:
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            dx /= distance
            dy /= distance
            
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt
        
        if self.get_rect().colliderect(player.get_rect()):
            current_time = pygame.time.get_ticks() / 1000.0
            if current_time - self.last_damage_time >= self.damage_interval:
                player.take_damage(self.damage)
                self.last_damage_time = current_time
        
        return self.health > 0
    
    def take_damage(self, damage: int):
        self.health -= damage
        if self.health < 0:
            self.health = 0

class Item(Entity):
    def __init__(self, x: float, y: float, item_type: str, config: dict):
        super().__init__(x, y, config['size'], config['color'])
        self.item_type = item_type
        self.config = config
        self.health = 1
        self.max_health = 1
    
    @property
    def symbol(self) -> str:
        return self.config.get('symbol', '?')
    
    def collect(self, player: Player) -> bool:
        if self.get_rect().colliderect(player.get_rect()):
            if self.item_type == 'health':
                player.health_items += 1
            elif self.item_type == 'ammo':
                player.ammo_items += 1
            return True
        return False
    
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.size)
        
        font = pygame.font.Font(None, 24)
        text = font.render(self.config['symbol'], True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_x, screen_y))
        screen.blit(text, text_rect)