# game_board.py
import tkinter as tk

class GameBoard:
    """
    Representa a interface gráfica do tabuleiro do jogo da velha,
    lidando com a criação dos botões e a atualização visual.
    """
    def __init__(self, master, game_manager):
        self.master = master
        self.game_manager = game_manager
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self._create_board_ui()

    def _create_board_ui(self):
        """Cria e organiza os botões do tabuleiro na interface."""
        self.board_frame = tk.Frame(self.master, bg="#2C3E50", bd=5, relief="ridge")
        self.board_frame.pack(pady=20)

        for r in range(3):
            for c in range(3):
                button = tk.Button(self.board_frame, text=' ', font=('Arial', 40, 'bold'),
                                   width=4, height=2, bd=3, relief="raised",
                                   command=lambda row=r, col=c: self.game_manager.make_move(row, col))
                button.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = button

    def update_board(self, board_state):
        """Atualiza o texto dos botões do tabuleiro com o estado atual do jogo."""
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=board_state[r][c], fg="#ECF0F1")
                if board_state[r][c] == 'X':
                    self.buttons[r][c].config(fg="#E74C3C") # Vermelho para X
                elif board_state[r][c] == 'O':
                    self.buttons[r][c].config(fg="#3498DB") # Azul para O

    def highlight_winner(self, winning_cells):
        """Destaca as células que formam a linha de vitória."""
        for r, c in winning_cells:
            self.buttons[r][c].config(bg="#27AE60", fg="white") # Verde para células vencedoras

    def disable_board(self):
        """Desativa todos os botões do tabuleiro."""
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(state=tk.DISABLED)

    def reset_board_ui(self):
        """Reinicia a aparência dos botões do tabuleiro para um novo jogo."""
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=' ', state=tk.NORMAL, bg="SystemButtonFace") # Cor padrão do sistema
