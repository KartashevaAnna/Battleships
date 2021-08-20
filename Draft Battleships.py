from random import randint
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ocean:
    def __init__(self):
        self.ocean = [["~" for column in range(6)] for row in range(6)]
        self.all_ships = []
        self.do_not_shoot_here = []
        self.ships_afloat = 7

    def view_ocean(self):
        for row in self.ocean:
            print(" ".join(row))
        return ""

    def place_ship(self, ship):
        for i in ship.hull():
            if not self.in_ocean(i) or i in self.do_not_shoot_here:
                raise OutOfBoardException
        ship_occupies_position = ship.hull()
        for grid_square in ship_occupies_position:
            self.ocean[grid_square.x][grid_square.y] = "\033[37m#"
            self.do_not_shoot_here.append(grid_square)
        self.all_ships.append(ship)
        self.envelop(ship)

    def envelop(self, ship):
        displacement = [(0, 1), (1, 1), (1, 0), (-1, 0), (0, -1), (1, - 1), (-1, 1), (-1, -1)]
        for element in ship.hull():
            for x, y in displacement:
                point_in_envelope = Point(element.x + x, element.y + y)
                if point_in_envelope not in self.do_not_shoot_here and self.in_ocean(point_in_envelope):
                    self.ocean[point_in_envelope.x][point_in_envelope.y] = "\033[90m^"
                    self.do_not_shoot_here.append(point_in_envelope)
    def in_ocean(self, point):
        limits = [0, 1, 2, 3, 4, 5]
        return point.x in limits and point.y in limits

    def missed_shot(self, point):
        if self.in_ocean(point):
            self.ocean[point.x][point.y] = "\033[94mO"
            print("\033[37mIt's a miss")
            self.do_not_shoot_here.append(point)

    def shot(self, point):
        if not self.in_ocean(point):
            raise OutOfBoardException
        if point in self.do_not_shoot_here:
            raise YouVeAlreadyShotHereException
        for ship in self.all_ships:
            if point in ship.hull():
                ship.lives -=1
                self.do_not_shoot_here.append(point)
                if ship.lives == 0:
                    print("\033[37mShip sunk!")
                    self.ships_afloat-=1
                    self.envelop(ship)
                    self.ocean[point.x][point.y] = "\033[35mH"
                    return True
                else:
                    print("\033[37mIt's a hit")
                    self.ocean[point.x][point.y] = "\033[35mH"
                    return True
        self.missed_shot(point)

    def clear_used_points(self):
        self.do_not_shoot_here = []




class Ship:
    def __init__(self, stern, length, is_horizontal=True):
        self.stern = stern
        self.length = length
        self.is_horizontal = is_horizontal
        self.lives = length


    def __repr__(self):
        return f"{self.hull()}"

    def hull(self):
        hull = []
        start_point_x = self.stern.x
        start_point_y = self.stern.y
        if self.is_horizontal:
            for i in range(self.length):
                hull.append(Point(start_point_x + i, start_point_y))
        else:
            for i in range(self.length):
                hull.append(Point(start_point_x, start_point_y + i))
        return hull

    def is_hit(self, point):
        return point in self.hull()


class My_Exceptions(Exception):
    pass
class OutOfBoardException(My_Exceptions):
    def __repr__(self):
        return "These coordinates are out of range"
class YouVeAlreadyShotHereException(My_Exceptions):
    def __repr__(self):
        return "You've already shot here!"
class Game:
    def _init_(self):
        player = self.random_ocean()
        computer = self.random_ocean()
    def random_ocean(self, is_visible = True):
        if is_visible:
            ocean = None
            while ocean is None:
                ocean = self.random_place()
                return ocean
        else:
            ocean = None
            while ocean is None:
                ocean = self.random_place(False)
                return ocean
    def random_place(self, is_visible = True):
        ship_hulls = [3, 2, 2, 1, 1, 1, 1]
        ocean = Ocean()
        attempts = 0
        for ship_size in ship_hulls:
            while True:
                attempts +=1
                if attempts > 10000:
                    return None
                ship = Ship(Point(randint(0, 5), randint(0, 5)), ship_size, randint(0, 1))
                try:
                    ocean.place_ship(ship)
                    break
                except OutOfBoardException:
                    pass
        ocean.clear_used_points()
        if not is_visible:
            ocean.ocean = [["~" for column in range(6)] for row in range(6)]

        return ocean
    def pick_a_target(self, is_human = True):
        if is_human:
            while True:
                dirty = input("give me a target (two integers from 1 to 6 with a space between them) ").split()
                if len(dirty)!=2:
                    print("Give me two coordinates with a space")
                    continue
                x, y = dirty
                if not (x.isdigit()) or not (y.isdigit):
                    print("Give me two coordinates with a space")
                    continue
                x, y = int(x), int(y)
                allowed_range = [1, 2, 3, 4, 5, 6]
                if x not in allowed_range or y not in allowed_range:
                    print("Give me two integers from 1 to 6")
                    continue
                target = Point(x - 1, y - 1)
                return target
        else:
            target = Point(randint(0, 5), randint(0, 5))
            return target
    def game_loop(self):
        my_ocean = self.random_ocean()
        computer_ocean = self.random_ocean(False)
        print("Your ocean")
        my_ocean.view_ocean()
        print("Computer ocean")
        computer_ocean.view_ocean()
        game_over = False
        while not game_over:
            successful_shot = False
            while not successful_shot:
                try:
                    target = self.pick_a_target(False)
                    my_ocean.shot(target)
                    print(f"computer target {target}")
                    print("your ocean")
                    my_ocean.view_ocean()
                    if my_ocean.ships_afloat == 0:
                        game_over = True
                    successful_shot = True
                except YouVeAlreadyShotHereException:
                    continue
            successful_shot = False
            while not successful_shot:
                try:
                    print("computer ocean")
                    computer_ocean.view_ocean()
                    target = self.pick_a_target()
                    computer_ocean.shot(target)
                    print(f"player targets {target}")
                    print("computer ocean")
                    computer_ocean.view_ocean()
                    if computer_ocean.ships_afloat == 0:
                        game_over = True
                    successful_shot = True
                except YouVeAlreadyShotHereException:
                    continue
first_game = Game()
first_game.game_loop()






