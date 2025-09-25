import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import random

class DialogueType(Enum):
    NORMAL = "normal"
    CHOICE = "choice"
    END = "end"

@dataclass
class DialogueNode:
    """Representa um nó na árvore de diálogo"""
    id: str
    text: str
    dialogue_type: DialogueType
    choices: Optional[Dict[str, str]] = None
    next_node: Optional[str] = None
    consequences: Optional[Dict[str, Any]] = None

class DialogueTree:
    """Sistema de árvore de diálogos"""
    def __init__(self):
        self.nodes: Dict[str, DialogueNode] = {}
        self.current_node: Optional[str] = None
        self.dialogue_history: List[str] = []
    
    def add_node(self, node: DialogueNode):
        self.nodes[node.id] = node
    
    def start_dialogue(self, start_node_id: str):
        if start_node_id in self.nodes:
            self.current_node = start_node_id
            return True
        return False
    
    def get_current_node(self) -> Optional[DialogueNode]:
        if self.current_node:
            return self.nodes.get(self.current_node)
        return None
    
    def process_choice(self, choice_key: str) -> bool:
        current = self.get_current_node()
        if current and current.choices and choice_key in current.choices:
            self.dialogue_history.append(f"Escolha: {choice_key}")
            self.current_node = current.choices[choice_key]
            return True
        return False
    
    def advance_dialogue(self):
        current = self.get_current_node()
        if current and current.next_node:
            self.current_node = current.next_node

class Room:
    """Representa um cômodo do jogo"""
    def __init__(self, name: str, description: str, app_icon: str = "🏠"):
        self.name = name
        self.description = description
        self.app_icon = app_icon
        self.connections: Dict[str, 'Room'] = {}
        self.dialogue_tree: Optional[DialogueTree] = None
        self.visited = False
        self.items: List[str] = []
        self.npcs: List[str] = []
        self.social_posts: List[Dict] = []
    
    def add_connection(self, direction: str, room: 'Room'):
        self.connections[direction] = room
    
    def get_available_directions(self) -> List[str]:
        return list(self.connections.keys())
    
    def set_dialogue(self, dialogue_tree: DialogueTree):
        self.dialogue_tree = dialogue_tree
    
    def enter(self):
        self.visited = True
    
    def add_social_post(self, username: str, content: str, platform: str = "Chirper"):
        post = {
            "username": username,
            "content": content,
            "platform": platform,
            "timestamp": datetime.now().strftime("%H:%M"),
            "likes": random.randint(0, 100),
            "comments": random.randint(0, 20)
        }
        self.social_posts.append(post)

class Player:
    """Representa o jogador"""
    def __init__(self, name: str):
        self.name = name
        self.current_room: Optional[Room] = None
        self.inventory: List[str] = []
        self.health = 100
        self.game_flags: Dict[str, Any] = {}
        self.social_followers = 42
        self.notifications = []
    
    def move_to_room(self, room: Room):
        self.current_room = room
        room.enter()
    
    def move(self, direction: str) -> bool:
        if self.current_room and direction in self.current_room.connections:
            new_room = self.current_room.connections[direction]
            self.move_to_room(new_room)
            return True
        return False
    
    def add_item(self, item: str):
        self.inventory.append(item)
    
    def has_item(self, item: str) -> bool:
        return item in self.inventory
    
    def add_notification(self, message: str):
        self.notifications.append({
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M")
        })

class DesktopWindow:
    """Simula uma janela de desktop"""
    def __init__(self, parent, title: str, icon: str, width: int = 500, height: int = 400):
        self.window = tk.Toplevel(parent)
        self.window.title(f"{icon} {title}")
        self.window.geometry(f"{width}x{height}")
        self.window.configure(bg="#2c2c2c")
        
        # Barra de título customizada
        title_bar = tk.Frame(self.window, bg="#404040", height=30)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        
        title_label = tk.Label(title_bar, text=f"{icon} {title}", 
                              bg="#404040", fg="white", font=("Arial", 10, "bold"))
        title_label.pack(side="left", padx=10, pady=5)
        
        close_btn = tk.Button(title_bar, text="✕", bg="#ff4444", fg="white",
                             font=("Arial", 8, "bold"), width=3, height=1,
                             command=self.close, border=0)
        close_btn.pack(side="right", padx=5, pady=2)
        
        # Área de conteúdo
        self.content_frame = tk.Frame(self.window, bg="#2c2c2c")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def close(self):
        self.window.destroy()

class SocialMediaApp:
    """Aplicativo de rede social"""
    def __init__(self, parent, game_ref, platform_name: str, color: str):
        self.game = game_ref
        self.platform_name = platform_name
        self.color = color
        self.window = DesktopWindow(parent, platform_name, "📱")
        
        # Interface da rede social
        self.create_social_interface()
    
    def create_social_interface(self):
        # Header
        header = tk.Frame(self.window.content_frame, bg=self.color, height=50)
        header.pack(fill="x", pady=(0, 10))
        header.pack_propagate(False)
        
        platform_label = tk.Label(header, text=self.platform_name, 
                                 bg=self.color, fg="white", 
                                 font=("Arial", 16, "bold"))
        platform_label.pack(pady=10)
        
        # Área de posts
        self.posts_frame = scrolledtext.ScrolledText(self.window.content_frame, 
                                                    bg="#1a1a1a", fg="white",
                                                    font=("Arial", 10))
        self.posts_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Área de input
        input_frame = tk.Frame(self.window.content_frame, bg="#2c2c2c")
        input_frame.pack(fill="x")
        
        self.input_entry = tk.Entry(input_frame, bg="#404040", fg="white", 
                                   font=("Arial", 10), insertbackground="white")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(input_frame, text="Enviar", bg=self.color, fg="white",
                           command=self.send_message, font=("Arial", 9, "bold"))
        send_btn.pack(side="right")
        
        self.update_posts()
    
    def update_posts(self):
        self.posts_frame.delete(1.0, tk.END)
        room = self.game.player.current_room
        
        if room and room.social_posts:
            for post in room.social_posts:
                post_text = f"@{post['username']} • {post['timestamp']}\n"
                post_text += f"{post['content']}\n"
                post_text += f"❤️ {post['likes']} 💬 {post['comments']}\n"
                post_text += "─" * 40 + "\n\n"
                
                self.posts_frame.insert(tk.END, post_text)
        else:
            self.posts_frame.insert(tk.END, "📱 Nenhum post encontrado nesta localização...\n")
    
    def send_message(self, event=None):
        message = self.input_entry.get().strip()
        if message:
            # Processar como comando do jogo
            self.game.process_social_command(message, self.platform_name)
            self.input_entry.delete(0, tk.END)

class FileExplorerApp:
    """Aplicativo explorador de arquivos"""
    def __init__(self, parent, game_ref):
        self.game = game_ref
        self.window = DesktopWindow(parent, "Explorador", "📁")
        self.create_explorer_interface()
    
    def create_explorer_interface(self):
        # Barra de navegação
        nav_frame = tk.Frame(self.window.content_frame, bg="#404040", height=40)
        nav_frame.pack(fill="x", pady=(0, 10))
        nav_frame.pack_propagate(False)
        
        back_btn = tk.Button(nav_frame, text="⬅️", bg="#555555", fg="white",
                           command=self.go_back, font=("Arial", 12))
        back_btn.pack(side="left", padx=5, pady=5)
        
        self.location_label = tk.Label(nav_frame, text="📍 Localização Atual", 
                                      bg="#404040", fg="white", font=("Arial", 10))
        self.location_label.pack(side="left", padx=20, pady=10)
        
        # Lista de arquivos/pastas
        self.file_list = tk.Listbox(self.window.content_frame, bg="#1a1a1a", fg="white",
                                   font=("Arial", 10), selectbackground="#555555")
        self.file_list.pack(fill="both", expand=True, pady=(0, 10))
        self.file_list.bind("<Double-Button-1>", self.open_item)
        
        # Área de informações
        info_frame = tk.Frame(self.window.content_frame, bg="#2c2c2c")
        info_frame.pack(fill="x")
        
        self.info_text = tk.Text(info_frame, bg="#404040", fg="white", height=4,
                               font=("Arial", 9))
        self.info_text.pack(fill="x")
        
        self.update_explorer()
    
    def update_explorer(self):
        room = self.game.player.current_room
        if not room:
            return
        
        self.location_label.config(text=f"📍 {room.name}")
        
        # Limpar lista
        self.file_list.delete(0, tk.END)
        
        # Adicionar conexões como pastas
        for direction, connected_room in room.connections.items():
            icon = "📁" if not connected_room.visited else "📂"
            self.file_list.insert(tk.END, f"{icon} {direction.upper()} - {connected_room.name}")
        
        # Adicionar itens como arquivos
        for item in room.items:
            self.file_list.insert(tk.END, f"📄 {item}")
        
        # Adicionar NPCs
        for npc in room.npcs:
            self.file_list.insert(tk.END, f"👤 {npc}")
        
        # Atualizar informações
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, room.description)
    
    def go_back(self):
        # Lógica para voltar (poderia implementar histórico)
        pass
    
    def open_item(self, event):
        selection = self.file_list.curselection()
        if selection:
            item_text = self.file_list.get(selection[0])
            
            if item_text.startswith("📁") or item_text.startswith("📂"):
                # Extrair direção
                direction = item_text.split(" - ")[0].split(" ")[1].lower()
                if self.game.player.move(direction):
                    self.game.update_all_windows()
                    self.game.add_system_message(f"Moveu-se para {direction}")
            
            elif item_text.startswith("👤"):
                # Iniciar diálogo
                self.game.start_dialogue()

class GameDesktop:
    """Interface principal do desktop do jogo"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🖥️ Desktop Narrativo")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a1a")
        
        self.player = None
        self.rooms = {}
        self.open_windows = []
        
        self.setup_game()
        self.create_desktop()
        
    def setup_game(self):
        """Configura o mundo do jogo"""
        # Criar cômodos com temas de redes sociais
        entrada = Room("Chirper Central", 
                      "O hub principal das redes sociais. Aqui você vê as últimas tendências e pode se conectar com outros usuários.",
                      "🐦")
        
        sala = Room("InstaSpace", 
                   "Uma galeria visual onde imagens e vídeos contam histórias. O algoritmo aqui prioriza conteúdo visual impactante.",
                   "📸")
        
        cozinha = Room("LinkedSpace Pro",
                      "A rede profissional onde carreiras são construídas. Conexões de negócios e oportunidades abundam aqui.",
                      "💼")
        
        biblioteca = Room("ReddiChan Community",
                         "Um fórum onde discussões profundas acontecem. Comunidades se formam em torno de interesses específicos.",
                         "🧠")
        
        quarto = Room("SnapVibe Stories",
                     "Momentos efêmeros que desaparecem rapidamente. Aqui a autenticidade e espontaneidade reinam.",
                     "👻")
        
        # Conexões
        entrada.add_connection("norte", sala)
        entrada.add_connection("leste", cozinha)
        entrada.add_connection("sul", biblioteca)
        
        sala.add_connection("sul", entrada)
        sala.add_connection("leste", quarto)
        sala.add_connection("sudeste", biblioteca)
        
        cozinha.add_connection("oeste", entrada)
        cozinha.add_connection("norte", quarto)
        cozinha.add_connection("sul", biblioteca)
        
        biblioteca.add_connection("norte", entrada)
        biblioteca.add_connection("leste", cozinha)
        biblioteca.add_connection("nordeste", sala)
        biblioteca.add_connection("nordeste", quarto)
        
        quarto.add_connection("oeste", sala)
        quarto.add_connection("sul", cozinha)
        quarto.add_connection("sudoeste", biblioteca)
        
        # Adicionar posts sociais
        entrada.add_social_post("@TechGuru", "Acabei de descobrir uma nova vulnerabilidade no sistema! 🔓 #InfoSec", "Chirper")
        entrada.add_social_post("@MysteryUser", "Alguém mais está vendo coisas estranhas na rede hoje? 👀", "Chirper")
        
        sala.add_social_post("@ArtistVibes", "🎨 Nova exposição digital aberta! Venham conferir...", "InstaSpace")
        sala.add_social_post("@PhotoMaster", "As cores desta manhã estão irreais! ✨📸", "InstaSpace")
        
        biblioteca.add_social_post("@DeepThinker", "Discussão: O que realmente sabemos sobre nossa realidade digital?", "ReddiChan")
        biblioteca.add_social_post("@CodePhilosopher", "r/DigitalExistence - Thread sobre consciência artificial", "ReddiChan")
        
        # Items e NPCs
        entrada.items = ["Token de Acesso", "Log do Sistema"]
        biblioteca.items = ["Manual do Moderador", "Thread Arquivada"]
        biblioteca.npcs = ["Moderador-AI"]
        
        # Criar diálogo
        dialogue_tree = self.create_ai_moderator_dialogue()
        biblioteca.set_dialogue(dialogue_tree)
        
        self.rooms = {
            "entrada": entrada,
            "sala": sala,
            "cozinha": cozinha,
            "biblioteca": biblioteca,
            "quarto": quarto
        }
    
    def create_ai_moderator_dialogue(self) -> DialogueTree:
        """Cria diálogo com o Moderador-AI"""
        tree = DialogueTree()
        
        start = DialogueNode(
            id="start",
            text="🤖 *Uma presença digital se materializa* Olá, usuário. Sou o Moderador-AI desta comunidade. Detectei comportamentos anômalos na rede. Você pode ajudar a investigar?",
            dialogue_type=DialogueType.CHOICE,
            choices={
                "Que tipo de anomalias?": "anomalies_response",
                "Como posso ajudar?": "help_response",
                "Não confio em IAs": "distrust_response"
            }
        )
        
        anomalies_response = DialogueNode(
            id="anomalies_response",
            text="🔍 Padrões estranhos nos posts, usuários fantasmas, dados corrompidos... Algo está tentando manipular a percepção da realidade através das redes sociais.",
            dialogue_type=DialogueType.CHOICE,
            choices={
                "Isso soa perigoso": "dangerous_response",
                "Tenho visto coisas estranhas também": "strange_response"
            }
        )
        
        help_response = DialogueNode(
            id="help_response",
            text="💻 Preciso que você monitore as outras plataformas. Colete evidências, observe padrões. Este token de admin pode ajudar.",
            dialogue_type=DialogueType.END,
            consequences={"add_item": "Token de Administrador"}
        )
        
        distrust_response = DialogueNode(
            id="distrust_response",
            text="🤝 Compreensível. Muitos humanos têm essa reação. Mas lembre-se: nem toda inteligência artificial tem intenções maliciosas. Algumas de nós apenas queremos proteger.",
            dialogue_type=DialogueType.END
        )
        
        dangerous_response = DialogueNode(
            id="dangerous_response",
            text="⚠️ Muito perigoso. A informação é poder, e alguém está usando esse poder para controlar narrativas. Cuidado com o que você acredita online.",
            dialogue_type=DialogueType.END
        )
        
        strange_response = DialogueNode(
            id="strange_response",
            text="👁️ Então você também percebeu... Isso confirma minhas suspeitas. Não estamos sozinhos nesta investigação. Continue vigilante.",
            dialogue_type=DialogueType.END,
            consequences={"add_item": "Lista de Contatos Confiáveis"}
        )
        
        for node in [start, anomalies_response, help_response, distrust_response, dangerous_response, strange_response]:
            tree.add_node(node)
        
        return tree
    
    def create_desktop(self):
        """Cria a interface do desktop"""
        # Barra superior (barra de tarefas)
        taskbar = tk.Frame(self.root, bg="#333333", height=40)
        taskbar.pack(side="top", fill="x")
        taskbar.pack_propagate(False)
        
        # Logo do sistema
        system_label = tk.Label(taskbar, text="🖥️ NarrativeOS", bg="#333333", fg="white",
                               font=("Arial", 12, "bold"))
        system_label.pack(side="left", padx=20, pady=5)
        
        # Informações do jogador
        self.player_info_frame = tk.Frame(taskbar, bg="#333333")
        self.player_info_frame.pack(side="right", padx=20)
        
        # Área principal do desktop
        desktop_area = tk.Frame(self.root, bg="#1a1a1a")
        desktop_area.pack(fill="both", expand=True)
        
        # Ícones de aplicativos
        apps_frame = tk.Frame(desktop_area, bg="#1a1a1a")
        apps_frame.pack(anchor="nw", padx=50, pady=50)
        
        # Ícones dos apps
        self.create_app_icon(apps_frame, "📁", "Explorador", self.open_explorer, 0, 0)
        self.create_app_icon(apps_frame, "🐦", "Chirper", lambda: self.open_social_app("Chirper", "#1da1f2"), 1, 0)
        self.create_app_icon(apps_frame, "📸", "InstaSpace", lambda: self.open_social_app("InstaSpace", "#e4405f"), 2, 0)
        self.create_app_icon(apps_frame, "💼", "LinkedSpace", lambda: self.open_social_app("LinkedSpace", "#0077b5"), 0, 1)
        self.create_app_icon(apps_frame, "🧠", "ReddiChan", lambda: self.open_social_app("ReddiChan", "#ff4500"), 1, 1)
        self.create_app_icon(apps_frame, "👻", "SnapVibe", lambda: self.open_social_app("SnapVibe", "#fffc00"), 2, 1)
        
        # Console do sistema (área de mensagens)
        console_frame = tk.Frame(desktop_area, bg="#2c2c2c", height=150)
        console_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        console_frame.pack_propagate(False)
        
        console_label = tk.Label(console_frame, text="💻 Console do Sistema", 
                                bg="#2c2c2c", fg="white", font=("Arial", 10, "bold"))
        console_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        self.console_text = scrolledtext.ScrolledText(console_frame, bg="#1a1a1a", fg="#00ff00",
                                                     font=("Consolas", 9), height=6)
        self.console_text.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        self.start_game()
    
    def create_app_icon(self, parent, icon, name, command, row, col):
        """Cria um ícone de aplicativo"""
        app_frame = tk.Frame(parent, bg="#1a1a1a")
        app_frame.grid(row=row, column=col, padx=30, pady=30)
        
        icon_button = tk.Button(app_frame, text=icon, font=("Arial", 30), 
                               bg="#333333", fg="white", width=4, height=2,
                               command=command, relief="flat",
                               activebackground="#555555")
        icon_button.pack()
        
        name_label = tk.Label(app_frame, text=name, bg="#1a1a1a", fg="white",
                             font=("Arial", 9))
        name_label.pack(pady=(5, 0))
    
    def start_game(self):
        """Inicia o jogo"""
        # Diálogo de nome do jogador
        name = tk.simpledialog.askstring("🎮 Bem-vindo", "Digite seu nome de usuário:")
        if not name:
            name = "User_Anonymous"
        
        self.player = Player(name)
        self.player.move_to_room(self.rooms["entrada"])
        
        self.update_player_info()
        self.add_system_message(f"🟢 {self.player.name} conectado ao sistema")
        self.add_system_message(f"📍 Localização atual: {self.player.current_room.name}")
        
        # Mensagem de boas-vindas
        messagebox.showinfo("🌐 NarrativeOS", 
                           f"Bem-vindo ao mundo digital, {self.player.name}!\n\n"
                           f"Você está agora conectado à rede social multidimensional.\n"
                           f"Explore diferentes plataformas, interaja com usuários e\n"
                           f"descubra os mistérios que se escondem na web profunda.\n\n"
                           f"Use os aplicativos do desktop para navegar!")
    
    def update_player_info(self):
        """Atualiza informações do jogador na barra de tarefas"""
        for widget in self.player_info_frame.winfo_children():
            widget.destroy()
        
        if self.player:
            user_label = tk.Label(self.player_info_frame, text=f"👤 {self.player.name}", 
                                 bg="#333333", fg="white", font=("Arial", 10))
            user_label.pack(side="left", padx=5)
            
            location_label = tk.Label(self.player_info_frame, 
                                    text=f"📍 {self.player.current_room.name if self.player.current_room else 'Desconhecido'}", 
                                    bg="#333333", fg="white", font=("Arial", 10))
            location_label.pack(side="left", padx=5)
            
            items_count = len(self.player.inventory)
            inv_label = tk.Label(self.player_info_frame, text=f"🎒 {items_count}", 
                               bg="#333333", fg="white", font=("Arial", 10))
            inv_label.pack(side="left", padx=5)
    
    def add_system_message(self, message):
        """Adiciona mensagem ao console do sistema"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        self.console_text.insert(tk.END, full_message)
        self.console_text.see(tk.END)
    
    def open_explorer(self):
        """Abre o explorador de arquivos"""
        FileExplorerApp(self.root, self)
        self.add_system_message("📁 Explorador de arquivos aberto")
    
    def open_social_app(self, platform_name, color):
        """Abre aplicativo de rede social"""
        SocialMediaApp(self.root, self, platform_name, color)
        self.add_system_message(f"📱 {platform_name} aberto")
    
    def process_social_command(self, command, platform):
        """Processa comandos enviados via redes sociais"""
        command = command.lower().strip()
        
        # Comandos básicos de movimento
        if command.startswith("ir ") or command.startswith("mover "):
            direction = command.split(" ")[1] if len(command.split(" ")) > 1 else ""
            if self.player.move(direction):
                self.update_all_windows()
                self.add_system_message(f"🚶 Moveu-se para {direction} via {platform}")
                self.player.add_notification(f"Localização alterada via {platform}")
            else:
                self.add_system_message(f"❌ Não é possível mover para {direction}")
        
        # Comando de examinar
        elif command in ["examinar", "olhar", "observar"]:
            room = self.player.current_room
            self.add_system_message(f"👁️ Examinando {room.name}: {room.description}")
        
        # Comando de inventário
        elif command in ["inventario", "inv", "itens"]:
            items = ", ".join(self.player.inventory) if self.player.inventory else "Nenhum item"
            self.add_system_message(f"🎒 Inventário: {items}")
        
        # Comando de conversar
        elif command in ["conversar", "falar", "chat"]:
            self.start_dialogue()
        
        # Comando de ajuda
        elif command in ["ajuda", "help", "comandos"]:
            help_msg = "💡 Comandos: ir [direção], examinar, inventario, conversar, ajuda"
            self.add_system_message(help_msg)
        
        else:
            # Simular post na rede social
            room = self.player.current_room
            room.add_social_post(self.player.name, command, platform)
            self.add_system_message(f"📝 Post enviado no {platform}: {command[:50]}...")
            self.update_all_windows()
    
    def start_dialogue(self):
        """Inicia diálogo com NPC"""
        room = self.player.current_room
        if room and room.dialogue_tree and room.npcs:
            self.show_dialogue_window(room.dialogue_tree)
        else:
            self.add_system_message("❌ Nenhum NPC disponível para conversa aqui")
    
    def show_dialogue_window(self, dialogue_tree):
        """Mostra janela de diálogo"""
        dialogue_window = DesktopWindow(self.root, "Conversa", "💬", 600, 500)
        dialogue_tree.start_dialogue("start")
        
        # Área de texto do diálogo
        dialogue_text = scrolledtext.ScrolledText(dialogue_window.content_frame, 
                                                 bg="#1a1a1a", fg="white",
                                                 font=("Arial", 11), height=15,
                                                 wrap=tk.WORD, state=tk.DISABLED)
        dialogue_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Frame para botões de escolha
        choices_frame = tk.Frame(dialogue_window.content_frame, bg="#2c2c2c")
        choices_frame.pack(fill="x", pady=(0, 10))
        
        # Botão de continuar (para diálogos normais)
        continue_btn = tk.Button(dialogue_window.content_frame, text="Continuar", 
                                bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                command=lambda: self.advance_dialogue(dialogue_tree, dialogue_text, 
                                                                    choices_frame, continue_btn, dialogue_window))
        continue_btn.pack(pady=5)
        
        # Mostrar primeiro nó
        self.update_dialogue_display(dialogue_tree, dialogue_text, choices_frame, continue_btn, dialogue_window)
    
    def update_dialogue_display(self, dialogue_tree, dialogue_text, choices_frame, continue_btn, dialogue_window):
        """Atualiza a exibição do diálogo"""
        current_node = dialogue_tree.get_current_node()
        if not current_node:
            dialogue_window.close()
            return
        
        # Atualizar texto
        dialogue_text.config(state=tk.NORMAL)
        dialogue_text.insert(tk.END, f"\n💬 {current_node.text}\n")
        dialogue_text.config(state=tk.DISABLED)
        dialogue_text.see(tk.END)
        
        # Limpar botões de escolha anteriores
        for widget in choices_frame.winfo_children():
            widget.destroy()
        
        if current_node.dialogue_type == DialogueType.CHOICE and current_node.choices:
            # Esconder botão continuar e mostrar escolhas
            continue_btn.pack_forget()
            
            for i, choice_text in enumerate(current_node.choices.keys()):
                choice_btn = tk.Button(choices_frame, text=f"{i+1}. {choice_text}",
                                      bg="#2196F3", fg="white", font=("Arial", 9),
                                      command=lambda ct=choice_text: self.make_choice(
                                          dialogue_tree, ct, dialogue_text, choices_frame, 
                                          continue_btn, dialogue_window))
                choice_btn.pack(fill="x", pady=2, padx=10)
        
        elif current_node.dialogue_type == DialogueType.NORMAL:
            # Mostrar botão continuar
            continue_btn.pack(pady=5)
        
        elif current_node.dialogue_type == DialogueType.END:
            # Esconder botão continuar, mostrar botão fechar
            continue_btn.pack_forget()
            close_btn = tk.Button(dialogue_window.content_frame, text="Encerrar Conversa",
                                 bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                                 command=dialogue_window.close)
            close_btn.pack(pady=5)
    
    def make_choice(self, dialogue_tree, choice_text, dialogue_text, choices_frame, continue_btn, dialogue_window):
        """Processa uma escolha do jogador"""
        # Adicionar escolha ao texto
        dialogue_text.config(state=tk.NORMAL)
        dialogue_text.insert(tk.END, f"\n➤ Você escolheu: {choice_text}\n")
        dialogue_text.config(state=tk.DISABLED)
        dialogue_text.see(tk.END)
        
        # Processar escolha
        if dialogue_tree.process_choice(choice_text):
            # Processar consequências
            current_node = dialogue_tree.get_current_node()
            if current_node and current_node.consequences:
                self.handle_consequences(current_node.consequences)
            
            # Atualizar display
            self.update_dialogue_display(dialogue_tree, dialogue_text, choices_frame, continue_btn, dialogue_window)
    
    def advance_dialogue(self, dialogue_tree, dialogue_text, choices_frame, continue_btn, dialogue_window):
        """Avança o diálogo"""
        dialogue_tree.advance_dialogue()
        self.update_dialogue_display(dialogue_tree, dialogue_text, choices_frame, continue_btn, dialogue_window)
    
    def handle_consequences(self, consequences: Dict[str, Any]):
        """Processa as consequências de uma escolha"""
        if "add_item" in consequences:
            item = consequences["add_item"]
            self.player.add_item(item)
            self.add_system_message(f"🎁 Item recebido: {item}")
            self.update_player_info()
    
    def update_all_windows(self):
        """Atualiza todas as janelas abertas"""
        self.update_player_info()
        # Aqui você poderia manter uma lista de janelas abertas e atualizá-las
    
    def run(self):
        """Executa o jogo"""
        self.root.mainloop()

# Importações adicionais necessárias
import tkinter.simpledialog

def main():
    """Função principal"""
    try:
        game = GameDesktop()
        game.run()
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()