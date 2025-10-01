# Guia de Contribuição

Obrigado por seu interesse em contribuir para o Jogo de Sobrevivência! Este documento fornece diretrizes para contribuições.

## 🚀 Como Contribuir

### 1. Fork e Clone
```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/jogos-ia.git
cd jogos-ia
```

### 2. Configurar Ambiente
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Executar Testes
```bash
# Executar testes básicos
python -m pytest tests/

# Executar teste de integração
python tests/test_game_integration.py
```

## 📝 Tipos de Contribuição

### 🐛 Correção de Bugs
- Use issues para reportar bugs
- Inclua passos para reproduzir
- Teste a correção antes de submeter

### ✨ Novas Funcionalidades
- Discuta grandes mudanças em issues primeiro
- Mantenha compatibilidade com código existente
- Adicione testes para novas funcionalidades

### 📚 Documentação
- Melhore README.md
- Adicione comentários no código
- Crie exemplos de uso

### 🎮 Balanceamento
- Teste diferentes configurações
- Documente mudanças de balanceamento
- Use cenários pré-definidos para testes

## 🔧 Padrões de Código

### Python
- Use PEP 8 para formatação
- Máximo 80 caracteres por linha
- Use type hints quando possível
- Documente funções complexas

### Estrutura de Arquivos
```
jogos-ia/
├── main.py              # Ponto de entrada
├── game.py              # Lógica principal
├── entities.py          # Entidades do jogo
├── world.py             # Sistema de mundo
├── dynamic_world.py     # Carregamento dinâmico
├── menu.py              # Interface de menu
├── camera.py            # Sistema de câmera
├── game_state.py        # Gerenciamento de estados
├── tests/               # Testes automatizados
├── docs/                # Documentação
└── examples/            # Exemplos de uso
```

### Convenções de Nomenclatura
- Classes: `PascalCase` (ex: `GameState`)
- Funções/Variáveis: `snake_case` (ex: `update_player`)
- Constantes: `UPPER_CASE` (ex: `MAX_AREAS`)
- Arquivos: `snake_case` (ex: `game_state.py`)

## 🧪 Testes

### Executar Testes
```bash
# Todos os testes
python -m pytest

# Testes específicos
python -m pytest tests/test_entities.py

# Com cobertura
python -m pytest --cov=.
```

### Escrever Testes
- Teste funcionalidades críticas
- Use fixtures para setup comum
- Teste casos extremos
- Mantenha testes simples e legíveis

### Exemplo de Teste
```python
def test_player_movement():
    player = Player(100, 100, config['player'])
    initial_x = player.x
    
    player.move(1, 0, 1.0)  # Move para direita
    
    assert player.x > initial_x
    assert player.y == 100
```

## 📋 Processo de Pull Request

### 1. Criar Branch
```bash
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b bugfix/corrigir-bug
```

### 2. Fazer Mudanças
- Faça commits pequenos e focados
- Use mensagens de commit descritivas
- Teste suas mudanças

### 3. Commit
```bash
git add .
git commit -m "feat: adiciona sistema de power-ups"
# ou
git commit -m "fix: corrige bug de colisão com inimigos"
```

### 4. Push e Pull Request
```bash
git push origin feature/nova-funcionalidade
# Criar PR no GitHub
```

## 🏷️ Convenções de Commit

Use o formato: `tipo(escopo): descrição`

### Tipos
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas de manutenção

### Exemplos
```
feat(menu): adiciona opção de configuração avançada
fix(entities): corrige bug de colisão com itens
docs(readme): atualiza instruções de instalação
test(game): adiciona testes para sistema de áreas
```

## 🎯 Áreas de Contribuição

### 🎮 Gameplay
- Novos tipos de inimigos
- Power-ups e itens especiais
- Mecânicas de combate
- Sistema de pontuação

### 🖥️ Interface
- Melhorias no menu
- Indicadores visuais
- Sistema de configuração
- Temas visuais

### ⚡ Performance
- Otimizações de memória
- Melhorias no carregamento dinâmico
- Otimização de renderização
- Sistema de cache

### 🧪 Testes
- Testes de integração
- Testes de performance
- Testes de balanceamento
- Testes de compatibilidade

## 📞 Comunicação

### Issues
- Use templates fornecidos
- Seja específico e detalhado
- Inclua screenshots quando relevante
- Use labels apropriadas

### Discussões
- Use GitHub Discussions para ideias
- Seja respeitoso e construtivo
- Ajude outros contribuidores
- Compartilhe conhecimento

## 🏆 Reconhecimento

Contribuidores serão reconhecidos em:
- README.md
- CHANGELOG.md
- Releases do GitHub
- Documentação do projeto

## 📜 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.

## ❓ Dúvidas?

- Abra uma issue para perguntas
- Use GitHub Discussions para discussões
- Consulte a documentação existente
- Entre em contato com os mantenedores

---

**Obrigado por contribuir! 🎉**