import pygame
import random
import yaml
from typing import List, Tuple, Dict
from entities import Player, Enemy, Item

class Area:
    def __init__(self, grid_x: int, grid_y: int, area_size: int, config: Dict):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.area_size = area_size
        self.x = grid_x * area_size
        self.y = grid_y * area_size
        self.active = False
        self.enemies: List[Enemy] = []
        self.items: List[Item] = []
        self.config = config
        
        self.generate_content()
    
    def generate_content(self):
        """Gera conteúdo para a área"""
        spawn_config = self.config['spawn']
        
        for _ in range(spawn_config['enemies_per_area']):
            x = random.uniform(self.x + 20, self.x + self.area_size - 20)
            y = random.uniform(self.y + 20, self.y + self.area_size - 20)
            enemy = Enemy(x, y, self.config['enemies'])
            self.enemies.append(enemy)
        
        for _ in range(spawn_config['health_items_per_area']):
            x = random.uniform(self.x + 15, self.x + self.area_size - 15)
            y = random.uniform(self.y + 15, self.y + self.area_size - 15)
            item = Item(x, y, 'health', self.config['items']['health'])
            self.items.append(item)
        
        for _ in range(spawn_config['ammo_items_per_area']):
            x = random.uniform(self.x + 15, self.x + self.area_size - 15)
            y = random.uniform(self.y + 15, self.y + self.area_size - 15)
            item = Item(x, y, 'ammo', self.config['items']['ammo'])
            self.items.append(item)
    
    def update(self, player: Player, dt: float):
        if not self.active:
            return
        
        for enemy in self.enemies[:]:
            if not enemy.update(player, dt):
                self.enemies.remove(enemy)
        
        for item in self.items[:]:
            if item.collect(player):
                self.items.remove(item)
    
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        if not self.active:
            return
        
        area_rect = pygame.Rect(
            int(self.x - camera_x),
            int(self.y - camera_y),
            self.area_size,
            self.area_size
        )
        pygame.draw.rect(screen, (40, 40, 40), area_rect)
        pygame.draw.rect(screen, (100, 100, 100), area_rect, 2)
        
        for enemy in self.enemies:
            enemy.draw(screen, camera_x, camera_y)
        
        for item in self.items:
            item.draw(screen, camera_x, camera_y)
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.area_size, self.area_size)

class World:
    def __init__(self, config_path: str = 'config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.area_size = self.config['world']['area_size']
        self.grid_size = self.config['world']['grid_size']
        self.activation_distance = self.config['world']['activation_distance']
        self.max_active_areas = self.config['world']['max_active_areas']
        
        self.areas: List[Area] = []
        self.active_areas: List[Area] = []
        
        self.generate_world()
    
    def generate_world(self):
        """Gera o mundo com todas as áreas"""
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                area = Area(x, y, self.area_size, self.config)
                self.areas.append(area)
        
        center_area = self.get_area(1, 1)
        if center_area:
            center_area.active = True
            self.active_areas.append(center_area)
    
    def get_area(self, grid_x: int, grid_y: int) -> Area:
        """Retorna a área nas coordenadas do grid"""
        for area in self.areas:
            if area.grid_x == grid_x and area.grid_y == grid_y:
                return area
        return None
    
    def get_area_at_position(self, x: float, y: float) -> Area:
        """Retorna a área que contém a posição"""
        grid_x = int(x // self.area_size)
        grid_y = int(y // self.area_size)
        return self.get_area(grid_x, grid_y)
    
    def update_active_areas(self, player: Player):
        """Atualiza quais áreas estão ativas"""
        current_area = self.get_area_at_position(player.x, player.y)
        if not current_area:
            return
        
        new_active_areas = [current_area]
        
        for area in self.areas:
            if area == current_area:
                continue
            
            distance = self.get_distance_to_area(player, area)
            if distance <= self.activation_distance:
                new_active_areas.append(area)
        
        new_active_areas = new_active_areas[:self.max_active_areas]
        
        for area in self.active_areas:
            if area not in new_active_areas:
                area.active = False
        
        for area in new_active_areas:
            if area not in self.active_areas:
                area.active = True
        
        self.active_areas = new_active_areas
    
    def get_distance_to_area(self, player: Player, area: Area) -> float:
        """Calcula a distância do jogador para a área"""
        player_rect = player.get_rect()
        area_rect = area.get_rect()
        
        dx = max(0, max(player_rect.left - area_rect.right, area_rect.left - player_rect.right))
        dy = max(0, max(player_rect.top - area_rect.bottom, area_rect.top - player_rect.bottom))
        
        return (dx**2 + dy**2)**0.5
    
    def update(self, player: Player, dt: float):
        """Atualiza o mundo"""
        self.update_active_areas(player)
        
        for area in self.active_areas:
            area.update(player, dt)
    
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Desenha o mundo"""
        for area in self.active_areas:
            area.draw(screen, camera_x, camera_y)
    
    def draw_grid(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Desenha o grid completo"""
        for area in self.areas:
            rect = area.get_rect()
            screen_rect = pygame.Rect(
                rect.x - camera_x,
                rect.y - camera_y,
                rect.width,
                rect.height
            )
            
            pygame.draw.rect(screen, (40, 40, 40), screen_rect)
            
            color = (100, 100, 100) if area.active else (50, 50, 50)
            pygame.draw.rect(screen, color, screen_rect, 3)
    
    @property
    def enemies(self) -> List[Enemy]:
        """Retorna todos os inimigos das áreas ativas"""
        all_enemies = []
        for area in self.active_areas:
            all_enemies.extend(area.enemies)
        return all_enemies