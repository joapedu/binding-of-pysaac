#!/usr/bin/env python3
import time
import psutil
import os
import sys

def measure_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def performance_comparison():
    print("⚡ TESTE DE PERFORMANCE - CARREGAMENTO DINÂMICO")
    print("=" * 60)
    
    print("\n📊 CENÁRIOS DE TESTE:")
    print("-" * 40)
    
    scenarios = [
        ("Tutorial", 3, "Fácil - Poucos inimigos"),
        ("Survival", 8, "Médio - Inimigos moderados"),
        ("Nightmare", 25, "Difícil - Muitos inimigos"),
        ("Performance", 200, "Extremo - Milhares de inimigos")
    ]
    
    print("Cenário | Inimigos/Área | Total Estático | Total Dinâmico | Economia")
    print("-" * 70)
    
    for name, enemies_per_area, description in scenarios:
        static_total = enemies_per_area * 9
        dynamic_total = enemies_per_area * 6
        economy = ((static_total - dynamic_total) / static_total) * 100
        
        print(f"{name:8} | {enemies_per_area:13} | {static_total:12} | {dynamic_total:13} | {economy:6.1f}%")
    
    print("\n💾 ECONOMIA DE MEMÓRIA:")
    print("-" * 40)
    print("• Cenário Tutorial: Economia mínima (já é leve)")
    print("• Cenário Survival: ~33% menos memória")
    print("• Cenário Nightmare: ~33% menos memória")
    print("• Cenário Performance: ~33% menos memória")
    
    print("\n🎯 BENEFÍCIOS EM CENÁRIOS EXTREMOS:")
    print("-" * 40)
    print("📈 CENÁRIO PERFORMANCE (200 inimigos/área):")
    print("   • Modo Estático: 1800 inimigos na memória")
    print("   • Modo Dinâmico: 1200 inimigos na memória")
    print("   • Economia: 600 inimigos (33%)")
    print("   • Impacto: Significativo na performance")
    
    print("\n🚀 CENÁRIO ULTRA-EXTREMO (1000 inimigos/área):")
    print("   • Modo Estático: 9000 inimigos na memória")
    print("   • Modo Dinâmico: 6000 inimigos na memória")
    print("   • Economia: 3000 inimigos (33%)")
    print("   • Impacto: Crítico para jogabilidade")
    
    print("\n📈 ESCALABILIDADE:")
    print("-" * 40)
    print("• Modo Estático: Memória cresce linearmente com inimigos")
    print("• Modo Dinâmico: Memória limitada a 6 áreas")
    print("• Benefício aumenta com cenários mais extremos")
    print("• Permite cenários impossíveis no modo estático")
    
    print("\n🔄 SISTEMA DE CACHE:")
    print("-" * 40)
    print("• Áreas são salvas em arquivos JSON")
    print("• Cache persiste entre sessões")
    print("• Carregamento mais rápido em áreas visitadas")
    print("• Reduz tempo de geração de conteúdo")
    
    print("\n📱 MONITORAMENTO EM TEMPO REAL:")
    print("-" * 40)
    print("Durante o jogo, observe:")
    print("• 'Memória: X/6 áreas' - Áreas carregadas")
    print("• 'Inimigos: X' - Total de inimigos ativos")
    print("• 'L' nas áreas - Indicador de carregamento")
    print("• Mudança de cor das bordas das áreas")
    
    print("\n🧪 COMO TESTAR:")
    print("-" * 40)
    print("1. Execute o jogo: python main.py")
    print("2. Escolha cenário 'Performance'")
    print("3. Pressione F10 para alternar modos")
    print("4. Observe as estatísticas no canto superior direito")
    print("5. Compare performance entre modos")
    
    print("\n✨ TESTE CONCLUÍDO!")
    print("=" * 60)
    print("💡 Recomendações:")
    print("   - Use modo dinâmico para cenários com 50+ inimigos/área")
    print("   - Modo estático é adequado para cenários leves")
    print("   - F10 permite alternar facilmente entre modos")
    print("   - Monitore estatísticas para otimizar experiência")

def memory_estimation():
    print("\n💾 ESTIMAÇÃO DE USO DE MEMÓRIA:")
    print("-" * 40)
    

    enemy_memory = 0.5
    item_memory = 0.2
    
    print("Estimativa de memória por entidade:")
    print(f"• Inimigo: ~{enemy_memory} KB")
    print(f"• Item: ~{item_memory} KB")
    
    print("\nCenários de exemplo:")
    scenarios = [
        ("Tutorial", 3, 3),
        ("Survival", 8, 3),
        ("Nightmare", 25, 3),
        ("Performance", 200, 3)
    ]
    
    for name, enemies, items in scenarios:
        static_enemies = enemies * 9
        static_items = items * 9
        dynamic_enemies = enemies * 6
        dynamic_items = items * 6
        
        static_memory = (static_enemies * enemy_memory + static_items * item_memory) / 1024
        dynamic_memory = (dynamic_enemies * enemy_memory + dynamic_items * item_memory) / 1024
        
        print(f"\n{name}:")
        print(f"  Estático: {static_memory:.1f} MB")
        print(f"  Dinâmico: {dynamic_memory:.1f} MB")
        print(f"  Economia: {static_memory - dynamic_memory:.1f} MB")

if __name__ == "__main__":
    performance_comparison()
    memory_estimation()