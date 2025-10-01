#!/usr/bin/env python3
import pygame
import sys
import os
import yaml
from game import Game
from menu import MainMenu
from game_state import create_preset_scenario, generate_random_scenario

def main():
    pygame.init()
    
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Binding of Pysaac - Menu Principal")
    
    clock = pygame.time.Clock()
    menu = MainMenu(screen_width, screen_height)
    game = None
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            action = menu.handle_event(event)
            
            if action == "start_game":
                try:
                    game = Game()
                    result = game.run()
                    if result == "main_menu":
                        continue
                    elif result == "quit":
                        running = False
                except Exception as e:
                    print(f"Erro ao executar o jogo: {e}")
            
            elif action == "save_config":
                save_custom_config(menu.get_config_values())
                print("✅ Configuração personalizada salva!")
            
            elif action.startswith("load_scenario_"):
                scenario_name = action.replace("load_scenario_", "")
                load_scenario(scenario_name)
                print(f"✅ Cenário '{scenario_name}' carregado!")
            
            elif action == "quit":
                running = False
        
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    return 0

def save_custom_config(config_values):
    custom_config = {
        'game': {
            'window_width': 1200,
            'window_height': 800,
            'fps': 60,
            'survival_time': config_values['survival_time']
        },
        'player': {
            'size': 20,
            'speed': config_values['player_speed'],
            'max_health': config_values['player_max_health'],
            'color': [0, 255, 0]
        },
        'enemy': {
            'size': 15,
            'speed': config_values['enemy_speed'],
            'health': config_values['enemy_health'],
            'damage': config_values['enemy_damage'],
            'damage_interval': 1.0,
            'color': [255, 0, 0]
        },
        'items': {
            'health': {
                'size': 10,
                'heal_amount': 30,
                'color': [255, 255, 0],
                'symbol': "➕"
            },
            'ammo': {
                'size': 10,
                'damage': 25,
                'radius': 100,
                'color': [0, 255, 255],
                'symbol': "⚡"
            }
        },
        'world': {
            'grid_size': 3,
            'area_size': config_values['area_size'],
            'activation_distance': config_values['activation_distance'],
            'max_active_areas': config_values['max_active_areas']
        },
        'spawn': {
            'enemies_per_area': config_values['enemies_per_area'],
            'health_items_per_area': 2,
            'ammo_items_per_area': 1
        }
    }
    
    with open('config_custom.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(custom_config, f, default_flow_style=False, allow_unicode=True)

def load_scenario(scenario_name):
    if scenario_name == 'random':
        config = generate_random_scenario()
    else:
        config = create_preset_scenario(scenario_name)
    
    if not config:
        print(f"❌ Cenário '{scenario_name}' não encontrado")
        return
    
    with open('config.yaml', 'r', encoding='utf-8') as f:
        base_config = yaml.safe_load(f)
    
    def deep_update(base_dict, update_dict):
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    deep_update(base_config, config)
    
    scenario_file = f'config_{scenario_name}.yaml'
    with open(scenario_file, 'w', encoding='utf-8') as f:
        yaml.dump(base_config, f, default_flow_style=False, allow_unicode=True)
    
    with open('config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(base_config, f, default_flow_style=False, allow_unicode=True)

if __name__ == "__main__":
    sys.exit(main())