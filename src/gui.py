import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
import tkinter as tk
from tkinter import messagebox, font
from .game_logic import new_board, get_winner, is_board_full, make_move
from .ai import minimax_ai, random_ai, finds_winning_moves_ai, finds_winning_and_losing_moves_ai

AI_PLAYERS = {
    "Random AI": random_ai,
    "Winning AI": finds_winning_moves_ai,
    "Blocking AI": finds_winning_and_losing_moves_ai,
    "Perfect AI (minimax)": minimax_ai,
}

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-Нолики с ИИ")
        self.window.resizable(False, False)
        
        self.bg_color = "#2c3e50"
        self.btn_bg = "#ecf0f1"
        self.x_color = "#e74c3c"
        self.o_color = "#3498db"
        self.btn_font = ("Segoe UI", 28, "bold")
        self.status_font = ("Segoe UI", 12)
        
        self.window.configure(bg=self.bg_color)
        
        self.board = new_board()
        self.current_player = 'X'
        self.game_over = False
        
        self.mode = 'human_vs_ai'
        self.ai_player_x = None
        self.ai_player_o = minimax_ai
        
        self.create_widgets()
        self.create_menu()
        
    def create_widgets(self):
        self.board_frame = tk.Frame(self.window, bg=self.bg_color)
        self.board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text='',
                    font=self.btn_font,
                    width=4,
                    height=2,
                    bg=self.btn_bg,
                    activebackground="#bdc3c7",
                    relief=tk.RAISED,
                    borderwidth=3,
                    command=lambda row=i, col=j: self.on_cell_click(row, col)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                # Привязываем события наведения
                btn.bind("<Enter>", lambda e, b=btn: self.on_enter(b))
                btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        self.status_label = tk.Label(
            self.window,
            text="Ваш ход (X)",
            font=self.status_font,
            bg=self.bg_color,
            fg="white"
        )
        self.status_label.pack(pady=10)
        
    def on_enter(self, button):
        if button.cget('text') == '':
            button.config(bg="#bdc3c7")
    
    def on_leave(self, button):
        if button.cget('text') == '':
            button.config(bg=self.btn_bg)
    
    def create_menu(self):
        menubar = tk.Menu(self.window, bg=self.bg_color, fg="white")
        self.window.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Игра", menu=game_menu)
        game_menu.add_command(label="Новая игра", command=self.reset_game)
        game_menu.add_separator()
        
        mode_menu = tk.Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="Режим", menu=mode_menu)
        mode_menu.add_command(label="Человек против человека", command=self.set_mode_human_human)
        mode_menu.add_command(label="Человек против ИИ", command=self.set_mode_human_vs_ai)
        mode_menu.add_command(label="ИИ против ИИ", command=self.set_mode_ai_vs_ai)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.window.quit)
        
        ai_menu_x = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Выбрать ИИ для X", menu=ai_menu_x)
        for name, func in AI_PLAYERS.items():
            ai_menu_x.add_command(label=name, command=lambda f=func: self.set_ai_player('X', f))
        
        ai_menu_o = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Выбрать ИИ для O", menu=ai_menu_o)
        for name, func in AI_PLAYERS.items():
            ai_menu_o.add_command(label=name, command=lambda f=func: self.set_ai_player('O', f))
    
    def set_ai_player(self, player, ai_func):
        if player == 'X':
            self.ai_player_x = ai_func
        else:
            self.ai_player_o = ai_func
        messagebox.showinfo("ИИ выбран", f"Для {player} выбран {ai_func.__name__}")
        self.reset_game()
    
    def set_mode_human_vs_ai(self):
        self.mode = 'human_vs_ai'
        self.ai_player_x = None
        if self.ai_player_o is None:
            self.ai_player_o = minimax_ai
        self.reset_game()
    
    def set_mode_human_human(self):
        self.mode = 'human_vs_human'
        self.ai_player_x = None
        self.ai_player_o = None
        self.reset_game()
    
    def set_mode_ai_vs_ai(self):
        self.mode = 'ai_vs_ai'
        if self.ai_player_x is None:
            self.ai_player_x = minimax_ai
        if self.ai_player_o is None:
            self.ai_player_o = random_ai
        self.reset_game()
        self.window.after(500, self.ai_move)
    
    def reset_game(self):
        self.board = new_board()
        self.current_player = 'X'
        self.game_over = False
        self.update_board_ui()
        self.status_label.config(text=f"Ход {self.current_player}" + (" (ИИ)" if self.is_ai(self.current_player) else " (человек)"))
        if self.mode == 'ai_vs_ai' and not self.game_over:
            self.window.after(500, self.ai_move)
    
    def is_ai(self, player):
        return (player == 'X' and self.ai_player_x is not None) or (player == 'O' and self.ai_player_o is not None)
    
    def get_ai_func(self, player):
        return self.ai_player_x if player == 'X' else self.ai_player_o
    
    def on_cell_click(self, row, col):
        if self.game_over:
            return
        if self.board[row][col] is not None:
            messagebox.showwarning("Неверный ход", "Клетка уже занята!")
            return
        if self.is_ai(self.current_player):
            return
        self.make_human_move(row, col)
    
    def make_human_move(self, row, col):
        make_move(self.board, (col, row), self.current_player)
        self.update_board_ui()
        if self.check_game_over():
            return
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_label.config(text=f"Ход {self.current_player}" + (" (ИИ)" if self.is_ai(self.current_player) else " (человек)"))
        if not self.game_over and self.is_ai(self.current_player):
            self.window.after(300, self.ai_move)
    
    def ai_move(self):
        if self.game_over:
            return
        ai_func = self.get_ai_func(self.current_player)
        if ai_func is None:
            return
        move = ai_func(self.board, self.current_player)
        if move is None:
            return
        x, y = move
        if self.board[y][x] is not None:
            return
        make_move(self.board, (x, y), self.current_player)
        self.update_board_ui()
        if self.check_game_over():
            return
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_label.config(text=f"Ход {self.current_player}" + (" (ИИ)" if self.is_ai(self.current_player) else " (человек)"))
        if self.mode == 'ai_vs_ai' and not self.game_over:
            self.window.after(400, self.ai_move)
    
    def check_game_over(self):
        winner = get_winner(self.board)
        if winner:
            self.end_game(f"Победитель: {winner}!")
            return True
        if is_board_full(self.board):
            self.end_game("Ничья!")
            return True
        return False
    
    def update_board_ui(self):
        for i in range(3):
            for j in range(3):
                val = self.board[i][j]
                text = val if val is not None else ''
                # Устанавливаем цвет текста в зависимости от фигуры
                if val == 'X':
                    fg = self.x_color
                elif val == 'O':
                    fg = self.o_color
                else:
                    fg = "black"
                self.buttons[i][j].config(text=text, fg=fg, bg=self.btn_bg)
    
    def end_game(self, message):
        self.game_over = True
        self.status_label.config(text=message)
        messagebox.showinfo("Игра окончена", message)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()