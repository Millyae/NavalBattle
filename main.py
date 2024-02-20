import random
class Ship:
    def __init__(self, size, positions):
        self.size = size
        self.positions = positions
        self.hits = [False] * size

    def hit(self, position):
        for i, pos in enumerate(self.positions):
            if pos == position:
                self.hits[i] = True
                return True
        return False

    def is_sunk(self):
        return all(self.hits)

class Board:
    def __init__(self, size=6):
        self.size = size
        self.ships = []

    def place_ship(self, ship):
        for pos in ship.positions:
            if not self.is_valid_position(pos):
                raise ValueError("Неверное положение судна")
        self.ships.append(ship)

    def is_valid_position(self, position):
        x, y = position
        return 1 <= x <= self.size and 1 <= y <= self.size

    def is_occupied(self, position):
        for ship in self.ships:
            if position in ship.positions:
                return True
        return False

    def random_position(self):
        return random.randint(1, self.size), random.randint(1, self.size)

    def receive_hit(self, position):
        for ship in self.ships:
            if ship.hit(position):
                return True
        return False

    def display(self, hide_ships=False):
        row_labels = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F"}
        print("   ", end="")
        for x in range(1, self.size + 1):
            print(f"| {x} ", end="")
        print("|")
        print("  " + "-" * (4 * self.size + 2))
        for y in range(1, self.size + 1):
            print(f"{row_labels[y]} |", end="")
            for x in range(1, self.size + 1):
                if hide_ships:
                    if any((x, y) in ship.positions for ship in self.ships if not ship.is_sunk()):
                        print(" O ", end="|")
                    else:
                        print("   ", end="|")
                else:
                    if any((x, y) in ship.positions for ship in self.ships):
                        if any((x, y) in ship.positions for ship in self.ships if ship.is_sunk()):
                            print(" X ", end="|")
                        else:
                            print(" ■ ", end="|")
                    else:
                        print(" T ", end="|")
            print()

    def display_move(self, position, hit):
        x, y = position
        if hit:
            print(f" {x}{y} | X")
        else:
            print(f" {x}{y} | T")

class Game:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.setup_board(self.player_board)
        self.setup_board(self.computer_board)

    def setup_board(self, board):
        board.place_ship(Ship(3, [(1, 1), (1, 2), (1, 3)]))
        board.place_ship(Ship(2, [(2, 6), (3, 6)]))
        board.place_ship(Ship(2, [(4, 1), (4, 3)]))
        board.place_ship(Ship(1, [(4, 6)]))
        board.place_ship(Ship(1, [(6, 1)]))
        board.place_ship(Ship(1, [(6, 3)]))
        board.place_ship(Ship(1, [(6, 5)]))

    def play(self):
        while True:
            print("Ваша доска:")
            self.player_board.display()
            print("\nДоска компьютера:")
            self.computer_board.display(hide_ships=True)
            player_move = self.get_move()
            hit = self.computer_board.receive_hit(player_move)
            if hit:
                print("Попадание!")
            else:
                print("Промах!")

            if self.check_winner(self.computer_board):
                print("Вы победили!")
                break

            computer_move = self.computer_board.random_position()
            hit = self.player_board.receive_hit(computer_move)
            if hit:
                print("Компьютер попал!")
            else:
                print("Компьютер промахнулся!")

            if self.check_winner(self.player_board):
                print("Вы проиграли!")
                break

    def get_move(self):
        while True:
            try:
                move = input("Введите координаты выстрела (например, A1): ")
                x = int(move[1])
                y = ord(move[0].upper()) - ord('A') + 1
                if not (1 <= x <= 6 and 1 <= y <= 6):
                    raise ValueError
                return x, y
            except (ValueError, IndexError):
                print("Неправильный формат ввода. Пожалуйста, введите в формате A1-F6.")

    def check_winner(self, board):
        for ship in board.ships:
            if not ship.is_sunk():
                return False
        return True

game = Game()
game.play()
