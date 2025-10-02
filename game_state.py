import json
import yaml
import random
from typing import Dict, List, Any
from entities import Player, Enemy, Item

class GameState:
    def __init__(self):
        self.player_data = {}
        self.areas_data = []
        self.game_config = {}
        self.metadata = {}
    
    def save_to_json(self, filename: str):
        state = {
            'metadata': self.metadata,
            'player': self.player_data,
            'areas': self.areas_data,
            'config': self.game_config
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def save_to_yaml(self, filename: str):
        state = {
            'metadata': self.metadata,
            'player': self.player_data,
            'areas': self.areas_data,
            'config': self.game_config
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(state, f, default_flow_style=False, allow_unicode=True)
    
    def load_from_json(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        self.metadata = state.get('metadata', {})
        self.player_data = state.get('player', {})
        self.areas_data = state.get('areas', [])
        self.game_config = state.get('config', {})
    
    def load_from_yaml(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f)
        
        self.metadata = state.get('metadata', {})
        self.player_data = state.get('player', {})
        self.areas_data = state.get('areas', [])
        self.game_config = state.get('config', {})

class GameStateManager:
    def __init__(self, world, player, config):
        self.world = world
        self.player = player
        self.config = config
    
    def capture_current_state(self) -> GameState:
        state = GameState()
        
        state.metadata = {
            'timestamp': pygame.time.get_ticks() / 1000.0,
            'active_areas_count': len(self.world.active_areas),
            'total_enemies': sum(len(area.enemies) for area in self.world.areas),
            'total_items': sum(len(area.items) for area in self.world.areas)
        }
        
        state.player_data = {
            'x': self.player.x,
            'y': self.player.y,
            'health': self.player.health,
            'max_health': self.player.max_health,
            'health_items': self.player.health_items,
            'ammo_items': self.player.ammo_items
        }
        
        state.areas_data = []
        for area in self.world.areas:
            area_data = {
                'grid_x': area.grid_x,
                'grid_y': area.grid_y,
                'active': area.active,
                'enemies': [],
                'items': []
            }
            
            for enemy in area.enemies:
                enemy_data = {
                    'x': enemy.x,
                    'y': enemy.y,
                    'health': enemy.health,
                    'max_health': enemy.max_health
                }
                area_data['enemies'].append(enemy_data)
            
            for item in area.items:
                item_data = {
                    'x': item.x,
                    'y': item.y,
                    'item_type': item.item_type,
                    'symbol': item.symbol
                }
                area_data['items'].append(item_data)
            
            state.areas_data.append(area_data)
        
        state.game_config = self.config.copy()
        
        return state
    
    def restore_from_state(self, state: GameState):
        self.player.x = state.player_data['x']
        self.player.y = state.player_data['y']
        self.player.health = state.player_data['health']
        self.player.max_health = state.player_data['max_health']
        self.player.health_items = state.player_data['health_items']
        self.player.ammo_items = state.player_data['ammo_items']
        
        for i, area_data in enumerate(state.areas_data):
            if i < len(self.world.areas):
                area = self.world.areas[i]
                area.active = area_data['active']
                
                area.enemies.clear()
                for enemy_data in area_data['enemies']:
                    enemy = Enemy(enemy_data['x'], enemy_data['y'], self.config['enemy'])
                    enemy.health = enemy_data['health']
                    enemy.max_health = enemy_data['max_health']
                    area.enemies.append(enemy)
                
                area.items.clear()
                for item_data in area_data['items']:
                    item_config = self.config['items'][item_data['item_type']]
                    item = Item(item_data['x'], item_data['y'], item_data['item_type'], item_config)
                    item.symbol = item_data['symbol']
                    area.items.append(item)
        
        self.world.active_areas = [area for area in self.world.areas if area.active]

def create_preset_scenario(scenario_name: str) -> Dict:
    presets = {
        'tutorial': {
            'world': {'area_size': 300, 'activation_distance': 40, 'max_active_areas': 2},
            'spawn': {'enemies_per_area': 2, 'health_items_per_area': 3, 'ammo_items_per_area': 2},
            'enemy': {'speed': 60, 'damage': 5, 'health': 30},
            'player': {'speed': 150, 'max_health': 120},
            'game': {'survival_time': 30}
        },
        'survival': {
            'world': {'area_size': 500, 'activation_distance': 80, 'max_active_areas': 4},
            'spawn': {'enemies_per_area': 8, 'health_items_per_area': 1, 'ammo_items_per_area': 1},
            'enemy': {'speed': 120, 'damage': 15, 'health': 60},
            'player': {'speed': 200, 'max_health': 100},
            'game': {'survival_time': 90}
        },
        'nightmare': {
            'world': {'area_size': 600, 'activation_distance': 120, 'max_active_areas': 6},
            'spawn': {'enemies_per_area': 25, 'health_items_per_area': 1, 'ammo_items_per_area': 1},
            'enemy': {'speed': 150, 'damage': 25, 'health': 40},
            'player': {'speed': 250, 'max_health': 80},
            'items': {'ammo': {'damage': 50, 'radius': 150}},
            'game': {'survival_time': 120}
        },
        'arena': {
            'world': {'area_size': 200, 'activation_distance': 30, 'max_active_areas': 1},
            'spawn': {'enemies_per_area': 15, 'health_items_per_area': 5, 'ammo_items_per_area': 5},
            'enemy': {'speed': 100, 'damage': 20, 'health': 50},
            'player': {'speed': 180, 'max_health': 150},
            'game': {'survival_time': 45}
        },
        'performance': {
            'world': {'area_size': 1000, 'activation_distance': 200, 'max_active_areas': 9},
            'spawn': {'enemies_per_area': 200, 'health_items_per_area': 5, 'ammo_items_per_area': 5},
            'enemy': {'speed': 80, 'damage': 5, 'health': 20},
            'player': {'speed': 400, 'max_health': 200},
            'items': {'ammo': {'damage': 100, 'radius': 200}},
            'game': {'survival_time': 30, 'fps': 30}
        }
    }
    
    return presets.get(scenario_name, {})

def generate_random_scenario() -> Dict:
    import random
    
    return {
        'world': {
            'area_size': random.choice([300, 400, 500, 600]),
            'activation_distance': random.randint(40, 120),
            'max_active_areas': random.randint(2, 6)
        },
        'spawn': {
            'enemies_per_area': random.randint(3, 20),
            'health_items_per_area': random.randint(1, 4),
            'ammo_items_per_area': random.randint(1, 3)
        },
        'enemy': {
            'speed': random.randint(80, 180),
            'damage': random.randint(8, 30),
            'health': random.randint(30, 80)
        },
        'player': {
            'speed': random.randint(150, 250),
            'max_health': random.randint(80, 150)
        },
        'game': {
            'survival_time': random.randint(30, 180)
        }
    }