#trabalho final do Professor Natan, Feito pelos Alunos: Kariton Silva, Izaque Gabriel

# main.py
import tkinter as tk
from game_manager import GameManager

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jogo da Velha")
    root.geometry("600x750") # Ajustado para possivelmente dar mais espaço
    root.resizable(False, False) # Evita que a janela seja redimensionada

    game_manager = GameManager(root)

    root.mainloop()
