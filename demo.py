# -*- coding: utf-8 -*-
# Jogo de Aventura em Texto com Sistema de Diálogo e Cômodos Interativos

# @nicholascode-hub prodnc777@gmail.com

import os
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

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
    choices: Optional[Dict[str, str]] = None  # {texto_escolha: proximo_no_id}
    next_node: Optional[str] = None
    consequences: Optional[Dict[str, Any]] = None  # Efeitos da escolha

class DialogueTree:
    """Sistema de árvore de diálogos"""
    def __init__(self):
        self.nodes: Dict[str, DialogueNode] = {}
        self.current_node: Optional[str] = None
        self.dialogue_history: List[str] = []
    
    def add_node(self, node: DialogueNode):
        """Adiciona um nó à árvore"""
        self.nodes[node.id] = node
    
    def start_dialogue(self, start_node_id: str):
        """Inicia um diálogo"""
        if start_node_id in self.nodes:
            self.current_node = start_node_id
            return True
        return False
    
    def get_current_node(self) -> Optional[DialogueNode]:
        """Retorna o nó atual"""
        if self.current_node:
            return self.nodes.get(self.current_node)
        return None
    
    def process_choice(self, choice_key: str) -> bool:
        """Processa uma escolha do jogador"""
        current = self.get_current_node()
        if current and current.choices and choice_key in current.choices:
            self.dialogue_history.append(f"Escolha: {choice_key}")
            self.current_node = current.choices[choice_key]
            return True
        return False
    
    def advance_dialogue(self):
        """Avança para o próximo nó (diálogos lineares)"""
        current = self.get_current_node()
        if current and current.next_node:
            self.current_node = current.next_node

class Room:
    """Representa um cômodo do jogo"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.connections: Dict[str, 'Room'] = {}  # direção -> cômodo
        self.dialogue_tree: Optional[DialogueTree] = None
        self.visited = False
        self.items: List[str] = []
        self.npcs: List[str] = []
    
    def add_connection(self, direction: str, room: 'Room'):
        """Adiciona uma conexão com outro cômodo"""
        self.connections[direction] = room
    
    def get_available_directions(self) -> List[str]:
        """Retorna as direções disponíveis"""
        return list(self.connections.keys())
    
    def set_dialogue(self, dialogue_tree: DialogueTree):
        """Define o diálogo do cômodo"""
        self.dialogue_tree = dialogue_tree
    
    def enter(self):
        """Marca o cômodo como visitado"""
        self.visited = True

class Player:
    """Representa o jogador"""
    def __init__(self, name: str):
        self.name = name
        self.current_room: Optional[Room] = None
        self.inventory: List[str] = []
        self.health = 100
        self.game_flags: Dict[str, Any] = {}  # Para controlar o estado do jogo
    
    def move_to_room(self, room: Room):
        """Move o jogador para um cômodo"""
        self.current_room = room
        room.enter()
    
    def move(self, direction: str) -> bool:
        """Tenta mover o jogador em uma direção"""
        if self.current_room and direction in self.current_room.connections:
            new_room = self.current_room.connections[direction]
            self.move_to_room(new_room)
            return True
        return False
    
    def add_item(self, item: str):
        """Adiciona um item ao inventário"""
        self.inventory.append(item)
    
    def has_item(self, item: str) -> bool:
        """Verifica se o jogador possui um item"""
        return item in self.inventory

class GameInterface:
    """Interface do jogo"""
    def __init__(self):
        self.running = True
    
    def clear_screen(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_text(self, text: str, delay: float = 0.03):
        """Exibe texto com efeito de digitação"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def display_room(self, room: Room):
        """Exibe informações do cômodo atual"""
        print("=" * 60)
        print(f"📍 {room.name}")
        print("=" * 60)
        self.display_text(room.description)
        
        if room.items:
            print(f"\n🔍 Você vê: {', '.join(room.items)}")
        
        if room.npcs:
            print(f"\n👥 Pessoas presentes: {', '.join(room.npcs)}")
        
        directions = room.get_available_directions()
        if directions:
            print(f"\n🚪 Saídas disponíveis: {', '.join(directions)}")
        
        print()
    
    def display_dialogue(self, node: DialogueNode):
        """Exibe um nó de diálogo"""
        print("\n" + "─" * 50)
        self.display_text(f"💬 {node.text}")
        
        if node.dialogue_type == DialogueType.CHOICE and node.choices:
            print("\nEscolhas:")
            for i, choice in enumerate(node.choices.keys(), 1):
                print(f"  {i}. {choice}")
        
        print("─" * 50)
    
    def get_user_input(self, prompt: str = "> ") -> str:
        """Obtém entrada do usuário"""
        return input(prompt).strip().lower()
    
    def display_help(self):
        """Exibe ajuda do jogo"""
        print("\n" + "=" * 60)
        print("🎮 COMANDOS DISPONÍVEIS")
        print("=" * 60)
        print("• mover [direção] ou ir [direção] - Move para outra sala")
        print("• examinar ou olhar - Examina o ambiente atual")
        print("• conversar ou falar - Inicia diálogo (se disponível)")
        print("• inventario ou inv - Mostra seu inventário")
        print("• mapa - Mostra salas visitadas")
        print("• ajuda ou help - Mostra esta ajuda")
        print("• sair ou quit - Sai do jogo")
        print("=" * 60)
    
    def display_inventory(self, player: Player):
        """Exibe o inventário do jogador"""
        print(f"\n🎒 Inventário de {player.name}:")
        if player.inventory:
            for item in player.inventory:
                print(f"  • {item}")
        else:
            print("  Vazio")
    
    def display_status(self, player: Player):
        """Exibe status do jogador"""
        print(f"\n❤️ Vida: {player.health}/100")

class Game:
    """Classe principal do jogo"""
    def __init__(self):
        self.interface = GameInterface()
        self.player = None
        self.rooms: Dict[str, Room] = {}
        self.game_state = "menu"
        self.setup_game()
    
    def setup_game(self):
        """Configura o mundo do jogo"""
        # Criar cômodos
        entrada = Room("Entrada da Mansão", 
                      "Você está na entrada de uma mansão antiga. O ar está pesado e há um cheiro de mofo. "
                      "Quadros antigos adornam as paredes e um lustre empoeirado pende do teto alto.")
        
        sala = Room("Sala de Estar",
                   "Uma sala ampla com móveis cobertos por lençóis brancos. Uma lareira apagada domina uma das paredes. "
                   "Livros estão espalhados pelo chão e há pegadas na poeira.")
        
        cozinha = Room("Cozinha",
                      "A cozinha está em desordem. Pratos sujos se acumulam na pia e há uma panela ainda no fogão. "
                      "Uma porta dos fundos está entreaberta, deixando entrar uma brisa fria.")
        
        biblioteca = Room("Biblioteca",
                         "Estantes altíssimas repletas de livros antigos. Uma escada de madeira dá acesso aos volumes superiores. "
                         "Uma mesa de estudos está coberta de papéis e há uma caneta ainda com tinta fresca.")
        
        quarto = Room("Quarto Principal",
                     "Um quarto elegante mas abandonado. A cama está desfeita e roupas estão jogadas no chão. "
                     "Uma janela oferece vista para um jardim selvagem.")
        
        # Adicionar conexões entre cômodos
        entrada.add_connection("norte", sala)
        entrada.add_connection("leste", cozinha)
        
        sala.add_connection("sul", entrada)
        sala.add_connection("leste", biblioteca)
        sala.add_connection("norte", quarto)
        
        cozinha.add_connection("oeste", entrada)
        cozinha.add_connection("norte", biblioteca)
        
        biblioteca.add_connection("oeste", sala)
        biblioteca.add_connection("sul", cozinha)
        biblioteca.add_connection("norte", quarto)
        
        quarto.add_connection("sul", sala)
        quarto.add_connection("leste", biblioteca)
        
        # Adicionar itens aos cômodos
        entrada.items = ["chave enferrujada", "retrato rasgado"]
        biblioteca.items = ["livro misterioso", "carta antiga"]
        cozinha.items = ["faca de cozinha"]
        
        # Adicionar NPCs
        biblioteca.npcs = ["Bibliotecário Fantasma"]
        
        # Criar diálogo para a biblioteca
        dialogue_tree = self.create_library_dialogue()
        biblioteca.set_dialogue(dialogue_tree)
        
        # Registrar cômodos
        self.rooms = {
            "entrada": entrada,
            "sala": sala,
            "cozinha": cozinha,
            "biblioteca": biblioteca,
            "quarto": quarto
        }
    
    def create_library_dialogue(self) -> DialogueTree:
        """Cria o diálogo da biblioteca"""
        tree = DialogueTree()
        
        # Nó inicial
        start = DialogueNode(
            id="start",
            text="Uma figura etérea aparece entre as estantes... 'Bem-vindo, viajante. Há muito tempo ninguém visita esta biblioteca. O que você busca?'",
            dialogue_type=DialogueType.CHOICE,
            choices={
                "Estou explorando a mansão": "explore_response",
                "Procuro por respostas": "answers_response",
                "Quem é você?": "identity_response"
            }
        )
        
        # Respostas às escolhas
        explore_response = DialogueNode(
            id="explore_response",
            text="'Ah, um explorador... Esta mansão guarda muitos segredos. Cuidado com o que procura, pois nem tudo que se encontra deveria ser encontrado.'",
            dialogue_type=DialogueType.CHOICE,
            choices={
                "Que tipo de segredos?": "secrets_response",
                "Não tenho medo": "brave_response"
            }
        )
        
        answers_response = DialogueNode(
            id="answers_response",
            text="'Respostas... sempre respostas. Mas você está fazendo as perguntas certas? Talvez devesse começar perguntando sobre esta mansão.'",
            dialogue_type=DialogueType.CHOICE,
            choices={
                "Me fale sobre a mansão": "mansion_response",
                "Que perguntas devo fazer?": "questions_response"
            }
        )
        
        identity_response = DialogueNode(
            id="identity_response",
            text="'Eu sou o guardião deste conhecimento, condenado a vagar entre estas páginas por toda eternidade. Meu nome se perdeu no tempo, mas meu propósito permanece.'",
            dialogue_type=DialogueType.NORMAL,
            next_node="purpose_explain"
        )
        
        # Nós secundários
        secrets_response = DialogueNode(
            id="secrets_response",
            text="'A família que vivia aqui desapareceu uma noite... Dizem que ainda vagam pelos corredores. O livro vermelho na estante superior tem mais detalhes.'",
            dialogue_type=DialogueType.END
        )
        
        brave_response = DialogueNode(
            id="brave_response",
            text="'Coragem é admirável, jovem. Mas lembre-se: coragem sem sabedoria é imprudência. Leve este amuleto... pode precisar.'",
            dialogue_type=DialogueType.END,
            consequences={"add_item": "amuleto protetor"}
        )
        
        mansion_response = DialogueNode(
            id="mansion_response",
            text="'Esta mansão pertencia aos Ravencroft. Uma família próspera até que a ganância os corrompeu. Agora suas almas estão presas aqui.'",
            dialogue_type=DialogueType.END
        )
        
        questions_response = DialogueNode(
            id="questions_response",
            text="'Pergunte sobre os Ravencroft. Pergunte sobre a noite em que desapareceram. Pergunte sobre o ritual que realizaram no porão...'",
            dialogue_type=DialogueType.END
        )
        
        purpose_explain = DialogueNode(
            id="purpose_explain",
            text="'Meu propósito é guiar aqueles que buscam a verdade. Mas cuidado... a verdade pode ser mais terrível do que a ignorância.'",
            dialogue_type=DialogueType.END
        )
        
        # Adicionar todos os nós à árvore
        for node in [start, explore_response, answers_response, identity_response, 
                    secrets_response, brave_response, mansion_response, 
                    questions_response, purpose_explain]:
            tree.add_node(node)
        
        return tree
    
    def start_game(self):
        """Inicia o jogo"""
        self.interface.clear_screen()
        print("🏚️" + "=" * 58 + "🏚️")
        print("     BEM-VINDO À MANSÃO DOS SEGREDOS PERDIDOS")
        print("🏚️" + "=" * 58 + "🏚️")
        
        self.interface.display_text(
            "\nVocê se encontra diante de uma mansão abandonada em uma noite tempestuosa. "
            "Relâmpagos iluminam as janelas quebradas e o vento uiva através das rachaduras nas paredes. "
            "Algo o trouxe até aqui... mas o quê?"
        )
        
        name = input("\n👤 Qual é o seu nome, corajoso explorador? ")
        if not name.strip():
            name = "Explorador Misterioso"
        
        self.player = Player(name)
        self.player.move_to_room(self.rooms["entrada"])
        
        self.interface.display_text(f"\nBem-vindo, {self.player.name}!")
        input("\nPressione ENTER para começar sua jornada...")
        
        self.game_loop()
    
    def game_loop(self):
        """Loop principal do jogo"""
        while self.interface.running:
            self.interface.clear_screen()
            
            # Exibir informações do cômodo atual
            if self.player.current_room:
                self.interface.display_room(self.player.current_room)
            
            # Obter comando do jogador
            command = self.interface.get_user_input(f"🎮 O que você faz, {self.player.name}? ")
            
            if command == "":
                continue
            
            # Processar comando
            self.process_command(command)
    
    def process_command(self, command: str):
        """Processa comandos do jogador"""
        parts = command.split()
        action = parts[0] if parts else ""
        
        if action in ["sair", "quit", "q"]:
            self.interface.display_text("\n👋 Obrigado por jogar! Até a próxima aventura!")
            self.interface.running = False
            
        elif action in ["ajuda", "help", "h"]:
            self.interface.display_help()
            input("\nPressione ENTER para continuar...")
            
        elif action in ["mover", "ir", "m"] and len(parts) > 1:
            direction = parts[1]
            self.move_player(direction)
            
        elif action in ["examinar", "olhar", "e"]:
            input("\nPressione ENTER para continuar...")
            
        elif action in ["conversar", "falar", "c"]:
            self.start_dialogue()
            
        elif action in ["inventario", "inv", "i"]:
            self.interface.display_inventory(self.player)
            input("\nPressione ENTER para continuar...")
            
        elif action in ["mapa", "map"]:
            self.show_map()
            input("\nPressione ENTER para continuar...")
            
        elif action in ["status", "vida"]:
            self.interface.display_status(self.player)
            input("\nPressione ENTER para continuar...")
            
        else:
            self.interface.display_text("❌ Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis.")
            input("\nPressione ENTER para continuar...")
    
    def move_player(self, direction: str):
        """Move o jogador"""
        if self.player.move(direction):
            self.interface.display_text(f"✅ Você se move para {direction}...")
            time.sleep(1)
        else:
            self.interface.display_text(f"❌ Não é possível ir para {direction} daqui.")
            input("\nPressione ENTER para continuar...")
    
    def start_dialogue(self):
        """Inicia diálogo no cômodo atual"""
        room = self.player.current_room
        if room and room.dialogue_tree and room.npcs:
            tree = room.dialogue_tree
            tree.start_dialogue("start")
            
            while tree.current_node:
                current_node = tree.get_current_node()
                if not current_node:
                    break
                
                self.interface.display_dialogue(current_node)
                
                if current_node.dialogue_type == DialogueType.CHOICE and current_node.choices:
                    choice_list = list(current_node.choices.keys())
                    try:
                        choice_num = int(input("\nEscolha (número): ")) - 1
                        if 0 <= choice_num < len(choice_list):
                            chosen_text = choice_list[choice_num]
                            tree.process_choice(chosen_text)
                            
                            # Processar consequências
                            if current_node.consequences:
                                self.handle_consequences(current_node.consequences)
                        else:
                            print("❌ Escolha inválida!")
                            continue
                    except ValueError:
                        print("❌ Por favor, digite um número!")
                        continue
                
                elif current_node.dialogue_type == DialogueType.NORMAL:
                    input("\nPressione ENTER para continuar...")
                    tree.advance_dialogue()
                
                elif current_node.dialogue_type == DialogueType.END:
                    input("\nPressione ENTER para terminar a conversa...")
                    break
            
            tree.current_node = None
        else:
            self.interface.display_text("❌ Não há ninguém para conversar aqui.")
            input("\nPressione ENTER para continuar...")
    
    def handle_consequences(self, consequences: Dict[str, Any]):
        """Processa as consequências de uma escolha"""
        if "add_item" in consequences:
            item = consequences["add_item"]
            self.player.add_item(item)
            self.interface.display_text(f"🎁 Você recebeu: {item}")
            time.sleep(1)
    
    def show_map(self):
        """Mostra o mapa de salas visitadas"""
        print("\n🗺️ MAPA - SALAS VISITADAS:")
        print("=" * 30)
        for name, room in self.rooms.items():
            status = "✅" if room.visited else "❓"
            print(f"{status} {room.name}")

def main():
    """Função principal"""
    try:
        game = Game()
        game.start_game()
    except KeyboardInterrupt:
        print("\n\n👋 Jogo interrompido. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("Por favor, reporte este erro!")

if __name__ == "__main__":
    main()