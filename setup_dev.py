#!/usr/bin/env python3
"""
Script de configuração para desenvolvimento.
Instala dependências e configura o ambiente de desenvolvimento.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Executa um comando e exibe o resultado."""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        return False

def main():
    print("🛠️  CONFIGURAÇÃO DO AMBIENTE DE DESENVOLVIMENTO")
    print("=" * 60)

    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Python {python_version.major}.{python_version.minor} não é suportado.")
        print("   Requer Python 3.8 ou superior.")
        return 1
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if not os.path.exists("venv"):
        print("\n📦 Criando ambiente virtual...")
        if not run_command(f"{sys.executable} -m venv venv", "Criando venv"):
            return 1
    
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    print(f"\n💡 Para ativar o ambiente virtual, execute:")
    print(f"   {activate_cmd}")
    
    print("\n📚 Instalando dependências...")
    
    run_command(f"{pip_cmd} install --upgrade pip", "Atualizando pip")
    
    run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependências do projeto")
    
    dev_deps = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "flake8>=6.0.0",
        "black>=23.0.0",
        "isort>=5.12.0",
        "safety>=2.3.0",
        "bandit>=1.7.0",
        "psutil>=5.9.0"
    ]
    
    for dep in dev_deps:
        run_command(f"{pip_cmd} install {dep}", f"Instalando {dep}")
    
    if platform.system() == "Linux":
        print("\n🔧 Instalando dependências do sistema...")
        system_deps = [
            "sudo apt-get update",
            "sudo apt-get install -y python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev"
        ]
        
        for dep in system_deps:
            run_command(dep, f"Executando: {dep}")
    
    print("\n🧪 Executando testes básicos...")
    run_command(f"{python_cmd} -c \"import pygame; pygame.init(); pygame.quit()\"", "Testando pygame")
    run_command(f"{python_cmd} -c \"import yaml; print('YAML OK')\"", "Testando YAML")
    run_command(f"{python_cmd} -c \"import numpy; print('NumPy OK')\"", "Testando NumPy")
    
    print("\n🔍 Executando verificação de código...")
    run_command(f"{python_cmd} -m flake8 . --count --select=E9,F63,F7,F82", "Verificando erros críticos")
    
    print("\n🧪 Executando testes...")
    run_command(f"{python_cmd} -m pytest tests/ -v", "Executando testes unitários")
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("\n📋 Próximos passos:")
    print(f"1. Ative o ambiente virtual: {activate_cmd}")
    print("2. Execute o jogo: python main.py")
    print("3. Execute testes: python run_tests.py")
    print("4. Execute linting: flake8 .")
    print("5. Formate código: black .")
    
    print("\n🎮 Comandos úteis:")
    print("   python main.py                    # Executar jogo")
    print("   python run_tests.py --type all    # Executar todos os testes")
    print("   python run_tests.py --type quick  # Teste rápido")
    print("   python run_tests.py --type lint   # Verificar código")
    print("   black .                           # Formatar código")
    print("   isort .                           # Organizar imports")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())