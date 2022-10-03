from random import randint, choice


class Board:
    def __init__(self):
        self.board = []
        self.opponent = [[0 for _ in range(6)] for _ in range(6)]
        self.ships = []
        self.points_available = 36
        self.ships_count = 7

    def cellAvailable(self, row, col):
        # Проверим все соседние ячейки. Если все они пустые, значит ячейку можно занимать
        for i in range(row - 1, row + 2):
            if i < 0 or i > 5:  # Выходим за границы
                continue
            for j in range(col - 1, col + 2):
                if i == row and j == col:  # Попали в середину
                    continue
                if j < 0 or j > 5:  # Выходим за границы
                    continue
                if self.board[i][j][0] is not None:  # Ячейка занята
                    return False
        return True

    def add3(self):
        # Корабль 3-клетки
        # Зададим начальную позицию для левого верхнего угла корабля
        row = randint(0, 5)  # Номер строки (изначально делаем горизонтально, строка любая)
        col = randint(0, 3)  # Номер столбца (нельзя брать последние два столбца, иначе не поместится)
        direction = randint(0, 1)  # Направление корабля (0 - горизонтально, 1 - вертикально)
        if direction == 1:  # Если корабль расположен вертикально, то отразим точку относительно главной диагонали
            row, col = col, row
        # Создаем и добавляем корабль в список
        ship = Ship(3, row, col, direction)
        self.ships.append(ship)
        if direction == 0:
            for i in range(3):
                self.board[row][col + i] = (ship, i)
        else:
            for i in range(3):
                self.board[row + i][col] = (ship, i)

    def add2(self):
        # Корабль 2-клетки
        lst = []  # Список подходящих
        # Перебираем горизонтальные корабли
        for row in range(6):
            for col in range(5):
                if self.board[row][col][0] is None and self.board[row][col + 1][0] is None:  # Нужные клетки не заняты
                    if self.cellAvailable(row, col) and self.cellAvailable(row, col + 1):  # Соседние клетки не заняты
                        lst.append((row, col, 0))
        # Перебираем вертикальные корабли
        for row in range(5):
            for col in range(6):
                if self.board[row][col][0] is None and self.board[row + 1][col][0] is None:  # Нужные клетки не заняты
                    if self.cellAvailable(row, col) and self.cellAvailable(row + 1, col):  # Соседние клетки не заняты
                        lst.append((row, col, 1))
        s = choice(lst)
        row = s[0]
        col = s[1]
        direction = s[2]
        ship = Ship(2, row, col, direction)
        if direction == 0:
            self.board[row][col] = (ship, 0)
            self.board[row][col + 1] = (ship, 1)
        else:
            self.board[row][col] = (ship, 0)
            self.board[row + 1][col] = (ship, 1)

    def add1(self):
        # Корабль 1-клетка
        lst = []
        for row in range(6):
            for col in range(6):
                if self.board[row][col][0] is None:  # Нужная клетка не занята
                    if self.cellAvailable(row, col):  # Соседние клетки не заняты
                        lst.append((row, col, 0))
        if len(lst) == 0:  # Нет подходящих мест для корабля
            return True
        s = choice(lst)
        row = s[0]
        col = s[1]
        ship = Ship(1, row, col, 0)
        self.board[row][col] = (ship, 0)
        return False

    def fill(self):
        success = False
        while not success:
            self.board = [[(None, 0) for _ in range(6)] for _ in range(6)]
            self.ships = []
            self.add3()
            self.add2()
            self.add2()
            # Одноклеточные корабли могут не поместиться. Тогда будем перегенерировать все заново
            success = True
            for _ in range(4):
                if self.add1():
                    success = False

    @classmethod
    def drawSplitter(cls):
        # Рисуем горизонтальную разделительную линию
        first_cell = True
        for _ in range(6):
            if first_cell:
                print("  ───", end='')
                first_cell = False
            else:
                print("┼───", end='')

    def print(self):
        first_row = True
        print("Ваше поле                          Поле противника")
        # Подписываем сверху буквы
        print("   А   Б   В   Г   Д   Е              А   Б   В   Г   Д   Е")
        row_num = 1
        for row, opp_row in zip(self.board, self.opponent):
            # Рисуем горизонтальную разделительную линию
            if first_row:
                first_row = False
            else:
                self.drawSplitter()
                print("          ", end='')
                self.drawSplitter()
                print()
            # Рисуем основную строку своего поля
            print(str(row_num) + " ", end='')
            first_cell = True
            for cell in row:
                if first_cell:
                    first_cell = False
                else:
                    print("│", end='')
                # Если нет корабля
                if cell[0] is None:
                    if cell[1] == 0:
                        print("   ", end='')
                    else:
                        print(" · ", end='')
                # Если есть корабль
                else:
                    if cell[0].getState(cell[1]) == 0:
                        print(" █ ", end='')
                    else:
                        print(" X ", end='')
            print("          ", end='')
            # Рисуем основную строку поля противника
            print(str(row_num) + " ", end='')
            first_cell = True
            for cell in opp_row:
                if first_cell:
                    first_cell = False
                else:
                    print("│", end='')
                # Если нет корабля
                if cell == 0:
                    print("   ", end='')
                elif cell == 1:
                    print(" · ", end='')
                elif cell == 2:
                    print(" X ", end='')
                else:
                    print(" █ ", end='')
                # Если есть корабль
            print()
            row_num += 1

    def shot(self, point):
        # Выстрел по заданным координатам
        (row, col) = point
        cell = self.board[row][col]
        if cell[0] is None:  # Пустая клетка
            if cell[1] == 0:
                self.board[row][col] = (None, 1)
                return 1  # Промах
            else:
                return -1  # Ошибка! Сюда уже стреляли!
        else:
            result = cell[0].shot(cell[1])
            if result == 3:
                self.ships_count -= 1
            return 5 if self.ships_count == 0 else result

    def floodFill(self, row, col):
        # Перекрашиваем все подбитые (2) части корабля в (3), чтобы корректно отображалось на поле
        if self.opponent[row][col] == 2:
            self.opponent[row][col] = 3
            if row > 0:
                self.floodFill(row - 1, col)
            if row < 5:
                self.floodFill(row + 1, col)
            if col > 0:
                self.floodFill(row, col - 1)
            if col < 5:
                self.floodFill(row, col + 1)
            if row > 0 and col > 0:
                self.floodFill(row - 1, col - 1)
            if row < 5 and col < 5:
                self.floodFill(row + 1, col + 1)
            if row < 5 and col > 0:
                self.floodFill(row + 1, col - 1)
            if row > 0 and col < 5:
                self.floodFill(row - 1, col + 1)
        if self.opponent[row][col] == 0:
            self.opponent[row][col] = 1
            self.points_available -= 1

    def setResult(self, point, result):
        # Помечаем результат выстрела на поле противника
        (row, col) = point
        if result == 3:
            self.opponent[row][col] = 2
            self.floodFill(row, col)
        self.opponent[row][col] = result
        self.points_available -= 1

    def getRandomAvailablePoint(self):
        # Получаем случайную свободную точку на поле противника
        r = randint(1, self.points_available)
        for row in range(6):
            for col in range(6):
                if self.opponent[row][col] == 0:
                    r -= 1
                    if r == 0:
                        return row, col
        raise IndexError


class Ship:
    def __init__(self, n, row, col, direction):
        self.n = n
        self.row = row
        self.col = col
        self.direction = direction
        self.ship = n * [0]  # 0 - нет попадания

    def getState(self, k):
        if len(self.ship) <= k:
            raise IndexError
        return self.ship[k]

    def shot(self, k):
        if len(self.ship) <= k:
            raise IndexError
        if not self.ship[k] == 0:
            return -1  # Ошибка! Сюда уже стреляли!
        self.ship[k] = 1
        self.n -= 1
        if self.n < 0:
            raise IndexError
        return 2 if self.n > 0 else 3  # Если попали, возвращаем 1, если убили - 2


class Player:
    def __init__(self, player_type):
        self.player_type = player_type  # 0 - человек, 1 - компьютер
        self.board = Board()
        self.board.fill()

    def shot(self, point):
        return self.board.shot(point)

    def getPoint(self):
        # Если это игрок, получаем от него координаты выстрела
        if self.player_type == 0:
            while True:
                res = input("Введите координаты выстрела: ").upper()
                if not len(res) == 2:
                    raise UserWarning("Неверный формат ввода! Ввод должен быть в формате <буква><цифра>!")
                col, row = res[0], res[1]
                if col not in "АБВГДЕ":
                    raise UserWarning("Неверная буква! Должна быть от А до Е!")
                if row not in "123456":
                    raise UserWarning("Неверный номер строки! Номер строки должен быть от 1 до 6!")
                else:
                    row = int(row)
                    if row < 1 or row > 6:
                        raise UserWarning("Неверный номер строки! Номер строки должен быть от 1 до 6!")
                col = "АБВГДЕ".index(col)
                return row-1, col
        else:
            return self.board.getRandomAvailablePoint()

    def setResult(self, point, result):
        self.board.setResult(point, result)

    def print(self):
        self.board.print()


def main():
    Players = [Player(0), Player(1)]
    curr_player = 0
    other_player = 1
    game_over = False
    print("Привет! Давай поиграем в морской бой! Правила простые:")
    print("- Количество кораблей: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку")
    print("- Корабли находятся на расстоянии минимум одна клетка друг от друга")
    print("- Нельзя дважды стрелять в одну и ту же клетку")
    print("- Координаты вводятся в формате <Столбец><Строка>, например, А1")
    # Основной игровой цикл
    while not game_over:
        # Если текущий игрок - человек, то печатаем его карточку
        if curr_player == 0:
            Players[0].print()
        # Пытаемся получить координаты выстрела, пока не получим подходящие
        while True:
            point = Players[curr_player].getPoint()
            shot_result = Players[other_player].shot(point)
            if shot_result == -1:
                print("В эти координаты уже стреляли!")
            else:
                if shot_result == 5:
                    print("Победил " + ("Человек!" if curr_player == 0 else "Компьютер!"))
                    game_over = True
                else:
                    Players[curr_player].setResult(point, shot_result)
                break
        curr_player, other_player = other_player, curr_player


if __name__ == '__main__':
    main()