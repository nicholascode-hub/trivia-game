# 🎵 Trivia Game - K-pop vs Programação 🧪

Um jogo de trivia interativo desenvolvido em Python que desafia seus conhecimentos em duas categorias distintas: K-pop e Programação!

## 📋 Descrição

Este é um jogo de perguntas e respostas com interface gráfica moderna que combina entretenimento com aprendizado. O jogo apresenta um banco de dados próprio de perguntas detalhadas sobre grupos de K-pop (EXO, BLACKPINK, TWICE) e conceitos fundamentais de programação Python. Com sistema de vidas, pontuação e escolha dinâmica de tópicos, proporciona uma experiência educativa e divertida.

## 🚀 Funcionalidades

- 🎯 Perguntas de múltipla escolha especializadas
- 🎵 Categoria K-pop: EXO, BLACKPINK, TWICE e K-pop geral
- 💻 Categoria Programação: Python, conceitos básicos e lógica
- 💖 Sistema de vidas (3 corações visuais)
- 🏆 Sistema de pontuação (10 pontos por acerto)
- 🔄 Embaralhamento automático das perguntas
- ✨ Interface moderna com tema dark (ttkbootstrap)
- 🖥️ Suporte a tela cheia (F11/ESC)
- 📊 Feedback imediato e escolha de próximo tópico

## 🛠️ Dependências

Para executar este projeto, você precisa ter as seguintes dependências instaladas:

### Bibliotecas Python Necessárias:
- `tkinter` - Interface gráfica básica (geralmente já incluída no Python)
- `ttkbootstrap` - Interface moderna com temas Bootstrap
- `random` - Embaralhamento de perguntas (biblioteca padrão)

### Instalação das dependências:
```bash
pip install ttkbootstrap
```

> **Nota sobre tkinter:** Já vem instalado com o Python na maioria dos sistemas. Caso não tenha:
> - Ubuntu/Debian: `sudo apt-get install python3-tk`
> - macOS/Windows: já incluído no Python padrão

## 📦 Como executar

1. **Clone o repositório:**
```bash
git clone https://github.com/nicholascode-hub/trivia-game.git
cd trivia-game
```

2. **Instale as dependências:**
```bash
pip install ttkbootstrap
```

3. **Execute o jogo:**
```bash
python main.py
```

## 🎮 Como jogar

1. **Inicialização:** Execute o arquivo `main.py` para abrir a interface gráfica
2. **Controles:** Use F11 para tela cheia e ESC para sair da tela cheia
3. **Sistema de Vidas:** Você começa com 3 corações (vidas)
4. **Mecânica do Jogo:**
   - **Acertou:** Ganha 10 pontos e escolhe o próximo tópico
   - **Errou:** Perde 1 vida e muda automaticamente de tópico
   - **Game Over:** Quando acabam as 3 vidas
5. **Pontuação:** Cada resposta correta vale 10 pontos
6. **Tópicos:** Alterne entre K-pop e Programação conforme sua preferência

## 🧩 Lógica Principal do Jogo

### Arquitetura e Fluxo:

**1. Inicialização (`__init__`):**
- Cria a janela principal com tema "superhero" do ttkbootstrap
- Carrega dois bancos de dados estáticos de perguntas:
  - **K-pop:** 45+ perguntas sobre EXO, BLACKPINK, TWICE e K-pop geral
  - **Programação:** 20+ perguntas sobre Python e conceitos básicos
- Embaralha ambos os bancos usando `random.shuffle()`
- Inicializa variáveis do jogo (pontos=0, vidas=3, contador=0)

**2. Interface Gráfica (`setup_ui`):**
- Utiliza `ttkbootstrap` para tema moderno dark
- Sistema de scroll para telas pequenas
- Canvas customizado para desenhar corações coloridos (vidas)
- Frames organizados: título, informações, pergunta, opções, botões
- Suporte a tela cheia com binds F11/ESC

**3. Sistema de Perguntas (`get_current_question`, `next_question`):**
- **Rotação de tópicos:** Alterna entre K-pop e Programação
- **Anti-repetição:** Quando esgota um banco, reembaralha automaticamente
- **Índices independentes:** Mantém posição separada para cada categoria
- **Atualização dinâmica:** Modifica interface baseado no tópico atual

**4. Mecânica de Jogo (`check_answer`):**
```
Resposta Correta:
├── +10 pontos
├── Feedback positivo
└── Escolha de próximo tópico

Resposta Incorreta:
├── -1 vida (atualiza corações)
├── Troca automática de tópico
├── Verifica Game Over (vidas = 0)
└── Continua com nova pergunta
```

**5. Sistema de Vidas (`draw_hearts`, `update_lives_display`):**
- **Canvas personalizado:** Desenha corações usando coordenadas
- **Feedback visual:** Vermelho = vida, preto = vida perdida
- **Atualização dinâmica:** Redesenha a cada mudança de vida

**6. Controle de Fluxo:**
```
Início → Embaralhar Perguntas → Mostrar Pergunta → 
Aguardar Resposta → Verificar → [Correto: Escolher Tópico | Incorreto: Trocar Tópico] → 
Próxima Pergunta → [Continuar | Game Over] → Reiniciar
```

### Diferencial Técnico:
- **Banco de dados próprio:** Não depende de APIs externas
- **Interface responsiva:** Sistema de scroll e redimensionamento
- **Estado persistente:** Mantém progresso durante toda a sessão
- **Visual moderno:** ttkbootstrap com tema consistente
- **UX otimizada:** Feedback imediato e controles intuitivos

## 📚 Banco de Perguntas

### K-pop (45+ perguntas):
- **EXO:** Formação, subgrupos, membros, poderes míticos, álbuns, fandom
- **BLACKPINK:** Debut, integrantes, sucessos, recordes, parcerias globais
- **TWICE:** Reality show Sixteen, formação, evolução conceitual, turnês
- **K-pop Geral:** BTS, Girls' Generation, BIGBANG, termos e cultura

### Programação (20+ perguntas):
- **Python:** Sintaxe básica, funções, variáveis, tipos de dados
- **Conceitos:** Algoritmos, orientação a objetos, frameworks, Git
- **Ferramentas:** IDEs, debugging, open source, tipagem dinâmica

## 📝 Estrutura do Projeto

```
trivia-game/
├── main.py          # Arquivo principal com toda a lógica do jogo
├── README.md        # Este arquivo de documentação
└── requirements.txt # Lista de dependências (opcional)
```

### Organização do Código:
- **Classe TriviaGame:** Contém toda a lógica do jogo
- **Bancos de dados:** Arrays de dicionários com perguntas estruturadas
- **Interface:** Métodos para criação e gerenciamento da UI
- **Lógica de jogo:** Controle de fluxo, verificação de respostas, sistema de vidas

## 🎨 Características Técnicas

- **Framework UI:** ttkbootstrap (Bootstrap para Python)
- **Tema:** "superhero" (dark theme moderno)
- **Resolução:** Responsiva com scroll automático
- **Compatibilidade:** Python 3.6+ com tkinter
- **Arquitetura:** Orientada a objetos, classe única bem estruturada
- **Performance:** Leve, executa localmente sem dependências de rede

## 🤝 Contribuições

Contribuições são bem-vindas! Você pode:

### Como Contribuir:
- **Adicionar perguntas:** Expanda os bancos K-pop ou Programação
- **Novos tópicos:** Sugira categorias como Anime, História, Ciências
- **Melhorias UI:** Aprimorar design, animações, responsividade
- **Features:** Sistema de dificuldade, multiplayer, persistência de dados
- **Otimizações:** Performance, organização de código, documentação

### Processo:
1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça suas mudanças e commit: `git commit -m "Adiciona nova funcionalidade"`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Você pode usar, modificar e distribuir livremente, mantendo os créditos originais.

## 🎯 Roadmap / Próximas Funcionalidades

- [ ] **Sistema de dificuldade** (Fácil, Médio, Difícil)
- [ ] **Persistência de dados** (salvar high scores)
- [ ] **Modo cronômetro** (tempo limite por pergunta)
- [ ] **Novas categorias** (Anime, História, Ciências, Esportes)
- [ ] **Multiplayer local** (dois jogadores alternando)
- [ ] **Sistema de conquistas** (badges por marcos alcançados)
- [ ] **Export de estatísticas** (relatório de desempenho)
- [ ] **Modo treino** (revisar perguntas erradas)
- [ ] **Interface mobile** (versão para dispositivos móveis)
- [ ] **Sons e efeitos** (feedback audio para respostas)

## 🐛 Problemas Conhecidos

- Interface pode não escalar perfeitamente em telas muito pequenas (<800px)
- Tema dark pode ter contraste baixo em alguns monitores antigos
- F11 (fullscreen) pode não funcionar em alguns ambientes Linux específicos

---

### 📊 Estatísticas do Projeto
- **Linguagem:** Python 🐍
- **Linhas de código:** ~400+
- **Perguntas totais:** 65+
- **Categorias:** 2 principais
- **Dependências:** 1 externa (ttkbootstrap)

---

⭐ **Gostou do projeto? Deixe uma estrela no GitHub!**

🐛 **Encontrou um bug? Abra uma issue detalhada!**

💡 **Tem sugestões? Pull requests são bem-vindos!**
