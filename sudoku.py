class Game:
    def __init__(self, game):
        '''Takes in a list of 81 numbers, parses into Groups of Rows, Columns, Boxes'''
        game = [Value(x) for x in game]
        self.rows = [[] for i in range(9)]
        counter = 0
        for x in range(9):
            for y in range(9):
                self.rows[x].append(game[counter])
                counter += 1
        self.rows = [Group(x) for x in self.rows]
        self.cols = [[] for i in range(9)]
        counter = 0
        for x in range(9):
            for y in range(9):
                self.cols[y].append(game[counter])
                counter += 1
        self.cols = [Group(x) for x in self.cols]
        counter = 0
        self.boxes = [[] for i in range(9)]
        for x in range(9):
            box_tracker = 0
            if (x > 2):
                box_tracker = 3
            if (x > 5):
                box_tracker = 6
            for y in range(9):
                add = 0
                if (6 > y > 2):
                    add = 1
                if (y > 5):
                    add = 2
                self.boxes[box_tracker + add].append(game[counter])
                counter += 1
        self.boxes = [Group(x) for x in self.boxes]
        self.test_mode = False
        self.game = game

    def print_game(self):
        '''Prints the game'''
        game = ''
        row_count = 0
        col_count = 0
        for x in self.rows:
            for y in x:
                game += str(y)
                col_count += 1
                if (col_count % 3 == 0 and col_count != 9):
                    game += ' '
            game += '\n'
            row_count += 1
            if (row_count % 3 == 0 and row_count != 9):
                game += '\n'
        print(game)


    def eliminate_possibilities(self):
        '''Eliminates possible values based on row, column, and box'''
        if (self.test_mode):
            for i in self.rows:
                i.test_elim_poss()
            for i in self.cols:
                i.test_elim_poss()
            for i in self.boxes:
                i.test_elim_poss()
        else:
            for i in self.rows:
                i.elim_poss()
            for i in self.cols:
                i.elim_poss()
            for i in self.boxes:
                i.elim_poss()


    def update_game(self):
        '''Updates possible values for each square, finds the square with least number of possible values to test'''
        counter = 0
        min_length = 100
        for i in self.rows:
            for x in i:
                if (self.test_mode):
                    if (len(x.test_values) == 1):
                        x.try_value(x.test_values[0])
                        counter += 1
                        self.eliminate_possibilities()
                elif (len(x) == 1):
                    x.set_value(x.possible_values[0])
                    counter += 1
                    self.eliminate_possibilities()
                if (self.test_mode):
                    if (len(x.test_values) < min_length and x.value == 0):
                        min_length = len(x.test_values)
                        min_square = x
                elif (len(x.possible_values) < min_length and len(x.possible_values) != 0):
                    min_length = len(x)
                    min_square = x
                if (len(x.test_values) == 0 and x.value == 0):
                    return True
                if all([x.check_sum() for x in self.rows]):
                    return False
        if (counter == 0):
            self.test_mode = True
            self.test_solve(min_square)
            return False

        return False


    def test_solve(self, box):
        '''Looks for solution via depth first search'''
        moves = [x for x in box.test_values]
        current_values = [x.value for x in self.game]
        other_values = [[y for y in x.test_values] for x in self.game]
        'Tries each possible value'
        for x in moves:
            if (all([x.check_sum() for x in self.rows])):
                return
            box.try_value(x)
            while not (all([x.check_sum() for x in self.rows])):
                self.eliminate_possibilities()
                if (self.update_game()):
                    break
                if (all([x.check_sum() for x in self.rows])):
                    return
            index = 0
            for x in self.game:
                x.test_values = [y for y in other_values[index]]
                x.value = current_values[index]
                index += 1
        box.try_value(0)

    def solve(self):
        while not (all([x.check_sum() for x in self.rows])):
            self.eliminate_possibilities()
            self.update_game()
        return [x.value for x in self.game]


class Group:
    def __init__(self, entries):
        self.entries = entries
        self.current = 0

    def check_sum(self):
        if (sum([x.val() for x in self.entries]) == 45):
            return True
        else:
            return False

    def check_unique(self):
        return len(set(self.entries)) != 9

    def __iter__(self):
        return self

    def __next__(self):
        if (self.current > 8):
            self.current = 0
            raise StopIteration
        else:
            self.current += 1
            return self.entries[self.current - 1]

    def elim_poss(self):
        for i in self.entries:
            if (len(i.possible_values) != 0):
                for x in self.entries:
                    if (x.val() in i.possible_values):
                        i.possible_values.remove(x.val())
                        i.test_values.remove(x.val())

    def test_elim_poss(self):
        for i in self.entries:
            if len(i.test_values) != 0:
                for x in self.entries:
                    if (x.val() in i.test_values):
                        i.test_values.remove(x.val())


class Value:
    def __init__(self, val):
        self.value = val
        if (val == 0):
            self.possible_values = [i + 1 for i in range(9)]
            self.test_values = [i + 1 for i in range(9)]
        else:
            self.possible_values = []
            self.test_values = []
        self.testing = False
        self.test_index = 0

    def val(self):
        return self.value

    def try_value(self, value):
        self.value = value
        self.test_values = []

    def set_value(self, value):
        self.value = value
        self.possible_values = []

    def __len__(self):
        return len(self.possible_values)

    def __str__(self):
        if self.val() == 0:
            return '_'
        else:
            return str(self.value)
