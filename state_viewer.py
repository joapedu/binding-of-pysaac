#!/usr/bin/env python3
import json
import yaml
import os
import sys
from game_state import GameState, create_preset_scenario, generate_random_scenario

def print_state_info(state: GameState):
    print("=" * 50)
    print("📊 INFORMAÇÕES DO ESTADO DO JOGO")
    print("=" * 50)
    
    print(f"⏰ Timestamp: {state.metadata.get('timestamp', 'N/A')}")
    print(f"🎯 Áreas ativas: {state.metadata.get('active_areas_count', 'N/A')}")
    print(f"👾 Total de inimigos: {state.metadata.get('total_enemies', 'N/A')}")
    print(f"📦 Total de itens: {state.metadata.get('total_items', 'N/A')}")
    
    print("\n👤 JOGADOR:")
    print(f"   Posição: ({state.player_data.get('x', 0):.1f}, {state.player_data.get('y', 0):.1f})")
    print(f"   Saúde: {state.player_data.get('health', 0)}/{state.player_data.get('max_health', 0)}")
    print(f"   Itens de saúde: {state.player_data.get('health_items', 0)}")
    print(f"   Itens de munição: {state.player_data.get('ammo_items', 0)}")
    
    print("\n🗺️  ÁREAS:")
    for i, area in enumerate(state.areas_data):
        status = "✅ ATIVA" if area.get('active', False) else "❌ INATIVA"
        print(f"   Área {i+1} ({area.get('grid_x', 0)},{area.get('grid_y', 0)}): {status}")
        print(f"      Inimigos: {len(area.get('enemies', []))}")
        print(f"      Itens: {len(area.get('items', []))}")
        
        enemies = area.get('enemies', [])
        if enemies:
            print("      👾 Inimigos:")
            for j, enemy in enumerate(enemies[:3]):
                print(f"         {j+1}. Pos: ({enemy.get('x', 0):.1f}, {enemy.get('y', 0):.1f}) Saúde: {enemy.get('health', 0)}")
            if len(enemies) > 3:
                print(f"         ... e mais {len(enemies) - 3} inimigos")
        
        items = area.get('items', [])
        if items:
            print("      📦 Itens:")
            for j, item in enumerate(items[:3]):
                print(f"         {j+1}. {item.get('symbol', '?')} Pos: ({item.get('x', 0):.1f}, {item.get('y', 0):.1f})")
            if len(items) > 3:
                print(f"         ... e mais {len(items) - 3} itens")

def list_saved_states():
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'state' in f]
    yaml_files = [f for f in os.listdir('.') if f.endswith('.yaml') and 'state' in f]
    
    print("💾 ESTADOS SALVOS:")
    print("=" * 30)
    
    if not json_files and not yaml_files:
        print("   Nenhum estado salvo encontrado.")
        return []
    
    all_files = []
    for file in json_files + yaml_files:
        try:
            state = GameState()
            if file.endswith('.json'):
                state.load_from_json(file)
            else:
                state.load_from_yaml(file)
            
            timestamp = state.metadata.get('timestamp', 0)
            enemies = state.metadata.get('total_enemies', 0)
            areas = state.metadata.get('active_areas_count', 0)
            
            print(f"   📄 {file}")
            print(f"      ⏰ {timestamp:.1f}s | 👾 {enemies} inimigos | 🎯 {areas} áreas ativas")
            all_files.append(file)
        except Exception as e:
            print(f"   ❌ {file} (erro: {e})")
    
    return all_files

def create_scenario_file(scenario_name: str, filename: str):
    if scenario_name == 'random':
        config = generate_random_scenario()
        print(f"🎲 Gerando cenário aleatório...")
    else:
        config = create_preset_scenario(scenario_name)
        if not config:
            print(f"❌ Cenário '{scenario_name}' não encontrado.")
            print("   Cenários disponíveis: tutorial, survival, nightmare, arena, random")
            return False
        print(f"📋 Usando cenário pré-definido: {scenario_name}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print(f"✅ Cenário salvo em: {filename}")
    return True

def main():
    if len(sys.argv) < 2:
        print("🎮 Visualizador de Estados do Jogo")
        print("=" * 40)
        print("Uso:")
        print("  python state_viewer.py list                    # Listar estados salvos")
        print("  python state_viewer.py view <arquivo>          # Visualizar estado")
        print("  python state_viewer.py create <cenario> <arquivo>  # Criar cenário")
        print("")
        print("Cenários disponíveis:")
        print("  tutorial  - Cenário fácil para aprendizado")
        print("  survival  - Modo sobrevivência padrão")
        print("  nightmare - Cenário extremamente difícil")
        print("  arena     - Combate em área pequena")
        print("  random    - Cenário gerado aleatoriamente")
        return
    
    command = sys.argv[1]
    
    if command == 'list':
        list_saved_states()
    
    elif command == 'view':
        if len(sys.argv) < 3:
            print("❌ Especifique o arquivo para visualizar")
            return
        
        filename = sys.argv[2]
        if not os.path.exists(filename):
            print(f"❌ Arquivo '{filename}' não encontrado")
            return
        
        try:
            state = GameState()
            if filename.endswith('.json'):
                state.load_from_json(filename)
            elif filename.endswith('.yaml') or filename.endswith('.yml'):
                state.load_from_yaml(filename)
            else:
                print("❌ Formato de arquivo não suportado. Use .json ou .yaml")
                return
            
            print_state_info(state)
        except Exception as e:
            print(f"❌ Erro ao carregar arquivo: {e}")
    
    elif command == 'create':
        if len(sys.argv) < 4:
            print("❌ Especifique o cenário e nome do arquivo")
            print("   Exemplo: python state_viewer.py create tutorial cenario_tutorial.yaml")
            return
        
        scenario_name = sys.argv[2]
        filename = sys.argv[3]
        
        if not filename.endswith(('.yaml', '.yml')):
            filename += '.yaml'
        
        create_scenario_file(scenario_name, filename)
    
    else:
        print(f"❌ Comando '{command}' não reconhecido")
        print("   Comandos disponíveis: list, view, create")

if __name__ == "__main__":
    main()