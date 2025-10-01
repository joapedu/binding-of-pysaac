#!/usr/bin/env python3
"""
Script para executar testes localmente.
Facilita a execução de diferentes tipos de testes.
"""

import sys
import os
import subprocess
import argparse

def run_command(command, description):
    """Executa um comando e exibe o resultado."""
    print(f"\n🔧 {description}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Executar testes do Jogo de Sobrevivência")
    parser.add_argument("--type", choices=["all", "unit", "integration", "quick", "lint", "format"], 
                       default="quick", help="Tipo de teste a executar")
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo verboso")
    parser.add_argument("--coverage", "-c", action="store_true", help="Incluir relatório de cobertura")
    
    args = parser.parse_args()
    
    print("🎮 JOGO DE SOBREVIVÊNCIA - EXECUTOR DE TESTES")
    print("=" * 60)
    
    if not os.path.exists("main.py"):
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    success = True
    
    if args.type in ["all", "unit", "quick"]:
        cmd = "python -m pytest tests/ -v"
        if args.coverage:
            cmd += " --cov=. --cov-report=html --cov-report=term-missing"
        if not args.verbose:
            cmd += " --tb=short"
        
        success &= run_command(cmd, "Executando testes unitários")
    
    if args.type in ["all", "integration", "quick"]:
        success &= run_command("python tests/test_game_integration.py", "Executando teste de integração")
    
    if args.type in ["all", "lint"]:
        success &= run_command("flake8 .", "Verificando código com flake8")
        success &= run_command("python -c \"import yaml; yaml.safe_load(open('config.yaml'))\"", "Verificando config.yaml")
    
    if args.type in ["all", "format"]:
        success &= run_command("black --check .", "Verificando formatação com black")
        success &= run_command("isort --check-only .", "Verificando organização de imports")
    
    if args.type == "quick":
        success &= run_command("python -c \"import pygame; pygame.init(); pygame.quit()\"", "Testando pygame")
        
        success &= run_command("python -c \"import entities, world, camera, game_state, menu\"", "Testando importações")
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Todos os testes executados com sucesso!")
        sys.exit(0)
    else:
        print("❌ Alguns testes falharam!")
        sys.exit(1)

if __name__ == "__main__":
    main()