# game_manager.py
import tkinter as tk
from tkinter import messagebox
from game_board import GameBoard
from minimax_ai import MinimaxAI

class GameManager:
    """
    Gerencia o fluxo do jogo da velha, estados, placar, modos de jogo
    (Jogador vs. Jogador ou Jogador vs. IA com dificuldades) e
    interage com a interface do tabuleiro e a lógica da IA.
    """
    def __init__(self, master):
        self.master = master
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.player_scores = {'X': 0, 'O': 0}
        self.mode = None # 'vs_player' ou 'vs_ai'
        self.ai_difficulty = None # 'easy', 'medium', 'hard', 'impossible'

        self.ai = MinimaxAI('O', 'X') # IA joga como 'O', humano como 'X'

        self._setup_ui_elements() # Método para criar todos os widgets
        self.game_board = GameBoard(self.master, self)
        self.game_board.update_board(self.board)
        print(f"DEBUG: Jogo inicializado. Modo atual: {self.mode}") # DEBUG PRINT

    def _setup_ui_elements(self):
        """Inicializa e organiza todos os widgets da interface do usuário."""
        self.score_label = tk.Label(self.master, text="Placar: X - 0 | O - 0", font=('Arial', 18, 'bold'), pady=12, fg="#2C3E50")
        self.score_label.pack(side=tk.TOP) 

        mode_frame = tk.Frame(self.master, pady=10)
        mode_frame.pack(side=tk.TOP)
        tk.Label(mode_frame, text="Escolha o Modo:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(mode_frame, text="Jogador vs. Jogador", command=self.set_vs_player_mode, font=('Arial', 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(mode_frame, text="Jogador vs. IA", command=self._show_ai_difficulty_options, font=('Arial', 12), bg="#FFC107", fg="#2C3E50").pack(side=tk.LEFT, padx=5)

        self.ai_difficulty_frame = tk.Frame(self.master, pady=5, bg="#F0F0F0", relief="groove", bd=2) 
        
        spacer_frame = tk.Frame(self.ai_difficulty_frame, height=40, width=1, bg="#F0F0F0") # Altura desejada
        spacer_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=0, pady=0) # Pequeno dummy para forçar altura. Width=1 para ser pequeno.

        tk.Label(self.ai_difficulty_frame, text="Dificuldade da IA:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5, pady=5) 
        difficulties = {"Fácil": "easy", "Médio": "medium", "Difícil": "hard", "Impossível": "impossible"}
        colors = {"Fácil": "#BBDEFB", "Médio": "#FFF9C4", "Difícil": "#FFCDD2", "Impossível": "#D1C4E9"}
        for text, diff_level in difficulties.items():
            tk.Button(self.ai_difficulty_frame, text=text, command=lambda d=diff_level: self.set_vs_ai_mode(d),
                      font=('Arial', 10), bg=colors[text]).pack(side=tk.LEFT, padx=3, pady=5)
        
        self.ai_difficulty_frame.pack(side=tk.TOP, fill=tk.X, expand=False) 
        self.ai_difficulty_frame.pack_forget() 
        
        control_frame = tk.Frame(self.master, pady=15)
        control_frame.pack(side=tk.TOP)
        tk.Button(control_frame, text="Reiniciar Partida", command=self.reset_game, font=('Arial', 12), bg="#90CAF9", fg="black").pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Novo Jogo", command=self.start_new_game, font=('Arial', 12), bg="#B2DFDB", fg="black").pack(side=tk.LEFT, padx=10)

    def _show_ai_difficulty_options(self):
        """Exibe as opções de dificuldade da IA e informa o modo selecionado."""
        print("DEBUG: _show_ai_difficulty_options foi chamado.") 
        self.ai_difficulty_frame.pack(side=tk.TOP, fill=tk.X, expand=False) 
        self.master.update_idletasks() 

        frame_width = self.ai_difficulty_frame.winfo_width()
        frame_height = self.ai_difficulty_frame.winfo_height()
        print(f"DEBUG: Dimensões do ai_difficulty_frame após pack: Largura={frame_width}, Altura={frame_height}")

        self.master.after(100, lambda: messagebox.showinfo("Modo de Jogo", "Modo: Jogador vs. IA. Agora, escolha a dificuldade."))
        print("DEBUG: ai_difficulty_frame.pack() executado e messagebox agendado.")

    def set_vs_player_mode(self):
        """Configura o jogo para o modo Jogador vs. Jogador."""
        self.mode = 'vs_player'
        self.ai_difficulty_frame.pack_forget() 
        print("DEBUG: Modo definido para 'vs_player'. Frame de dificuldade oculto.") 
        messagebox.showinfo("Modo Selecionado", "Pronto! Jogo: Jogador vs. Jogador.")
        self.start_new_game() 

    def set_vs_ai_mode(self, difficulty):
        """Configura o jogo para o modo Jogador vs. IA com a dificuldade especificada."""
        self.mode = 'vs_ai'
        self.ai_difficulty = difficulty
        self.ai_difficulty_frame.pack_forget() 
        print(f"DEBUG: Modo definido para 'vs_ai' com dificuldade '{difficulty}'. Frame de dificuldade oculto.") 
        messagebox.showinfo("Modo Selecionado", f"Pronto! Jogo: Jogador vs. IA ({difficulty.capitalize()}).")
        self.start_new_game() 

    def make_move(self, row, col):
        """Processa a jogada de um jogador humano."""
        print(f"DEBUG: make_move chamado. Modo atual: {self.mode}") 
        if not self.mode:
            messagebox.showwarning("Atenção", "Por favor, escolha um modo de jogo antes de começar.")
            return

        if self.board[row][col] == ' ' and not self.game_over:
            self._execute_move(row, col, self.current_player)
            self.check_game_status()

            if not self.game_over:
                self.switch_player()
                if self.mode == 'vs_ai' and self.current_player == self.ai.ai_player:
                    self.master.after(700, self._initiate_ai_turn) 

    def _execute_move(self, row, col, player):
        """Executa uma jogada no tabuleiro e atualiza a interface."""
        self.board[row][col] = player
        self.game_board.update_board(self.board)

    def _initiate_ai_turn(self):
        """Inicia o turno da IA e executa sua jogada."""
        if not self.game_over:
            ai_choice = self.ai.find_best_move(self.board, self.ai_difficulty)
            if ai_choice:
                self._execute_move(ai_choice[0], ai_choice[1], self.ai.ai_player)
                self.check_game_status()
                if not self.game_over:
                    self.switch_player()

    def switch_player(self):
        """Alterna o jogador atual."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_game_status(self):
        """Verifica o status do jogo (vitória ou empate) e atualiza a UI."""
        winner, cells = self.check_winner()
        if winner:
            self.game_over = True
            self.player_scores[winner] += 1
            self.update_score_display()
            self.game_board.highlight_winner(cells)
            messagebox.showinfo("Fim da Rodada!", f"Parabéns! O jogador '{winner}' venceu a rodada!")
            self.game_board.disable_board()
        elif self.is_board_full():
            self.game_over = True
            messagebox.showinfo("Fim da Rodada!", "A rodada terminou em empate!")
            self.game_board.disable_board()

    def check_winner(self):
        """Identifica se há um vencedor e retorna o caractere e as células da vitória."""
        lines = []
        # Linhas
        for r in range(3):
            lines.append([(r, c) for c in range(3)])
        # Colunas
        for c in range(3):
            lines.append([(r, c) for r in range(3)])
        # Diagonais
        lines.append([(i, i) for i in range(3)])
        lines.append([(i, 2 - i) for i in range(3)])

        for line_coords in lines:
            char1, char2, char3 = [self.board[r][c] for r, c in line_coords]
            if char1 != ' ' and char1 == char2 == char3:
                return char1, line_coords
        return None, []

    def is_board_full(self):
        """Verifica se o tabuleiro está completamente preenchido."""
        return all(self.board[r][c] != ' ' for r in range(3) for c in range(3))

    def reset_game(self):
        """Reinicia a partida atual (mantém o placar)."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.current_player = 'X'
        self.game_board.reset_board_ui()
        self.game_board.update_board(self.board) 
        if self.mode == 'vs_ai' and self.current_player == self.ai.ai_player:
            self.master.after(700, self._initiate_ai_turn)

    def start_new_game(self):
        """Inicia um novo jogo do zero (zera o placar)."""
        self.player_scores = {'X': 0, 'O': 0}
        self.update_score_display()
        self.reset_game()
