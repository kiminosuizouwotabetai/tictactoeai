import sys
from ai import random_ai, finds_winning_moves_ai, finds_winning_and_losing_moves_ai, minimax_ai, minimax_ai_alpha_beta
from game_logic import get_winner, is_board_full

AI_FUNCTIONS = {
    'random_ai': random_ai,
    'winning_ai': finds_winning_moves_ai,
    'blocking_ai': finds_winning_and_losing_moves_ai,
    'minimax_ai': minimax_ai,
    'minimax_alpha_beta': minimax_ai_alpha_beta,
}

def new_board():
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]

def render(board):
    print("\n  0 1 2")
    for i, row in enumerate(board):
        print(f"{i} ", end="")
        for cell in row:
            symbol = cell if cell is not None else "."
            print(f" {symbol}", end="")
        print()
    print()

def get_move():
    while True:
        try:
            x = int(input("Введите X (0-2): "))
            y = int(input("Введите Y (0-2): "))
            return (x, y)
        except ValueError:
            print("Введите числа, пожалуйста.")

def make_move(board, move_coords, player):
    x, y = move_coords
    if board[y][x] is not None:
        print("Клетка занята! Пропускаем ход.")
        return False
    board[y][x] = player
    return True

def human_player(board, player):
    """Интерфейс для человека, соответствующий ИИ-функциям"""
    return get_move()

def play(player1_name, player2_name):
    """Сыграть одну партию между двумя ИИ, вернуть 0/1/2"""
    board = new_board()
    current_player = 'X'
    player1_func = AI_FUNCTIONS[player1_name]
    player2_func = AI_FUNCTIONS[player2_name]
    player_funcs = {'X': player1_func, 'O': player2_func}
    
    while True:
        move = player_funcs[current_player](board, current_player)
        if make_move(board, move, current_player):
            winner = get_winner(board)
            if winner == 'X':
                return 1
            elif winner == 'O':
                return 2
            if is_board_full(board):
                return 0
            current_player = 'O' if current_player == 'X' else 'X'

def repeated_battle(player1_name, player2_name, rounds=1000):
    """Провести rounds партий, вывести статистику побед и ничьих"""
    wins = {1: 0, 2: 0, 0: 0}
    for i in range(rounds):
        result = play(player1_name, player2_name)
        wins[result] += 1
        if (i+1) % 100 == 0:
            print(f"Сыграно {i+1} игр...")
    print("\n=== Статистика ===")
    print(f"{player1_name} побед: {wins[1]} ({wins[1]/rounds*100:.1f}%)")
    print(f"{player2_name} побед: {wins[2]} ({wins[2]/rounds*100:.1f}%)")
    print(f"Ничьих: {wins[0]} ({wins[0]/rounds*100:.1f}%)")

def main():
    if len(sys.argv) == 3:
        p1_name, p2_name = sys.argv[1], sys.argv[2]
        if p1_name not in AI_FUNCTIONS or p2_name not in AI_FUNCTIONS:
            print("Доступные ИИ:", list(AI_FUNCTIONS.keys()))
            return
        result = play(p1_name, p2_name)
        if result == 0:
            print("Ничья!")
        elif result == 1:
            print(f"Победил {p1_name}!")
        else:
            print(f"Победил {p2_name}!")
        return
    
    if len(sys.argv) == 4 and sys.argv[3].startswith('--battle'):
        p1_name, p2_name = sys.argv[1], sys.argv[2]
        rounds = int(sys.argv[3].split('=')[1]) if '=' in sys.argv[3] else 1000
        repeated_battle(p1_name, p2_name, rounds)
        return
    
    print("Добро пожаловать в Крестики-Нолики!")
    print("Вы играете за X, компьютер за O.")
    board = new_board()
    current_player = 'X'
    player_funcs = {'X': human_player, 'O': AI_FUNCTIONS['blocking_ai']}
    
    while True:
        render(board)
        print(f"Ход игрока {current_player}")
        move = player_funcs[current_player](board, current_player)
        if make_move(board, move, current_player):
            winner = get_winner(board)
            if winner:
                render(board)
                print(f"Победитель: {winner}!")
                break
            if is_board_full(board):
                render(board)
                print("Ничья!")
                break
            current_player = 'O' if current_player == 'X' else 'X'
        else:
            print("Клетка занята, попробуйте снова.")

if __name__ == "__main__":
    main()