import copy

class ChessAlgorithm(object):
    def find_all_moves(self, position):
        return position.get_moves()

    def check_strength(self, position):
        position.get_strength()

    def sort_moves_by_strength(self, moves):
        return sorted(moves, key=lambda m: m.strength)

    def iterate(self, original_position):
        moves = self.find_all_moves(original_position)
        for position in moves:
            position.strength = self.check_strength(position)
        for move in self.sort_moves_by_strength(moves):
            print 'Move %s %s' % (move, move.strength)

class Piece(object):
    pass

class ChessPosition(object):
    PAWN = Piece()
    HORSE = Piece()
    BISHOP = Piece()
    TOWER = Piece()
    QUEEN = Piece()
    KING = Piece()

    WHITE = True
    BLACK = False

    def __init__(self, position_array, move_number):
        self.position = position_array
        self.move_number = move_number
        self.white_to_move = move_number % 2 == 1

    def __str__(self):
        return self.position

    def __repr__(self):
        return str(self.position)

    def _is_white_piece(self, piece):
        return piece[1]

    def get_moves(self):
        moves = []
        for i, row in enumerate(self.position):
            for j, piece in enumerate(row):
                if piece == None:
                    continue
                if self.white_to_move and self._is_white_piece(piece):
                    moves += self._get_moves(piece, i, j)
                if not self.white_to_move and not self._is_white_piece(piece):
                    moves += self._get_moves(piece, i, j)
        return moves

    def _get_moves(self, piece, row, column):
        if piece[0] == self.PAWN and piece[1] == self.WHITE:
            return self._get_white_pawn_moves(piece, row, column)

    def _get_pawn_moves(self, piece, row, column, color=WHITE):
        #TODO: en passent
        #one forward, two forward, attack left, attack right,
        #en passent, upgrade to officer
        possible_moves = []
        if color == self.WHITE:
            second_next_row = row + 2
            next_row = row + 1
            is_same_color = self._is_white_piece
        else:
            second_next_row = row - 2
            next_row = row - 1
            is_same_color = lambda *x: not self._is_white_piece(*x)

        if row < 6 and self.position[next_row][column] == None:
            position = copy.deepcopy(self.position)
            position[row][column] = None
            position[next_row][column] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1))
        if row == 1:
            if self.position[second_next_row][column] == None and self.position[next_row][column] == None:
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[second_next_row][column] = piece
                possible_moves.append(ChessPosition(position, self.move_number+1))
        if row == 6 and self.position[next_row][column] == None:
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[next_row][column] = (officer, self.WHITE)
                possible_moves.append(ChessPosition(position, self.move_number+1))
        #left attack and upgrade
        if row == 6 and column != 0 and self.position[next_row][column-1] != None and \
           not is_same_color(self.position[next_row][column-1]):
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[next_row][column-1] = (officer, self.WHITE)
                possible_moves.append(ChessPosition(position, self.move_number+1))
        #right attack and upgrade
        if row == 6 and column != 7 and self.position[next_row][column+1] != None and \
           not is_same_color(self.position[next_row][column+1]):
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[next_row][column+1] = (officer, self.WHITE)
                possible_moves.append(ChessPosition(position, self.move_number+1))
        # attack left
        if row < 6 and column != 0 and self.position[next_row][column-1] != None and \
           not is_same_color(self.position[next_row][column-1]):
            position = copy.deepcopy(self.position)
            position[row][column] = None
            position[next_row][column-1] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1))
        # attack right
        if row < 6 and column != 7 and self.position[next_row][column+1] != None and \
           not is_same_color(self.position[next_row][column+1]):
            position = copy.deepcopy(self.position)
            position[row][column] = None
            position[next_row][column+1] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1))
        return possible_moves

    def _get_black_pawn_moves(self, piece, row, column):
        pass

    def get_strength(self):
        pass
