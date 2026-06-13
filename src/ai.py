import random
import copy
from .game_logic import get_winner, is_board_full
from functools import lru_cache

def minimax_ai_alpha_beta(board, current_player):
    board_tuple = tuple(tuple(row) for row in board)
    _, best_move = _minimax_alpha_beta(board_tuple, current_player, True, -float('inf'), float('inf'))
    return best_move

def _minimax_alpha_beta(board_tuple, player, is_maximizing, alpha, beta):
    board = [list(row) for row in board_tuple]
    opponent = 'O' if player == 'X' else 'X'
    
    winner = get_winner(board)
    if winner is not None or is_board_full(board):
        if winner == player:
            return (1, None)
        elif winner == opponent:
            return (-1, None)
        return (0, None)
    
    if is_maximizing:
        best_score = -float('inf')
        best_move = None
        for y in range(3):
            for x in range(3):
                if board[y][x] is None:
                    board[y][x] = player
                    score, _ = _minimax_alpha_beta(
                        tuple(tuple(row) for row in board), player, False, alpha, beta
                    )
                    board[y][x] = None
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        return (best_score, best_move)
        return (best_score, best_move)
    else:
        best_score = float('inf')
        best_move = None
        for y in range(3):
            for x in range(3):
                if board[y][x] is None:
                    board[y][x] = opponent
                    score, _ = _minimax_alpha_beta(
                        tuple(tuple(row) for row in board), player, True, alpha, beta
                    )
                    board[y][x] = None
                    if score < best_score:
                        best_score = score
                        best_move = (x, y)
                    beta = min(beta, best_score)
                    if alpha >= beta:
                        return (best_score, best_move)
        return (best_score, best_move)

def minimax_ai(board, current_player):
    board_tuple = tuple(tuple(row) for row in board)
    _, best_move = _minimax_cached(board_tuple, current_player, True)
    return best_move

@lru_cache(maxsize=None)
def _minimax_cached(board_tuple, player, is_maximizing):
    board = [list(row) for row in board_tuple]
    opponent = 'O' if player == 'X' else 'X'
    
    winner = get_winner(board)
    if winner is not None or is_board_full(board):
        if winner == player:
            return (1, None)
        elif winner == opponent:
            return (-1, None)
        else:
            return (0, None)
    
    if is_maximizing:
        best_score = -float('inf')
        best_move = None
        for y in range(3):
            for x in range(3):
                if board[y][x] is None:
                    board[y][x] = player
                    # Рекурсивный вызов для хода противника
                    score, _ = _minimax_cached(tuple(tuple(row) for row in board), player, False)
                    board[y][x] = None
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
        return (best_score, best_move)
    else:
        best_score = float('inf')
        best_move = None
        for y in range(3):
            for x in range(3):
                if board[y][x] is None:
                    board[y][x] = opponent
                    score, _ = _minimax_cached(tuple(tuple(row) for row in board), player, True)
                    board[y][x] = None
                    if score < best_score:
                        best_score = score
                        best_move = (x, y)
        return (best_score, best_move)

def random_ai(board, player):
    empty_cells = []
    for y in range(3):
        for x in range(3):
            if board[y][x] is None:
                empty_cells.append((x, y))
    return random.choice(empty_cells) if empty_cells else None

def find_winning_move(board, player):
    for y in range(3):
        row = board[y]
        if row.count(player) == 2 and row.count(None) == 1:
            x = row.index(None)
            return (x, y)
    for x in range(3):
        col = [board[y][x] for y in range(3)]
        if col.count(player) == 2 and col.count(None) == 1:
            y = col.index(None)
            return (x, y)
    diag1 = [board[i][i] for i in range(3)]
    if diag1.count(player) == 2 and diag1.count(None) == 1:
        i = diag1.index(None)
        return (i, i)
    diag2 = [board[i][2-i] for i in range(3)]
    if diag2.count(player) == 2 and diag2.count(None) == 1:
        i = diag2.index(None)
        return (2-i, i)
    return None

def finds_winning_moves_ai(board, player):
    move = find_winning_move(board, player)
    if move:
        return move
    return random_ai(board, player)

def finds_winning_and_losing_moves_ai(board, player):
    move = find_winning_move(board, player)
    if move:
        print("winning move:", move, "value at that cell:", board[move[1]][move[0]])
        return move
    
    opponent = 'O' if player == 'X' else 'X'
    move = find_winning_move(board, opponent)
    if move:
        print("blocking move:", move, "value:", board[move[1]][move[0]])
        return move
    
    empty_cells = [(x, y) for y in range(3) for x in range(3) if board[y][x] is None]
    print("empty cells:", empty_cells)
    move = random.choice(empty_cells) if empty_cells else None
    print("random move:", move)
    return move

if __name__ == "__main__":
    test_board = [
        ['X', 'O', None],
        [None, 'O', None],
        ['X', None, None]
    ]
    move = random_ai(test_board, 'X')
    print("random_ai вернул:", move)
    x, y = move
    if test_board[y][x] is not None:
        print("ОШИБКА: клетка занята!", test_board[y][x])
    else:
        print("OK, клетка пуста")