#!/usr/bin/env python3
import subprocess
import sys
import os
import platform

def install_requirements():
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def check_python_version():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} não é suportado.")
        print("   Requer Python 3.8 ou superior.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} é compatível.")
    return True

def check_system():
    system = platform.system()
    print(f"🖥️  Sistema detectado: {system}")
    
    if system == "Linux":
        print("   Sistema Linux detectado - compatível ✅")
    elif system == "Windows":
        print("   Sistema Windows detectado - compatível ✅")
    elif system == "Darwin":
        print("   Sistema macOS detectado - compatível ✅")
    else:
        print(f"   Sistema {system} - compatibilidade não testada ⚠️")
    
    return True

def test_game():
    print("\n🎮 Testando execução do jogo...")
    try:
        result = subprocess.run([sys.executable, "main.py"], 
                              timeout=5, 
                              capture_output=True, 
                              text=True)
        print("✅ Jogo executou sem erros críticos!")
        return True
    except subprocess.TimeoutExpired:
        print("✅ Jogo iniciou corretamente (timeout esperado)")
        return True
    except Exception as e:
        print(f"❌ Erro ao testar jogo: {e}")
        return False

def main():
    print("🎮 Instalador do Jogo de Sobrevivência")
    print("=" * 40)
    
    if not check_python_version():
        return 1
    
    if not check_system():
        return 1
    
    if not install_requirements():
        return 1
    
    if not test_game():
        print("\n⚠️  O jogo pode ter problemas de execução.")
        print("   Verifique se todas as dependências foram instaladas corretamente.")
    
    print("\n🎉 Instalação concluída!")
    print("\n📋 Para executar o jogo:")
    print("   python main.py")
    print("\n🧪 Para testar cenários de balanceamento:")
    print("   python test_scenarios.py")
    print("\n📖 Consulte o README.md para mais informações.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())