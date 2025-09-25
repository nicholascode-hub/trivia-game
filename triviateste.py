import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

class TriviaGame:
    def __init__(self):
        self.root = ttk.Window(themename="superhero")
        self.root.title("Trivia Game - K-pop vs Exatas")
        self.root.geometry("900x700")  # Janela maior
        self.root.minsize(800, 600)    # Tamanho mínimo
        # Adicionar bind para F11 (fullscreen) e Escape (sair do fullscreen)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.is_fullscreen = False
        
        # Dicionários de perguntas
        self.kpop_questions = [
    # EXO questions
    {
        "pergunta": "Em que ano o EXO foi formado e qual agência gerencia o grupo?",
        "opcoes": ["2010, YG Entertainment", "2012, SM Entertainment", "2014, JYP Entertainment", "2016, Big Hit Entertainment"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual era a estratégia inicial de subgrupos do EXO?",
        "opcoes": [
            "EXO-K para Coreia do Sul e EXO-M para China, com músicas em coreano e mandarim",
            "EXO-A para Ásia e EXO-W para o mundo ocidental",
            "EXO-L para fãs e EXO-F para família",
            "EXO-B para baladas e EXO-D para danças"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Quantos membros formavam o EXO no debut e quantos permanecem atualmente?",
        "opcoes": ["12 no debut, 9 atualmente", "10 no debut, 7 atualmente", "9 no debut, 12 atualmente", "14 no debut, 10 atualmente"],
        "resposta_correta": 0
    },
    {
        "pergunta": "Quais membros chineses deixaram o EXO e em que período isso ocorreu?",
        "opcoes": [
            "Kris, Luhan e Tao, entre 2014 e 2015",
            "Xiumin, Suho e Lay, entre 2013 e 2014",
            "Baekhyun, Chen e Kai, entre 2015 e 2016",
            "Chanyeol, D.O. e Sehun, entre 2016 e 2017"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Quem é o líder do EXO e qual é o seu “poder mítico”?",
        "opcoes": ["Suho, poder da água", "Kai, poder do fogo", "D.O., poder da terra", "Lay, poder do vento"],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual dos membros do EXO é o mais velho e fazia parte originalmente do EXO-M?",
        "opcoes": ["Xiumin", "Baekhyun", "Chen", "Sehun"],
        "resposta_correta": 0
    },
    {
        "pergunta": "Quais são os membros da subunidade EXO-CBX?",
        "opcoes": [
            "Chen, Baekhyun e Xiumin",
            "Suho, D.O. e Sehun",
            "Chanyeol, Kai e Tao",
            "Lay, Kris e Luhan"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual é o nome da segunda subunidade formada por Sehun e Chanyeol?",
        "opcoes": ["EXO-CBX", "EXO-SC", "SuperM", "EXO-K"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual álbum do EXO foi o primeiro a vender mais de 1 milhão de cópias na Coreia em 12 anos?",
        "opcoes": ["Overdose", "XOXO", "Exodus", "The War"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Como se chama o fandom oficial do EXO e qual é o significado da letra 'L'?",
        "opcoes": [
            "EXO-L, 'L' significa 'Love' e representa a união entre EXO-K e EXO-M",
            "EXO-F, 'F' significa 'Família'",
            "EXO-A, 'A' significa 'Amigos'",
            "EXO-B, 'B' significa 'Brothers'"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "O que simboliza a narrativa mitológica do EXO no início da carreira?",
        "opcoes": [
            "Seres mitológicos da Terra",
            "Alienígenas de um exoplaneta com superpoderes individuais",
            "Robôs futuristas",
            "Heróis rivais de outra dimensão"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual dos seguintes não é um poder mítico atribuído a um membro do EXO?",
        "opcoes": [
            "Gelo (Xiumin)", "Água (Suho)", "Fogo (Chanyeol)", "Electricidade (Baekhyun)"
        ],
        "resposta_correta": 3
    },
    {
        "pergunta": "Qual dos álbuns do EXO foi o mais vendido na Coreia do Sul, ultrapassando 2 milhões de cópias?",
        "opcoes": ["Exist", "Overdose", "Exodus", "Don't Mess Up My Tempo"],
        "resposta_correta": 0
    },
    {
        "pergunta": "O que caracteriza o modelo de carreira ‘híbrido’ adotado por membros do EXO?",
        "opcoes": [
            "Trazer novos membros para substituir antigos",
            "Gerenciar atividades solo e grupo por diferentes agências para maior autonomia",
            "Parar as atividades solo para focar só no grupo",
            "Fazer todos os contratos diretamente com a SM Entertainment"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Quando está previsto o retorno completo do EXO com todos os nove membros após o serviço militar?",
        "opcoes": ["Final de 2024", "Final de 2025", "Início de 2026", "Nenhuma data prevista"],
        "resposta_correta": 1
    },

    # BLACKPINK questions
    {
        "pergunta": "Quantos membros compõem o BLACKPINK e quais são seus nomes?",
        "opcoes": ["Três: Jisoo, Jennie, Rosé", "Quatro: Jisoo, Jennie, Rosé, Lisa", "Cinco: Jisoo, Jennie, Rosé, Lisa, Rose", "Seis: Jisoo, Jennie, Rosé, Lisa, Lisa, Jennie"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Quando a YG Entertainment confirmou oficialmente o debut do BLACKPINK?",
        "opcoes": ["Maio de 2016", "Agosto de 2015", "Junho de 2017", "Janeiro de 2016"],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual foi a ordem de revelação das integrantes do BLACKPINK em 2016?",
        "opcoes": [
            "Jennie, Lisa, Jisoo, Rosé",
            "Rosé, Jisoo, Lisa, Jennie",
            "Lisa, Jennie, Rosé, Jisoo",
            "Jisoo, Rosé, Lisa, Jennie"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Quais singles Lançados no debut de BLACKPINK alcançaram o topo da Billboard World Digital Song Sales?",
        "opcoes": [
            "'Whistle' em 1º e 'Boombayah' em 2º",
            "'Playing with Fire' e 'Stay'",
            "'Ddu-Du Ddu-Du' e 'Kill This Love'",
            "'Pink Venom' e 'Shut Down'"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual integrante é conhecida como vocalista líder e também atua como atriz?",
        "opcoes": ["Jennie", "Jisoo", "Rosé", "Lisa"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual membro do BLACKPINK é reconhecido por ser rapper principal e uma importante ícone de moda de luxo Chanel?",
        "opcoes": ["Lisa", "Jennie", "Jisoo", "Rosé"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Lisa tem uma característica única em sua trajetória na YG Entertainment, qual é?",
        "opcoes": [
            "Única membro coreana do grupo",
            "Única traineee aprovada em audição na Tailândia em 2010",
            "A primeira integrante a lançar um álbum solo",
            "A única que canta e não dança"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Quais gêneros musicais predominam na sonoridade do BLACKPINK?",
        "opcoes": [
            "Jazz e blues",
            "Rock e country",
            "EDM, pop, hip-hop e trap",
            "Reggae e samba"
        ],
        "resposta_correta": 2
    },
    {
        "pergunta": "Qual álbum do BLACKPINK foi o primeiro grupo feminino de K-pop a estrear em 1º lugar na Billboard 200?",
        "opcoes": [
            "Square One",
            "Square Up",
            "The Album",
            "Born Pink"
        ],
        "resposta_correta": 3
    },
    {
        "pergunta": "Quais artistas ocidentais já colaboraram com o BLACKPINK em parceria musical?",
        "opcoes": [
            "Dua Lipa, Selena Gomez e Lady Gaga",
            "Beyoncé, Rihanna e Ariana Grande",
            "Taylor Swift, Adele e Billie Eilish",
            "Ed Sheeran, Shawn Mendes e Bruno Mars"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Que função cada integrante do BLACKPINK desempenha no grupo?",
        "opcoes": [
            "Jisoo - Dançarina; Jennie - Vocalista; Rosé - Rapper; Lisa - Vocalista",
            "Jisoo - Vocalista líder; Jennie - Rapper principal; Rosé - Vocalista principal; Lisa - Dançarina principal e rapper",
            "Jisoo - Rapper; Jennie - Dançarina; Rosé - Vocalista; Lisa - Produtora",
            "Todas são vocalistas principais"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Quais marcas de luxo cada integrante do BLACKPINK representa como embaixadora global?",
        "opcoes": [
            "Jisoo - Dior e Cartier; Jennie - Chanel e Calvin Klein; Rosé - Yves Saint Laurent e Tiffany & Co; Lisa - Louis Vuitton, Céline e Bulgari",
            "Jisoo - Chanel; Jennie - Dior; Rosé - Cartier; Lisa - Calvin Klein",
            "Jisoo - Louis Vuitton; Jennie - Tiffany & Co; Rosé - Bulgari; Lisa - Yves Saint Laurent",
            "Jisoo - Gucci; Jennie - Prada; Rosé - Fendi; Lisa - Versace"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual recorde digital o BLACKPINK detém no YouTube?",
        "opcoes": [
            "Maior número de inscritos para banda pop global",
            "Canal de artista musical com maior número de inscritos (mais de 96 milhões)",
            "Vídeo musical mais longo da história",
            "Primeiro grupo a usar YouTube para debutar"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual foi o primeiro single em língua coreana a liderar a parada Global Top Songs do Spotify?",
        "opcoes": [
            "'Ddu-Du Ddu-Du'",
            "'Kill This Love'",
            "'Pink Venom'",
            "'Boombayah'"
        ],
        "resposta_correta": 2
    },
    {
        "pergunta": "Qual novo modelo de negócios as integrantes do BLACKPINK adotaram para suas carreiras solo?",
        "opcoes": [
            "Continuar exclusivamente sob a YG Entertainment",
            "Fundar suas próprias gravadoras ou assinar com outras agências mantendo o grupo coeso",
            "Desistir das carreiras solo para focar só no grupo",
            "Mudar para uma gravadora americana, dissolvendo o grupo"
        ],
        "resposta_correta": 1
    },

    # TWICE and General Kpop questions (mixed)
    {
        "pergunta": "Qual grupo de K-pop é conhecido pela música 'Dynamite'?",
        "opcoes": ["BLACKPINK", "BTS", "TWICE", "Red Velvet"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Em que ano o grupo Girls' Generation (SNSD) debutou?",
        "opcoes": ["2006", "2007", "2008", "2009"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual é o nome real de G-Dragon do BIGBANG?",
        "opcoes": ["Kim Jong-kook", "Kwon Ji-yong", "Lee Min-ho", "Park Ji-min"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Quantos membros tem o grupo BLACKPINK?",
        "opcoes": ["3", "4", "5", "6"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual grupo feminino é conhecido pela música 'DDU-DU DDU-DU'?",
        "opcoes": ["TWICE", "Red Velvet", "BLACKPINK", "ITZY"],
        "resposta_correta": 2
    },
    {
        "pergunta": "O que significa 'maknae' no K-pop?",
        "opcoes": ["Líder do grupo", "Membro mais velho", "Membro mais novo", "Vocalista principal"],
        "resposta_correta": 2
    },
    {
        "pergunta": "Qual empresa é responsável pelo BTS?",
        "opcoes": ["SM Entertainment", "YG Entertainment", "Big Hit Entertainment", "JYP Entertainment"],
        "resposta_correta": 2
    },
    {
        "pergunta": "Quantos membros tem o grupo EXO atualmente?",
        "opcoes": ["8", "9", "10", "12"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual é o nome do fandom do TWICE?",
        "opcoes": ["ONCE", "BLINK", "ARMY", "ReVeluv"],
        "resposta_correta": 0
    },
    {
        "pergunta": "Em que país nasceu a integrante Lisa do BLACKPINK?",
        "opcoes": ["Coreia do Sul", "Tailândia", "China", "Japão"],
        "resposta_correta": 1
    },

    # TWICE questions
    {
        "pergunta": "Quantas integrantes o TWICE tem atualmente e qual foi a razão para essa formação?",
        "opcoes": [
            "Sete, escolhidas apenas pelo reality Sixteen",
            "Nove, com duas integrantes adicionadas após o reality show",
            "Oito, após uma integrante deixar o grupo",
            "Dez, com membros incluindo trainees convidados"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual reality show formou o TWICE e qual foi sua característica principal na seleção?",
        "opcoes": [
            "Produce 101, foco apenas em habilidades técnicas",
            "Sixteen, avaliava canto, dança, carisma e personalidade",
            "Unpretty Rapstar, competição de rap",
            "Idol School, votação popular exclusiva"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual foi a controvérsia na formação final do TWICE após o reality 'Sixteen'?",
        "opcoes": [
            "A adição de um integrante masculino ao grupo feminino",
            "A substituição da líder após o programa",
            "A ampliação do grupo de sete para nove membros, adicionando eliminadas",
            "A escolha do nome TWICE por votação dos fãs"
        ],
        "resposta_correta": 2
    },
    {
        "pergunta": "Quem foi a integrante escolhida por J.Y. Park para complementar a formação do grupo e qual sua habilidade destacada?",
        "opcoes": [
            "Tzuyu, a mais alta e viral em arquearia",
            "Momo, conhecida como 'máquina de dança'",
            "Jihyo, a líder com maior período de trainee",
            "Sana, fluente em coreano e japonesa"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual música marcou a estreia oficial do TWICE e qual fenômeno diferente seu videoclipe causou?",
        "opcoes": [
            "'Like Ooh-Ahh', ganhou popularidade gradual com viral de vídeo de zumbis",
            "'Cheer Up', desde o início no topo das paradas",
            "'Fancy', lançamento direto internacional",
            "'The Feels', primeiro single em inglês"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual conceito musical o TWICE usou inicialmente e como ele evoluiu em 2019?",
        "opcoes": [
            "'Black Swan' para um visual sombrio",
            "'Color pop', evoluindo para estética chic e madura com 'Fancy'",
            "'Hip-hop' para EDM progressivo",
            "'Baladas' para dance pop"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Que estratégia o TWICE utilizou para conquistar o mercado global ocidental?",
        "opcoes": [
            "Estreia do single em inglês 'The Feels'",
            "Participação em programas americanos de TV",
            "Colaborações com artistas americanos",
            "Tour mundial antes do debut coreano"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual o nome do fandom do TWICE e qual é o significado por trás desse nome?",
        "opcoes": [
            "ONCE, que significa 'Amar uma vez e retribuir duas vezes'",
            "BLINK, significando piscada e conexão rápida",
            "ARMY, união e força do exército",
            "ReVeluv, amor por Red Velvet"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual foi o marco da turnê 'Ready to Be' em números e país onde o TWICE ficou surpreso com o engajamento?",
        "opcoes": [
            "Mais de 2 milhões de fãs em 20 países, surpreendidos na Austrália",
            "Mais de 1,5 milhão de fãs em 14 países, com passagem notável no Brasil",
            "1 milhão de fãs somente na Coreia",
            "5 milhões de fãs no Japão"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Quem é a integrante que teve o maior período de trainee no TWICE e também é líder do grupo?",
        "opcoes": [
            "Nayeon",
            "Jihyo",
            "Chaeyoung",
            "Dahyun"
        ],
        "resposta_correta": 1
    }
]


        # Fixed indentation for exatas_questions
        self.exatas_questions = [
            # ===== PERGUNTAS DE PROGRAMAÇÃO =====
            {
                "pergunta": "O que é uma linguagem de programação?",
                "opcoes": [
                    "Uma linguagem falada por programadores",
                    "Um conjunto de instruções que um computador pode entender e executar",
                    "Um software para criar imagens",
                    "Um tipo de hardware que processa dados"
                ],
                "resposta_correta": 1
            },
            # ... (rest of the exatas questions)
        ]
    
        # Variáveis do jogo
        self.current_topic = "kpop"
        self.score = 0
        self.question_count = 0
        self.lives = 3  # Sistema de vidas
        self.current_question = None
        self.kpop_shuffled = self.kpop_questions.copy()
        self.exatas_shuffled = self.exatas_questions.copy()
        self.kpop_index = 0
        self.exatas_index = 0
        self.game_state = "question"  # "question" ou "topic_choice"
        
        # Embaralhar as perguntas
        random.shuffle(self.kpop_shuffled)
        random.shuffle(self.exatas_shuffled)
        
        self.setup_ui()
        self.next_question()
    
    def draw_heart(self, canvas, color):
        """Desenha um coração no canvas com a cor especificada"""
        canvas.delete("all")
        # Coordenadas para desenhar um coração maior (30x30)
        # Parte superior (dois círculos)
        canvas.create_oval(4, 6, 15, 17, fill=color, outline=color)
        canvas.create_oval(15, 6, 26, 17, fill=color, outline=color)
        # Parte inferior (triângulo)
        canvas.create_polygon(4, 12, 26, 12, 15, 26, fill=color, outline=color, smooth=True)
    
    def draw_hearts(self):
        """Desenha todos os corações baseado nas vidas atuais"""
        for i in range(3):
            if i < self.lives:
                self.draw_heart(self.heart_canvases[i], "red")  # Coração vermelho
            else:
                self.draw_heart(self.heart_canvases[i], "black")  # Coração preto
    
    def setup_ui(self):
        # Container principal para centralização
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=BOTH, expand=True)
        
        # Frame principal com scrollbar caso necessário
        main_canvas = tk.Canvas(main_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=main_canvas.yview)
        
        # Frame para centralização horizontal
        center_frame = ttk.Frame(main_canvas)
        
        # Frame do conteúdo com largura limitada para centralização
        self.scrollable_frame = ttk.Frame(center_frame, padding="40")
        self.scrollable_frame.pack(expand=True)
        
        # Configurar scroll
        def configure_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            # Centralizar horizontalmente
            canvas_width = main_canvas.winfo_width()
            frame_width = center_frame.winfo_reqwidth()
            x_position = max(0, (canvas_width - frame_width) // 2)
            main_canvas.coords("center_window", x_position, 0)
        
        center_frame.bind("<Configure>", configure_scroll_region)
        main_canvas.bind("<Configure>", configure_scroll_region)
        
        main_canvas.create_window((0, 0), window=center_frame, anchor="nw", tags="center_window")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas e scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind scroll do mouse
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Título
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill=X, pady=(0, 25))
        
        # Usar tk.Label para poder controlar a fonte do título
        title_label = tk.Label(title_frame, text="🎵 TRIVIA GAME 🧪", 
                              font=("Arial", 28, "bold"), 
                              bg='#2c3e50', fg='white')  # Cor fixa para compatibilidade
        title_label.pack()
        
        # Instruções de fullscreen
        instructions_label = tk.Label(title_frame, text="F11: Tela Cheia | ESC: Sair da Tela Cheia | Mouse: Scroll",
                                     font=("Arial", 12),
                                     bg='#2c3e50', fg='lightgray')  # Cor fixa para compatibilidade
        instructions_label.pack(pady=(8, 0))
        
        # Score, contador e vidas
        info_frame = ttk.Frame(self.scrollable_frame)
        info_frame.pack(fill=X, pady=(0, 25))
        
        # Vidas (corações) - lado esquerdo
        lives_frame = ttk.Frame(info_frame)
        lives_frame.pack(side=LEFT)
        
        lives_label = tk.Label(lives_frame, text="Vidas: ", 
                              font=("Arial", 14, "bold"),
                              bg='#2c3e50', fg='white')  # Cor fixa para compatibilidade
        lives_label.pack(side=LEFT)
        
        # Criar corações coloridos usando Canvas (maiores)
        self.heart_canvases = []
        for i in range(3):
            canvas = tk.Canvas(lives_frame, width=30, height=30, highlightthickness=0, bg='#2c3e50')
            canvas.pack(side=LEFT, padx=4)
            self.heart_canvases.append(canvas)
        
        # Score - centro
        self.score_label = tk.Label(info_frame, text="Pontuação: 0",
                                   font=("Arial", 14, "bold"),
                                   bg='#2c3e50', fg='white')  # Cor fixa para compatibilidade
        self.score_label.pack(side=LEFT, padx=(30, 0))
        
        # Contador de perguntas - direita
        self.question_count_label = tk.Label(info_frame, text="Pergunta: 0",
                                           font=("Arial", 14, "bold"),
                                           bg='#2c3e50', fg='white')  # Cor fixa para compatibilidade
        self.question_count_label.pack(side=RIGHT)
        
        # Tópico atual
        self.topic_label = tk.Label(self.scrollable_frame, text="",
                                   font=("Arial", 18, "bold"),
                                   bg='#2c3e50', fg='lightblue')  # Cor fixa para compatibilidade
        self.topic_label.pack(pady=(0, 25))
        
        # Frame da pergunta
        self.question_frame = ttk.LabelFrame(self.scrollable_frame, text="Pergunta", padding="25")
        self.question_frame.pack(fill=X, pady=(0, 25))
        
        self.question_label = tk.Label(self.question_frame, text="", wraplength=900,
                                      font=("Arial", 16),
                                      bg='#2c3e50', fg='white')  # Cor fixa para compatibilidade
        self.question_label.pack()
        
        # Frame das opções
        self.options_frame = ttk.LabelFrame(self.scrollable_frame, text="Opções", padding="25")
        self.options_frame.pack(fill=X, pady=(0, 25))
        
        self.option_var = tk.StringVar()
        self.option_buttons = []
        
        for i in range(4):
            btn = ttk.Radiobutton(self.options_frame, text="", variable=self.option_var, 
                                value=str(i))
            btn.pack(anchor=W, pady=8)
            self.option_buttons.append(btn)
        
        # Frame de escolha de tópico
        self.topic_choice_frame = ttk.LabelFrame(self.scrollable_frame, text="✅ Você acertou! Escolha o próximo tópico:", padding="25")
        
        self.topic_var = tk.StringVar(value="kpop")
        
        kpop_radio = ttk.Radiobutton(self.topic_choice_frame, text="🎵 K-pop", 
                                   variable=self.topic_var, value="kpop")
        kpop_radio.pack(anchor=W, pady=8)
        
        exatas_radio = ttk.Radiobutton(self.topic_choice_frame, text="🧪 Exatas", 
                                     variable=self.topic_var, value="exatas")
        exatas_radio.pack(anchor=W, pady=8)
        
        self.continue_btn = ttk.Button(self.topic_choice_frame, text="Próxima Pergunta", 
                                     command=self.continue_game, bootstyle=SUCCESS)
        self.continue_btn.pack(pady=15)
        
        # Frame dos botões - sempre visível na parte inferior
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(fill=X, pady=35, side=BOTTOM)  # Extra padding para evitar corte
        
        self.submit_btn = ttk.Button(button_frame, text="Responder", 
                                   command=self.check_answer, bootstyle=PRIMARY)
        self.submit_btn.pack(side=LEFT, padx=(0, 15))
        
        # Botão de reiniciar
        restart_btn = ttk.Button(button_frame, text="Reiniciar Jogo", 
                               command=self.restart_game, bootstyle=WARNING)
        restart_btn.pack(side=RIGHT)
        
        # Desenhar corações iniciais após criar a interface
        self.draw_hearts()
    
    def toggle_fullscreen(self, event=None):
        """Alterna entre fullscreen e janela normal"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
    
    def exit_fullscreen(self, event=None):
        """Sai do modo fullscreen"""
        self.is_fullscreen = False
        self.root.attributes('-fullscreen', False)
    
    def get_current_question(self):
        if self.current_topic == "kpop":
            if self.kpop_index >= len(self.kpop_shuffled):
                random.shuffle(self.kpop_shuffled)
                self.kpop_index = 0
            question = self.kpop_shuffled[self.kpop_index]
            self.kpop_index += 1
        else:
            if self.exatas_index >= len(self.exatas_shuffled):
                random.shuffle(self.exatas_shuffled)
                self.exatas_index = 0
            question = self.exatas_shuffled[self.exatas_index]
            self.exatas_index += 1
        
        return question
    
    def next_question(self):
        self.question_count += 1
        self.current_question = self.get_current_question()
        self.game_state = "question"
        
        # Mostrar elementos da pergunta e esconder escolha de tópico
        self.show_question_elements()
        
        # Atualizar conteúdo
        topic_text = "🎵 K-POP" if self.current_topic == "kpop" else "🧪 EXATAS"
        self.topic_label.config(text=f"Tópico: {topic_text}")
        
        self.question_label.config(text=self.current_question["pergunta"])
        
        for i, option in enumerate(self.current_question["opcoes"]):
            self.option_buttons[i].config(text=f"{chr(65+i)}) {option}")
        
        self.option_var.set("")
        
        # Atualizar contadores e vidas
        self.update_lives_display()
        self.score_label.config(text=f"Pontuação: {self.score}")
        self.question_count_label.config(text=f"Pergunta: {self.question_count}")
    
    def update_lives_display(self):
        """Atualiza a exibição dos corações baseado nas vidas restantes"""
        self.draw_hearts()
    
    def show_question_elements(self):
        """Mostra elementos da pergunta e esconde escolha de tópico"""
        self.question_frame.pack(fill=X, pady=(0, 20))
        self.options_frame.pack(fill=X, pady=(0, 20))
        self.submit_btn.pack(side=LEFT, padx=(0, 10))
        self.topic_choice_frame.pack_forget()
    
    def game_over(self):
        """Exibe tela de game over e reinicia o jogo"""
        messagebox.showinfo("Game Over! 💀", 
                          f"Suas vidas acabaram!\n\n🏆 Pontuação Final: {self.score}\n📊 Perguntas Respondidas: {self.question_count}\n\nO jogo será reiniciado!")
        self.restart_game_silent()
    
    def restart_game_silent(self):
        """Reinicia o jogo sem confirmação (usado após game over)"""
        self.score = 0
        self.question_count = 0
        self.lives = 3
        self.current_topic = "kpop"
        self.kpop_index = 0
        self.exatas_index = 0
        self.game_state = "question"
        
        # Reembaralhar as perguntas
        random.shuffle(self.kpop_shuffled)
        random.shuffle(self.exatas_shuffled)
        
        self.update_lives_display()
        self.next_question()
    
    def show_topic_choice_elements(self):
        """Esconde elementos da pergunta e mostra escolha de tópico"""
        self.question_frame.pack_forget()
        self.options_frame.pack_forget()
        self.submit_btn.pack_forget()
        self.topic_choice_frame.pack(fill=X, pady=20)
        self.topic_var.set(self.current_topic)
    
    def check_answer(self):
        selected = self.option_var.get()
        
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione uma opção!")
            return
        
        selected_index = int(selected)
        correct_index = self.current_question["resposta_correta"]
        
        if selected_index == correct_index:
            self.score += 10
            self.game_state = "topic_choice"
            messagebox.showinfo("Correto! ✅", 
                              f"Parabéns! Você acertou!\n\nResposta: {self.current_question['opcoes'][correct_index]}")
            
            # Mostrar escolha de tópico
            self.show_topic_choice_elements()
            
        else:
            # Perder uma vida
            self.lives -= 1
            self.update_lives_display()
            
            # Verificar se acabaram as vidas
            if self.lives <= 0:
                messagebox.showerror("Incorreto! ❌", 
                                   f"Resposta errada!\n\nResposta correta: {self.current_question['opcoes'][correct_index]}")
                self.game_over()
                return
            
            messagebox.showerror("Incorreto! ❌", 
                               f"Resposta errada!\n\nResposta correta: {self.current_question['opcoes'][correct_index]}\n\n💔 Vidas restantes: {self.lives}")
            
            # Trocar automaticamente de tópico
            self.current_topic = "exatas" if self.current_topic == "kpop" else "kpop"
            self.next_question()
    
    def continue_game(self):
        self.current_topic = self.topic_var.get()
        self.next_question()
    
    def restart_game(self):
        result = messagebox.askyesno("Reiniciar", "Tem certeza que deseja reiniciar o jogo?")
        if result:
            self.score = 0
            self.question_count = 0
            self.lives = 3
            self.current_topic = "kpop"
            self.kpop_index = 0
            self.exatas_index = 0
            self.game_state = "question"
            
            # Reembaralhar as perguntas
            random.shuffle(self.kpop_shuffled)
            random.shuffle(self.exatas_shuffled)
            
            self.update_lives_display()
            self.next_question()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TriviaGame()
    game.run()