# Крестики-нолики с искусственным интеллектом

Игра с несколькими уровнями ИИ: от случайных ходов до непобедимого алгоритма минимакс.

### Вариант 1: из исходного кода (требуется Python 3.7+)

pip install -r requirements.txt
python src/ti   ctactoe.py

### Вариант 2: из исполнительного файла .exe

Тут все очень просто: заходите в Releases, качаете .exe и играете!

### Игровой процесс

- Играйте против ИИ или наблюдайте битвы разных алгоритмов.

- Выберите режим при запуске: человек vs ИИ, ИИ vs ИИ, человек vs человек.

### Доступные ИИ

- random_ai – случайные ходы

- winning_ai – делает выигрышный ход, иначе случайный

- blocking_ai – атака + защита

- minimax_ai – непобедимый (реально непобедимый)

### Бонус

Команда для битвы 1000 партий:

bash
python src/tictactoe.py random_ai blocking_ai --battle=1000


[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=kiminosuizouwotabetai_tictactoeai&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=kiminosuizouwotabetai_tictactoeai)