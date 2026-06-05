import random

def random_ai(board, player):
    """Случайный допустимый ход"""
    empty_cells = []
    for y in range(3):
        for x in range(3):
            if board[y][x] is None:
                empty_cells.append((x, y))
    return random.choice(empty_cells) if empty_cells else None

def find_winning_move(board, player):
    """Возвращает координаты выигрышного хода для player, если он есть, иначе None"""
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
    """Выигрышный ход, иначе случайный"""
    move = find_winning_move(board, player)
    if move:
        return move
    return random_ai(board, player)

def finds_winning_and_losing_moves_ai(board, player):
    print("=== DEBUG ===")
    for row in board:
        print(row)
    print("player:", player)
    
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
    # Проверим, действительно ли клетка пуста
    x, y = move
    if test_board[y][x] is not None:
        print("ОШИБКА: клетка занята!", test_board[y][x])
    else:
        print("OK, клетка пуста")