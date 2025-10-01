import pygame
import math
import random
from typing import Tuple, List

class SpriteRenderer:
    def __init__(self, config=None):
        self.config = config
        self.colors = {
            'player': (0, 255, 0),
            'enemy': (255, 165, 0),
            'health_item': (255, 255, 0),
            'ammo_item': (0, 255, 255),
            'background': (40, 60, 40),
            'wall': (80, 60, 40),
            'floor': (60, 80, 60)
        }
        
        if config and 'enemies' in config:
            self.colors['enemy'] = tuple(config['enemies']['color'])
    
    def draw_player(self, screen: pygame.Surface, x: int, y: int, size: int, direction: float = 0):
        """Desenha o jogador com visual melhorado"""
        body_rect = pygame.Rect(x - size//2, y - size//2, size, size)
        pygame.draw.ellipse(screen, self.colors['player'], body_rect)
        
        pygame.draw.ellipse(screen, (0, 200, 0), body_rect, 2)
        
        eye_size = max(2, size // 8)
        eye_offset = size // 4
        
        left_eye_x = x - eye_offset
        left_eye_y = y - eye_offset
        pygame.draw.circle(screen, (255, 255, 255), (left_eye_x, left_eye_y), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (left_eye_x, left_eye_y), eye_size//2)
        
        right_eye_x = x + eye_offset
        right_eye_y = y - eye_offset
        pygame.draw.circle(screen, (255, 255, 255), (right_eye_x, right_eye_y), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (right_eye_x, right_eye_y), eye_size//2)
        
        if direction != 0:
            end_x = x + int(math.cos(direction) * size//2)
            end_y = y + int(math.sin(direction) * size//2)
            pygame.draw.line(screen, (0, 200, 0), (x, y), (end_x, end_y), 2)
    
    def draw_enemy(self, screen: pygame.Surface, x: int, y: int, size: int, health: int, max_health: int):
        """Desenha inimigo com visual melhorado"""
        body_rect = pygame.Rect(x - size//2, y - size//2, size, size)
        pygame.draw.ellipse(screen, self.colors['enemy'], body_rect)
        
        pygame.draw.ellipse(screen, (200, 100, 0), body_rect, 2)
        
        eye_size = max(2, size // 6)
        eye_offset = size // 3
        
        left_eye_x = x - eye_offset
        left_eye_y = y - eye_offset
        pygame.draw.circle(screen, (255, 200, 0), (left_eye_x, left_eye_y), eye_size)
        
        right_eye_x = x + eye_offset
        right_eye_y = y - eye_offset
        pygame.draw.circle(screen, (255, 200, 0), (right_eye_x, right_eye_y), eye_size)
        
        if health < max_health:
            bar_width = size
            bar_height = 4
            bar_x = x - bar_width//2
            bar_y = y - size//2 - 8
            
            pygame.draw.rect(screen, (150, 80, 0), (bar_x, bar_y, bar_width, bar_height))
            
            health_ratio = health / max_health
            health_width = int(bar_width * health_ratio)
            pygame.draw.rect(screen, (255, 165, 0), (bar_x, bar_y, health_width, bar_height))
    
    def draw_health_item(self, screen: pygame.Surface, x: int, y: int, size: int):
        """Desenha item de saúde com visual melhorado"""
        pygame.draw.circle(screen, (255, 255, 200), (x, y), size//2)
        pygame.draw.circle(screen, (200, 200, 0), (x, y), size//2, 2)
        
        cross_size = size//3
        pygame.draw.rect(screen, (255, 0, 0), (x - 2, y - cross_size, 4, cross_size*2))
        pygame.draw.rect(screen, (255, 0, 0), (x - cross_size, y - 2, cross_size*2, 4))
        
        pygame.draw.circle(screen, (255, 255, 255), (x - size//4, y - size//4), size//8)
    
    def draw_ammo_item(self, screen: pygame.Surface, x: int, y: int, size: int):
        """Desenha item de munição com visual melhorado"""
        pygame.draw.circle(screen, (200, 255, 255), (x, y), size//2)
        pygame.draw.circle(screen, (0, 200, 200), (x, y), size//2, 2)
        
        for i in range(4):
            angle = i * math.pi / 2
            start_x = x + int(math.cos(angle) * size//4)
            start_y = y + int(math.sin(angle) * size//4)
            end_x = x + int(math.cos(angle) * size//2)
            end_y = y + int(math.sin(angle) * size//2)
            pygame.draw.line(screen, (0, 255, 255), (start_x, start_y), (end_x, end_y), 2)
        
        pygame.draw.circle(screen, (255, 255, 255), (x, y), size//6)
    
    def draw_background_tile(self, screen: pygame.Surface, x: int, y: int, size: int, tile_type: str = 'floor'):
        """Desenha tile de fundo"""
        rect = pygame.Rect(x, y, size, size)
        
        if tile_type == 'floor':
            pygame.draw.rect(screen, self.colors['floor'], rect)
            pygame.draw.rect(screen, (50, 70, 50), rect, 1)
            if random.random() < 0.1:
                pygame.draw.circle(screen, (40, 60, 40), (x + size//2, y + size//2), 2)
        elif tile_type == 'wall':
            pygame.draw.rect(screen, self.colors['wall'], rect)
            pygame.draw.rect(screen, (60, 40, 20), rect, 2)
            for i in range(0, size, 8):
                pygame.draw.line(screen, (100, 80, 60), (x, y + i), (x + size, y + i), 1)
    
    def draw_area_background(self, screen: pygame.Surface, area_x: int, area_y: int, area_size: int):
        """Desenha fundo de uma área"""
        pygame.draw.rect(screen, self.colors['background'], (area_x, area_y, area_size, area_size))
        
        pygame.draw.rect(screen, (60, 80, 60), (area_x, area_y, area_size, area_size), 3)
        
        tile_size = 32
        for y in range(area_y, area_y + area_size, tile_size):
            for x in range(area_x, area_x + area_size, tile_size):
                tile_type = 'floor'
                if (x == area_x or x == area_x + area_size - tile_size or 
                    y == area_y or y == area_y + area_size - tile_size):
                    tile_type = 'wall'
                
                self.draw_background_tile(screen, x, y, tile_size, tile_type)
    
    def draw_particle_effect(self, screen: pygame.Surface, x: int, y: int, color: Tuple[int, int, int], count: int = 5):
        """Desenha efeito de partículas"""
        for _ in range(count):
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            size = random.randint(1, 3)
            pygame.draw.circle(screen, color, (x + offset_x, y + offset_y), size)
    
    def draw_damage_number(self, screen: pygame.Surface, x: int, y: int, damage: int, color: Tuple[int, int, int] = (255, 0, 0)):
        """Desenha número de dano flutuante"""
        font = pygame.font.Font(None, 24)
        text = font.render(f"-{damage}", True, color)
        screen.blit(text, (x, y))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x: int, y: int, color: Tuple[int, int, int], count: int = 10):
        """Adiciona explosão de partículas"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            lifetime = random.uniform(0.5, 1.5)
            
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': color,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': random.randint(2, 5)
            }
            self.particles.append(particle)
    
    def update(self, dt: float):
        """Atualiza partículas"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['lifetime'] -= dt
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Desenha partículas"""
        for particle in self.particles:
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            size = int(particle['size'] * (particle['lifetime'] / particle['max_lifetime']))
            
            if size > 0:
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), size)
