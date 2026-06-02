import random

def random_ai(board, player):
    empty_cells = []
    for y in range(3):
        for x in range(3):
            if board[y][x] is None:
                empty_cells.append((x, y))
    
    return random.choice(empty_cells) if empty_cells else None

def finds_winning_moves_ai(board, player):
    for y in range(3):
        row = board[y]
        if row.count(player) == 2 and row.count(None) == 1:
            # Находим индекс пустой клетки в строке
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
        return (i, 2-i)
    
    return random_ai(board, player)