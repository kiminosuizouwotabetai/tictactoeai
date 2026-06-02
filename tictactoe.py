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
        print("Клетка занята! Пропускаем ход.")  # временно
        return False
    board[y][x] = player
    return True

def get_winner(board):
    # строки
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    # столбцы
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    # диагонали
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def is_board_full(board):
    for row in board:
        if None in row:
            return False
    return True

def main():
    board = new_board()
    current_player = 'X'

    while True:
        render(board)
        print(f"Ход игрока {current_player}")
        move = get_move()
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
            print("Попробуйте снова.")

if __name__ == "__main__":
    main()