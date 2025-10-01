#!/usr/bin/env python3
"""
Teste de integração simples para o jogo de sobrevivência.
Verifica se o jogo pode ser inicializado e executado sem erros críticos.
"""

import sys
import os
import unittest
import pygame
import time
import threading
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities import Player, Enemy, Item
from world import World
from dynamic_world import DynamicAreaManager
from camera import Camera

class TestGameIntegration(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        pygame.init()
        self.config = {
            'game': {
                'window_width': 800,
                'window_height': 600,
                'fps': 60,
                'survival_time': 10
            },
            'player': {
                'size': 20,
                'speed': 200,
                'max_health': 100,
                'color': [0, 255, 0]
            },
            'enemy': {
                'size': 15,
                'speed': 100,
                'health': 50,
                'damage': 10,
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
                'area_size': 400,
                'activation_distance': 50,
                'max_active_areas': 4
            },
            'spawn': {
                'enemies_per_area': 2,
                'health_items_per_area': 1,
                'ammo_items_per_area': 1
            }
        }
    
    def tearDown(self):
        """Limpeza após cada teste."""
        pygame.quit()
    
    def test_player_creation(self):
        """Testa criação do jogador."""
        player = Player(100, 100, self.config['player'])
        
        self.assertEqual(player.x, 100)
        self.assertEqual(player.y, 100)
        self.assertEqual(player.health, 100)
        self.assertEqual(player.max_health, 100)
        self.assertTrue(player.alive)
    
    def test_player_movement(self):
        """Testa movimento do jogador."""
        player = Player(100, 100, self.config['player'])
        initial_x = player.x
        
        player.move(1, 0, 1.0)
        
        self.assertGreater(player.x, initial_x)
        self.assertEqual(player.y, 100)
    
    def test_enemy_creation(self):
        """Testa criação de inimigo."""
        enemy = Enemy(200, 200, self.config['enemies'])
        
        self.assertEqual(enemy.x, 200)
        self.assertEqual(enemy.y, 200)
        self.assertEqual(enemy.health, 50)
        self.assertTrue(enemy.alive)
    
    def test_item_creation(self):
        """Testa criação de itens."""
        health_item = Item(300, 300, 'health', self.config['items']['health'])
        ammo_item = Item(400, 400, 'ammo', self.config['items']['ammo'])
        
        self.assertEqual(health_item.item_type, 'health')
        self.assertEqual(ammo_item.item_type, 'ammo')
        self.assertEqual(health_item.symbol, '➕')
        self.assertEqual(ammo_item.symbol, '⚡')
    
    def test_world_creation(self):
        """Testa criação do mundo."""
        world = World()
        
        self.assertEqual(len(world.areas), 9)
        self.assertEqual(len(world.active_areas), 0)
    
    def test_dynamic_world_creation(self):
        """Testa criação do mundo dinâmico."""
        dynamic_world = DynamicAreaManager(self.config)
        
        self.assertEqual(len(dynamic_world.areas_data), 9)
        self.assertEqual(len(dynamic_world.active_areas), 0)
        self.assertEqual(len(dynamic_world.loaded_areas), 0)
    
    def test_camera_creation(self):
        """Testa criação da câmera."""
        camera = Camera(800, 600)
        
        self.assertEqual(camera.window_width, 800)
        self.assertEqual(camera.window_height, 600)
        self.assertEqual(camera.x, 0)
        self.assertEqual(camera.y, 0)
    
    def test_camera_follow(self):
        """Testa sistema de câmera seguindo jogador."""
        camera = Camera(800, 600)
        player = Player(100, 100, self.config['player'])

        camera.follow(player.x, player.y)
        camera.update(1.0)

        self.assertNotEqual(camera.x, 0)
        self.assertNotEqual(camera.y, 0)
    
    def test_player_damage(self):
        """Testa sistema de dano do jogador."""
        player = Player(100, 100, self.config['player'])
        initial_health = player.health
        
        player.take_damage(20)
        
        self.assertEqual(player.health, initial_health - 20)
        self.assertTrue(player.alive)
    
    def test_player_death(self):
        """Testa morte do jogador."""
        player = Player(100, 100, self.config['player'])
        
        player.take_damage(150)
        
        self.assertEqual(player.health, 0)
        self.assertFalse(player.alive)
    
    def test_item_collection(self):
        """Testa coleta de itens."""
        player = Player(100, 100, self.config['player'])
        health_item = Item(105, 105, 'health', self.config['items']['health'])
        
        initial_health_items = player.health_items
        
        collected = health_item.collect(player)
        
        self.assertTrue(collected)
        self.assertEqual(player.health_items, initial_health_items + 1)
        self.assertFalse(health_item.alive)
    
    def test_enemy_pursuit(self):
        """Testa perseguição do inimigo ao jogador."""
        player = Player(100, 100, self.config['player'])
        enemy = Enemy(200, 200, self.config['enemies'])
        
        initial_distance = ((enemy.x - player.x)**2 + (enemy.y - player.y)**2)**0.5
        
        enemy.update(player, 1.0)
        
        final_distance = ((enemy.x - player.x)**2 + (enemy.y - player.y)**2)**0.5
        
        self.assertLess(final_distance, initial_distance)
    
    def test_game_initialization(self):
        """Testa inicialização completa do jogo."""
        try:
            from game import Game
            
            with patch('pygame.display.set_mode'):
                game = Game()
                
                self.assertIsNotNone(game.player)
                self.assertIsNotNone(game.world)
                self.assertIsNotNone(game.camera)
                self.assertTrue(game.game_running)
                self.assertFalse(game.game_over)
                
        except ImportError as e:
            self.fail(f"Falha ao importar Game: {e}")
    
    def test_dynamic_loading_stats(self):
        """Testa estatísticas do carregamento dinâmico."""
        dynamic_world = DynamicAreaManager(self.config)
        stats = dynamic_world.get_memory_stats()
        
        self.assertIn('loaded_areas', stats)
        self.assertIn('active_areas', stats)
        self.assertIn('total_areas', stats)
        self.assertIn('total_enemies', stats)
        self.assertIn('total_items', stats)
        self.assertIn('memory_usage', stats)
        
        self.assertEqual(stats['total_areas'], 9)
        self.assertEqual(stats['loaded_areas'], 0)
        self.assertEqual(stats['active_areas'], 0)

def run_quick_game_test():
    """Executa um teste rápido do jogo sem interface gráfica."""
    print("🎮 Executando teste rápido do jogo...")
    
    try:
        pygame.init()
        
        config = {
            'game': {'window_width': 400, 'window_height': 300, 'fps': 30, 'survival_time': 5},
            'player': {'size': 20, 'speed': 100, 'max_health': 50, 'color': [0, 255, 0]},
            'enemy': {'size': 15, 'speed': 50, 'health': 25, 'damage': 5, 'damage_interval': 1.0, 'color': [255, 0, 0]},
            'items': {
                'health': {'size': 10, 'heal_amount': 15, 'color': [255, 255, 0], 'symbol': "➕"},
                'ammo': {'size': 10, 'damage': 10, 'radius': 50, 'color': [0, 255, 255], 'symbol': "⚡"}
            },
            'world': {'grid_size': 2, 'area_size': 200, 'activation_distance': 30, 'max_active_areas': 2},
            'spawn': {'enemies_per_area': 1, 'health_items_per_area': 1, 'ammo_items_per_area': 1}
        }
        
        player = Player(100, 100, config['player'])
        world = World()
        camera = Camera(400, 300)
        for i in range(10):
            player.move(1, 0, 0.1)
            world.update(player, 0.1)
            camera.follow(player.x, player.y)
            camera.update(0.1)
            time.sleep(0.01)
        
        print("✅ Teste básico do jogo executado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do jogo: {e}")
        return False
    finally:
        pygame.quit()

if __name__ == '__main__':
    print("🧪 Executando testes de integração...")
    
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "="*50)
    run_quick_game_test()