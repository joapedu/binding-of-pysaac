import pygame
import sys
import os
import yaml
import math
from entities import Player
from world import World
from camera import Camera
from game_state import GameStateManager, create_preset_scenario, generate_random_scenario
from pause_menu import PauseMenu

class Game:
    def __init__(self, config_path: str = 'config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.window_width = self.config['game']['window_width']
        self.window_height = self.config['game']['window_height']
        self.fps = self.config['game']['fps']
        self.survival_time = self.config['game']['survival_time']
        
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Jogo de Sobrevivência")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.world = World(config_path)
        self.camera = Camera(self.window_width, self.window_height)
        
        area_size = self.config['world']['area_size']
        center_x = area_size + area_size // 2
        center_y = area_size + area_size // 2
        self.player = Player(center_x, center_y, self.config['player'])
        
        self.state_manager = GameStateManager(self.world, self.player, self.config)
        self.pause_menu = PauseMenu(self.window_width, self.window_height)
        
        self.game_start_time = 0
        self.game_running = True
        self.game_over = False
        self.victory = False
        self.paused = False
        
        self.keys_pressed = set()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                
                if event.key == pygame.K_ESCAPE:
                    if not self.game_over:
                        self.pause_menu.toggle()
                        self.paused = self.pause_menu.visible
                elif event.key == pygame.K_h and not self.paused:
                    self.player.use_health_item()
                elif event.key == pygame.K_j and not self.paused:
                    killed_enemies = self.player.use_ammo_item(
                        self.world.enemies,
                        self.config['items']['ammo']['damage'],
                        self.config['items']['ammo']['radius']
                    )
                    for enemy in killed_enemies:
                        for area in self.world.areas:
                            if enemy in area.enemies:
                                area.enemies.remove(enemy)
                                break
                elif event.key == pygame.K_F5 and not self.paused:
                    self.save_state()
                elif event.key == pygame.K_F9 and not self.paused:
                    self.load_state()
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            
            if self.pause_menu.visible:
                action = self.pause_menu.handle_event(event)
                if action == "resume":
                    self.paused = False
                elif action == "restart":
                    self.restart()
                elif action == "main_menu":
                    self.game_running = False
                    return "main_menu"
                elif action == "quit":
                    self.game_running = False
                    return "quit"
    
    
    def update(self, dt: float):
        if self.game_over or self.paused:
            return
        
        if self.game_start_time == 0:
            self.game_start_time = pygame.time.get_ticks() / 1000.0
        
        current_time = pygame.time.get_ticks() / 1000.0
        elapsed_time = current_time - self.game_start_time
        
        if elapsed_time >= self.survival_time:
            self.victory = True
            self.game_over = True
            return
        
        dx = dy = 0
        if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
            dx = -1
        if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
            dx = 1
        if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
            dy = -1
        if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
            dy = 1
        
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
        
        self.player.move(dx, dy, dt)
        
        if self.player.health <= 0:
            self.game_over = True
            return
        
        self.world.update(self.player, dt)
        self.camera.follow(self.player.x, self.player.y)
        self.camera.update(dt)
    
    def draw(self):
        self.screen.fill((20, 20, 20))
        
        camera_x, camera_y = self.camera.get_position()
        
        self.world.draw_grid(self.screen, camera_x, camera_y)
        self.world.draw(self.screen, camera_x, camera_y)
        self.player.draw(self.screen, camera_x, camera_y)
        
        self.draw_ui()
        
        self.pause_menu.draw(self.screen)
        
        pygame.display.flip()
    
    def draw_ui(self):
        health_text = self.font.render(f"Vida: {self.player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))
        
        active_enemies = len(self.world.enemies)
        enemies_text = self.small_font.render(f"Inimigos: {active_enemies}", True, (255, 255, 255))
        self.screen.blit(enemies_text, (10, 50))
        
        health_items_text = self.small_font.render(f"➕: {self.player.health_items}", True, (255, 255, 255))
        self.screen.blit(health_items_text, (10, 75))
        
        ammo_items_text = self.small_font.render(f"⚡: {self.player.ammo_items}", True, (255, 255, 255))
        self.screen.blit(ammo_items_text, (10, 100))
        
        current_time = pygame.time.get_ticks() / 1000.0
        elapsed_time = current_time - self.game_start_time
        remaining_time = max(0, self.survival_time - elapsed_time)
        
        time_text = self.font.render(f"Tempo: {remaining_time:.1f}s", True, (255, 255, 255))
        self.screen.blit(time_text, (self.window_width - 200, 10))
        
        active_areas_text = self.small_font.render(f"Áreas Ativas: {len(self.world.active_areas)}", True, (255, 255, 255))
        self.screen.blit(active_areas_text, (self.window_width - 200, 50))
        
        if self.paused:
            controls_text = self.small_font.render("ESC: Continuar | PAUSADO", True, (255, 255, 0))
        else:
            controls_text = self.small_font.render("WASD: Mover | H: ➕ | J: ⚡ | F5: Salvar | F9: Carregar | ESC: Pausar", True, (200, 200, 200))
        self.screen.blit(controls_text, (10, self.window_height - 30))
        
        if self.game_over:
            if self.victory:
                result_text = self.font.render("VITÓRIA!", True, (0, 255, 0))
            else:
                result_text = self.font.render("GAME OVER", True, (255, 0, 0))
            
            text_rect = result_text.get_rect(center=(self.window_width//2, self.window_height//2))
            self.screen.blit(result_text, text_rect)
            
            restart_text = self.small_font.render("Pressione R para reiniciar", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(self.window_width//2, self.window_height//2 + 50))
            self.screen.blit(restart_text, restart_rect)
    
    def save_state(self):
        try:
            state = self.state_manager.capture_current_state()
            filename = f"game_state_{int(pygame.time.get_ticks() / 1000)}.json"
            state.save_to_json(filename)
            print(f"✅ Estado salvo em: {filename}")
        except Exception as e:
            print(f"❌ Erro ao salvar estado: {e}")
    
    def load_state(self):
        try:
            import glob
            state_files = glob.glob("game_state_*.json")
            if not state_files:
                print("❌ Nenhum estado salvo encontrado")
                return
            
            latest_file = max(state_files, key=os.path.getctime)
            state = self.state_manager.capture_current_state()
            state.load_from_json(latest_file)
            self.state_manager.restore_from_state(state)
            print(f"✅ Estado carregado de: {latest_file}")
        except Exception as e:
            print(f"❌ Erro ao carregar estado: {e}")
    
    
    def restart(self):
        self.world = World()
        area_size = self.config['world']['area_size']
        center_x = area_size + area_size // 2
        center_y = area_size + area_size // 2
        self.player = Player(center_x, center_y, self.config['player'])
        self.state_manager = GameStateManager(self.world, self.player, self.config)
        self.pause_menu = PauseMenu(self.window_width, self.window_height)
        self.game_start_time = 0
        self.game_over = False
        self.victory = False
        self.paused = False
    
    def run(self):
        while self.game_running:
            dt = self.clock.tick(self.fps) / 1000.0
            
            action = self.handle_events()
            if action == "main_menu":
                return "main_menu"
            elif action == "quit":
                return "quit"
            
            if pygame.K_r in self.keys_pressed and self.game_over:
                self.restart()
            
            self.update(dt)
            self.draw()
        
        pygame.quit()
        return "quit"