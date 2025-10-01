# Binding of Pysaac

Uma versão em Python inspirada em The Binding of Isaac com sistema de áreas ativas.

## Características

- **Menu Principal**: Interface gráfica com opções de configuração
- **Malha 3x3**: Mundo dividido em 9 áreas
- **Áreas Ativas**: Máximo de 4 áreas ativas simultaneamente
- **Viewport Independente**: Câmera que segue o jogador
- **NPCs**: Inimigos que perseguem o jogador
- **Itens**: Caixas de primeiros socorros (➕) e munição (⚡)
- **Objetivo**: Sobreviver por um tempo determinado
- **Configuração Interativa**: Sliders para ajustar balanceamento
- **Cenários Pré-definidos**: 6 cenários de teste diferentes
- **Carregamento Dinâmico**: Sistema otimizado de memória para áreas

## Instalação

### Linux (Manjaro/Ubuntu/Debian)

```bash
# Instalar Python e pip (se não estiver instalado)
sudo pacman -S python python-pip

# Instalar dependências
pip install -r requirements.txt

# Executar o jogo
python main.py
```

### Windows

```bash
# Instalar Python (https://python.org)
# Instalar dependências
pip install -r requirements.txt

# Executar o jogo
python main.py
```

## Menu Principal

### Opções do Menu
- **🎮 COMEÇAR JOGO**: Inicia o jogo com configurações atuais
- **⚙️ CONFIGURAR BALANCEAMENTO**: Ajusta parâmetros com sliders interativos
- **📊 CENÁRIOS DE TESTE**: Carrega cenários pré-definidos
- **❌ SAIR**: Encerra o programa

### Configuração de Balanceamento
- **Inimigos**: Quantidade, velocidade, dano, saúde
- **Mundo**: Tamanho das áreas, distância de ativação, áreas ativas
- **Jogador**: Velocidade, saúde máxima
- **Tempo**: Duração da sobrevivência

### Cenários Disponíveis
- **📚 TUTORIAL**: Poucos inimigos, muitas curas
- **🏃 SOBREVIVÊNCIA**: Modo equilibrado padrão
- **😱 PESADELO**: Centenas de inimigos rápidos
- **⚔️ ARENA**: Combate intenso em área pequena
- **🎲 ALEATÓRIO**: Configuração gerada aleatoriamente
- **🧪 PERFORMANCE**: Teste com milhares de inimigos

## Controles do Jogo

- **WASD** ou **Setas**: Mover o jogador
- **H**: Usar item de saúde (➕)
- **J**: Usar item de munição (⚡)
- **ESC**: Pausar/Despausar jogo
- **F5**: Salvar estado do jogo
- **F9**: Carregar último estado salvo
- **F10**: Alternar carregamento dinâmico/estático
- **R**: Reiniciar (após game over)

## Configuração

Edite o arquivo `config.yaml` para ajustar:

- Tempo de sobrevivência
- Velocidade e saúde do jogador
- Quantidade de inimigos por área
- Distância de ativação das áreas
- Dano e velocidade dos inimigos

## Balanceamento

O jogo suporta diferentes cenários de teste:

- **Poucos inimigos**: `enemies_per_area: 2-5`
- **Muitos inimigos**: `enemies_per_area: 10-50`
- **Áreas pequenas**: `area_size: 200-300`
- **Áreas grandes**: `area_size: 500-800`
- **Ativação próxima**: `activation_distance: 30-50`
- **Ativação distante**: `activation_distance: 100-200`

## Carregamento Dinâmico de Áreas

### Sistema Otimizado de Memória
- **Carregamento Inteligente**: Apenas áreas próximas ao jogador são carregadas
- **Cache Persistente**: Áreas são salvas em arquivos JSON para reutilização
- **Limite de Memória**: Máximo de 6 áreas carregadas simultaneamente
- **Descarregamento Automático**: Áreas distantes são removidas da memória

### Benefícios
- **Redução de Memória**: Até 33% menos uso de RAM em cenários extremos
- **Performance Melhorada**: Suporte a milhares de inimigos
- **Cache Inteligente**: Carregamento mais rápido em sessões subsequentes
- **Escalabilidade**: Cenários com 1000+ inimigos por área

### Controles
- **F10**: Alternar entre modo dinâmico e estático
- **Indicadores Visuais**: 'L' marca áreas carregadas
- **Estatísticas**: Monitor de memória em tempo real

## Menu de Pausa

### Sistema de Pausa Inteligente
- **Ativação**: Pressione ESC durante o jogo
- **Overlay**: Fundo semi-transparente sobre o jogo
- **Menu Centralizado**: Caixa com opções principais
- **Estado Preservado**: Jogo mantém posição e progresso

### Opções Disponíveis
- **▶️ CONTINUAR**: Retorna ao jogo (ESC também funciona)
- **🔄 REINICIAR**: Reinicia o jogo do início
- **🏠 MENU PRINCIPAL**: Volta ao menu principal
- **❌ SAIR**: Fecha o jogo completamente

### Características
- **Visual**: Estilo consistente com menu principal
- **Responsivo**: Navegação com mouse
- **Instantâneo**: Aparece imediatamente
- **Não Invasivo**: Não afeta performance

## Melhorias Visuais

### Sistema de Sprites Avançado
- **Personagens**: Sprites detalhados com olhos e direção
- **Inimigos**: Visual ameaçador com barras de vida
- **Itens**: Ícones temáticos com efeitos visuais
- **Cenário**: Tiles realistas com texturas diferenciadas

### Efeitos Visuais
- **Partículas**: Sistema de explosões e dano
- **Animações**: Movimento suave e direção visual
- **Feedback**: Indicadores visuais de ações
- **Cores**: Paleta consistente e temática

### Características Técnicas
- **Renderização**: Desenho vetorial otimizado
- **Performance**: 60 FPS garantidos
- **Escalabilidade**: Sprites adaptáveis
- **Configuração**: Parâmetros visuais ajustáveis

## Gerenciamento de Estados

### Salvar/Carregar Estados
- **F5**: Salva o estado atual do jogo
- **F9**: Carrega o último estado salvo
- Estados são salvos em arquivos `game_state_*.json`

### Visualizar Estados Salvos
```bash
python state_viewer.py list                    # Listar estados salvos
python state_viewer.py view <arquivo>          # Visualizar estado
python state_viewer.py create <cenario> <arquivo>  # Criar cenário
```

### Cenários Pré-definidos
- **tutorial**: Cenário fácil para aprendizado
- **survival**: Modo sobrevivência padrão  
- **nightmare**: Cenário extremamente difícil
- **arena**: Combate em área pequena
- **random**: Cenário gerado aleatoriamente

## Desenvolvimento

### Configuração do Ambiente
```bash
# Configurar ambiente de desenvolvimento
python setup_dev.py

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Executar testes
python run_tests.py --type all

# Executar jogo
python main.py
```

### Testes
```bash
# Teste rápido
python run_tests.py --type quick

# Todos os testes
python run_tests.py --type all

# Apenas linting
python run_tests.py --type lint

# Com cobertura
python run_tests.py --coverage
```

### Qualidade de Código
```bash
# Formatar código
black .

# Organizar imports
isort .

# Verificar código
flake8 .

# Análise de segurança
bandit -r .
```

## Estrutura do Projeto

```
jogos-ia/
├── main.py                    # Ponto de entrada com menu principal
├── game.py                    # Classe principal do jogo
├── menu.py                    # Sistema de menu e interface
├── pause_menu.py              # Menu de pausa durante o jogo
├── sprites.py                 # Sistema de sprites e efeitos visuais
├── entities.py                # Player, Enemy, Item
├── world.py                   # Sistema de áreas e malha
├── dynamic_world.py           # Carregamento dinâmico otimizado
├── camera.py                  # Sistema de câmera/viewport
├── game_state.py              # Gerenciamento de estados
├── state_viewer.py            # Visualizador de estados
├── performance_test.py        # Análise de performance
├── run_tests.py               # Executor de testes local
├── setup_dev.py               # Configuração de desenvolvimento
├── config.yaml                # Configurações do jogo
├── exemplo_estado_inicial.yaml # Exemplo de estado inicial
├── requirements.txt           # Dependências Python
├── pytest.ini                # Configuração do pytest
├── .flake8                    # Configuração do flake8
├── pyproject.toml             # Configuração de ferramentas
├── tests/                     # Testes automatizados
│   ├── __init__.py
│   └── test_game_integration.py
├── .github/                   # Configuração do GitHub
│   ├── workflows/
│   │   └── ci.yml             # Workflow de CI/CD
│   └── ISSUE_TEMPLATE/        # Templates de issues
├── CONTRIBUTING.md            # Guia de contribuição
├── CHANGELOG.md               # Histórico de mudanças
├── LICENSE                    # Licença MIT
└── README.md                  # Este arquivo
```