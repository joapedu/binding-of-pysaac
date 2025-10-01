#!/usr/bin/env python3
"""
Teste final para verificar se todos os problemas de spawn foram corrigidos.
"""

import yaml
import math
from world import World
from entities import Player

def test_spawn_final():
    print("🔧 TESTE FINAL - SPAWN DE INIMIGOS")
    print("=" * 50)
    
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print(f"📋 Configuração atual:")
    print(f"   • Inimigos por área: {config['spawn']['enemies_per_area']}")
    print(f"   • Tamanho das áreas: {config['world']['area_size']}x{config['world']['area_size']}")
    print(f"   • Máximo de áreas ativas: {config['world']['max_active_areas']}")
    print(f"   • Distância de ativação: {config['world']['activation_distance']}")
    
    world = World()
    world.config = config
    world.area_size = config['world']['area_size']
    world.grid_size = config['world']['grid_size']
    world.activation_distance = config['world']['activation_distance']
    world.max_active_areas = config['world']['max_active_areas']
    
    world.areas = []
    world.active_areas = []
    world.generate_world()
    
    center_x = config['world']['area_size'] + config['world']['area_size'] // 2
    center_y = config['world']['area_size'] + config['world']['area_size'] // 2
    player = Player(center_x, center_y, config['player'])
    
    print(f"\n🌍 Mundo criado:")
    print(f"   • Total de áreas: {len(world.areas)}")
    print(f"   • Áreas ativas: {len(world.active_areas)}")
    print(f"   • Posição do jogador: ({center_x}, {center_y})")
    
    for area in world.areas:
        print(f"\n🎯 Área ({area.grid_x},{area.grid_y}):")
        print(f"   • Posição: ({area.x}, {area.y})")
        print(f"   • Tamanho: {area.area_size}x{area.area_size}")
        print(f"   • Ativa: {'✅ SIM' if area.active else '❌ NÃO'}")
        print(f"   • Inimigos: {len(area.enemies)}")
        print(f"   • Itens: {len(area.items)}")
        
        if area.enemies:
            inimigos_fora = 0
            inimigos_muito_proximos = 0
            
            for i, enemy in enumerate(area.enemies):
                if (area.x <= enemy.x <= area.x + area.area_size and
                    area.y <= enemy.y <= area.y + area.area_size):
                    print(f"   • Inimigo {i+1}: ✅ pos=({enemy.x:.1f}, {enemy.y:.1f})")
                else:
                    print(f"   • Inimigo {i+1}: ❌ FORA pos=({enemy.x:.1f}, {enemy.y:.1f})")
                    inimigos_fora += 1
                
                for j, other_enemy in enumerate(area.enemies):
                    if i != j:
                        distance = math.sqrt((enemy.x - other_enemy.x)**2 + (enemy.y - other_enemy.y)**2)
                        if distance < 30:
                            inimigos_muito_proximos += 1
            
            if inimigos_fora == 0:
                print(f"   ✅ Todos os inimigos estão dentro da área")
            else:
                print(f"   ❌ {inimigos_fora} inimigos estão FORA da área!")
            
            if inimigos_muito_proximos == 0:
                print(f"   ✅ Espaçamento adequado entre inimigos")
            else:
                print(f"   ⚠️ {inimigos_muito_proximos} pares de inimigos muito próximos")
    
    print(f"\n🧪 Teste de ativação de áreas:")
    world.update_active_areas(player)
    print(f"   • Áreas ativas após update: {len(world.active_areas)}")
    
    for area in world.active_areas:
        print(f"   • Área ({area.grid_x},{area.grid_y}): {len(area.enemies)} inimigos, {len(area.items)} itens")

def test_distribuicao_inimigos():
    print(f"\n📊 TESTE DE DISTRIBUIÇÃO DE INIMIGOS")
    print("=" * 40)
    
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    for teste in range(3):
        print(f"\n🧪 Teste {teste + 1}:")
        
        world = World()
        world.config = config
        world.area_size = config['world']['area_size']
        world.grid_size = config['world']['grid_size']
        world.activation_distance = config['world']['activation_distance']
        world.max_active_areas = config['world']['max_active_areas']
        
        world.areas = []
        world.active_areas = []
        world.generate_world()
        
        center_area = None
        for area in world.areas:
            if area.grid_x == 1 and area.grid_y == 1:
                center_area = area
                break
        
        if center_area:
            center_area.active = True
            center_area.generate_content_when_activated()
            
            print(f"   • Área central: {len(center_area.enemies)} inimigos")
            
            if len(center_area.enemies) == config['spawn']['enemies_per_area']:
                print(f"   ✅ Quantidade correta de inimigos")
            else:
                print(f"   ❌ Quantidade incorreta: esperado {config['spawn']['enemies_per_area']}, obtido {len(center_area.enemies)}")

def main():
    print("🔧 TESTE COMPLETO DE CORREÇÕES FINAIS")
    print("=" * 50)
    
    test_spawn_final()
    test_distribuicao_inimigos()
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print("1. Execute: python main.py")
    print("2. Verifique se os inimigos laranjas aparecem distribuídos")
    print("3. Mova-se para ativar outras áreas")
    print("4. Observe o spawn uniforme de inimigos")

if __name__ == "__main__":
    main()