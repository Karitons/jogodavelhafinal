# minimax_ai.py
import math

class MinimaxAI:
    """
    Implementa uma IA para o jogo da velha usando o algoritmo Minimax,
    com diferentes níveis de dificuldade.
    """
    def __init__(self, ai_player, human_player):
        self.ai_player = ai_player
        self.human_player = human_player

    def find_best_move(self, board, difficulty):
        """
        Encontra a melhor jogada para a IA com base na dificuldade.
        'easy': Jogada aleatória.
        'medium': Combinação de minimax raso e aleatório.
        'hard': Minimax com profundidade limitada.
        'impossible': Minimax completo.
        """
        if difficulty == 'easy':
            return self._get_random_move(board)
        elif difficulty == 'medium':
            # Tenta uma jogada boa, mas pode cometer erros (não é um minimax completo)
            return self._minimax_move_partial(board, 2) or self._get_random_move(board)
        elif difficulty == 'hard':
            # Minimax com profundidade limitada para um desafio maior, mas não perfeito
            return self._minimax_move_partial(board, 4)
        elif difficulty == 'impossible':
            # Minimax completo para a jogada ótima
            return self._minimax_move_full(board)
        return None

    def _get_random_move(self, board):
        """Retorna uma jogada aleatória disponível."""
        empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
        if empty_cells:
            import random
            return random.choice(empty_cells)
        return None

    def _minimax_move_partial(self, board, depth_limit):
        """Executa o algoritmo Minimax com uma profundidade limitada."""
        best_score = -math.inf
        best_move = None
        
        # Cria uma cópia do jogo da velha para simular
        temp_board = [row[:] for row in board]

        for r in range(3):
            for c in range(3):
                if temp_board[r][c] == ' ':
                    temp_board[r][c] = self.ai_player
                    score = self._minimax(temp_board, 0, False, depth_limit)
                    temp_board[r][c] = ' ' # Desfaz a jogada

                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_move

    def _minimax_move_full(self, board):
        """Executa o algoritmo Minimax completo para encontrar a melhor jogada."""
        best_score = -math.inf
        best_move = None
        
        # Cria uma cópia do jogo da velha para simular
        temp_board = [row[:] for row in board]

        for r in range(3):
            for c in range(3):
                if temp_board[r][c] == ' ':
                    temp_board[r][c] = self.ai_player
                    score = self._minimax(temp_board, 0, False)
                    temp_board[r][c] = ' ' # Desfaz a jogada

                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_move

    def _minimax(self, board, depth, is_maximizing_player, depth_limit=None):
        """
        Implementação recursiva do algoritmo Minimax.
        Retorna a pontuação da melhor jogada.
        """
        winner, _ = self._check_winner(board)
        if winner == self.ai_player:
            return 1 # IA vence
        elif winner == self.human_player:
            return -1 # eu venço
        elif self._is_board_full(board):
            return 0 # Empate

        if depth_limit is not None and depth >= depth_limit:
                        return 0 

        if is_maximizing_player:
            best_score = -math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = self.ai_player
                        score = self._minimax(board, depth + 1, False, depth_limit)
                        board[r][c] = ' '
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = self.human_player
                        score = self._minimax(board, depth + 1, True, depth_limit)
                        board[r][c] = ' '
                        best_score = min(best_score, score)
            return best_score

    def _check_winner(self, board):
        """Verifica se há um vencedor no tabuleiro."""
        # Verificar linhas, colunas e diagonais
        lines = []
        for i in range(3):
            lines.append(board[i]) # Linhas
            lines.append([board[0][i], board[1][i], board[2][i]]) # Colunas
        lines.append([board[0][0], board[1][1], board[2][2]]) # Diagonal principal
        lines.append([board[0][2], board[1][1], board[2][0]]) # Diagonal secundária

        for line in lines:
            if all(cell == 'X' for cell in line):
                return 'X', None
            if all(cell == 'O' for cell in line):
                return 'O', None
        return None, None

    def _is_board_full(self, board):
        """Verifica se o tabuleiro está cheio."""
        return all(cell != ' ' for row in board for cell in row)
