# -*-coding: utf-8-*-
import copy
from chessengine.util import draw_board

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
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class ChessPosition(object):
    PAWN = Piece('pawn')
    HORSE = Piece('horse')
    BISHOP = Piece('bishop')
    TOWER = Piece('tower')
    QUEEN = Piece('queen')
    KING = Piece('king')

    WHITE = 'white'
    BLACK = 'black'

    def __init__(self, position_array, move_number, piece_moved=None, bc_rights=True, wc_rights=True):
        self.position = position_array
        self.move_number = move_number
        self.white_to_move = move_number % 2 == 1
        self.piece_moved = piece_moved
        self.bc_rights = bc_rights
        self.wc_rights = wc_rights

    def __unicode__(self):
        position = list(reversed(self.position))
        board = []
        mapper = {
            'pawn': 1,
            'horse': 2,
            'bishop': 3,
            'tower': 4,
            'queen': 5,
            'king': 6
        }
        for row in position:
            modified_row = []
            for element in row:
                if element is None:
                    modified_row.append(0)
                else:
                    piece, color = element
                    color_modifier = 1 if color == self.WHITE else -1
                    modified_row.append(color_modifier * mapper[piece.name])
            board.append(modified_row)
        return u'\n' + draw_board(board) + u'\n'

    def _is_white_piece(self, piece):
        return piece[1] == self.WHITE

    def get_moves_for_depth(self, depth=1):
        result = []
        if depth == 0:
            return []
        moves = self.get_moves()
        result.extend(moves)
        if depth > 1:
            for move in moves:
                result.extend(move.get_moves_for_depth(depth-1))
        return result

    def get_moves(self):
        color_to_move = self.WHITE if self.white_to_move else self.BLACK

        king, x, y = self.get_king(color_to_move) or (None, None, None)
        if king and self.king_in_check(king, x, y):
            return self._get_moves(king, x, y)
        moves = []
        for i, row in enumerate(self.position):
            for j, piece in enumerate(row):
                if piece == None:
                    continue
                if piece[1] == color_to_move:
                    moves.extend(self._get_moves(piece, i, j))
        return moves

    def _get_moves(self, piece, row, column, no_mate_checking=False):
        moves = []
        if piece[0].name == 'pawn':
            moves = self._get_pawn_moves(piece, row, column)
        elif piece[0].name == 'horse':
            moves = self._get_knight_moves(piece, row, column)
        elif piece[0].name == 'bishop':
            moves = self._get_bishop_moves(piece, row, column)
        elif piece[0].name == 'tower':
            moves = self._get_tower_moves(piece, row, column)
        elif piece[0].name == 'queen':
            moves = self._get_queen_moves(piece, row, column)
        elif piece[0].name == 'king':
            moves = self._get_king_moves(piece, row, column, no_mate_checking=no_mate_checking)
        else:
            raise NotImplementedError("%s" % piece[0])
        for move in moves[:]:
            if not no_mate_checking and not move.legal_move():
                moves.remove(move)
        return moves

    def copy_position(self, position):
        return [row[:] for row in position]

    def _get_pawn_moves(self, piece, row, column):
        #one forward, two forward, attack left, attack right,
        #en passent, upgrade to officer
        color = piece[1]
        possible_moves = []
        if color == self.WHITE:
            second_next_row = row + 2
            next_row = row + 1
            is_same_color = lambda piece: piece[1] == self.WHITE
            first_row = 1
            last_row = 6
            en_passent_row = 4
        else:
            second_next_row = row - 2
            next_row = row - 1
            is_same_color = lambda piece: piece[1] == self.BLACK
            first_row = 6
            last_row = 1
            en_passent_row = 3

        if row != last_row and self.position[next_row][column] == None:
            position = self.copy_position(self.position)
            position[row][column] = None
            position[next_row][column] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1))
        if row == first_row:
            if self.position[second_next_row][column] == None and self.position[next_row][column] == None:
                position = self.copy_position(self.position)
                position[row][column] = None
                position[second_next_row][column] = piece
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), (second_next_row, column)]))
        if row == last_row and self.position[next_row][column] == None:
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = self.copy_position(self.position)
                position[row][column] = None
                position[next_row][column] = (officer, color)
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), (next_row, column)]))
        #left attack and upgrade
        if row == last_row and column != 0 and self.position[next_row][column-1] != None and \
           not is_same_color(self.position[next_row][column-1]):
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = self.copy_position(self.position)
                position[row][column] = None
                position[next_row][column-1] = (officer, color)
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), (next_row, column-1)]))
        #right attack and upgrade
        if row == last_row and column != 7 and self.position[next_row][column+1] != None and \
           not is_same_color(self.position[next_row][column+1]):
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = self.copy_position(self.position)
                position[row][column] = None
                position[next_row][column+1] = (officer, color)
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), (next_row, column+1)]))
        # attack left
        if row != last_row and column != 0 and self.position[next_row][column-1] != None and \
           not is_same_color(self.position[next_row][column-1]):
            position = self.copy_position(self.position)
            position[row][column] = None
            position[next_row][column-1] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1,
                                                piece_moved=[(row, column), (next_row, column-1)]))
        # attack right
        if row != last_row and column != 7 and self.position[next_row][column+1] != None and \
           not is_same_color(self.position[next_row][column+1]):
            position = self.copy_position(self.position)
            position[row][column] = None
            position[next_row][column+1] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1,
                                                piece_moved=[(row, column), (next_row, column+1)]))
        # en passent left
        # if on opposite side row + 2 and last move was a double step
        # and on left side
        if column != 0 and row == en_passent_row and self.position[row][column-1] != None and \
           self.position[row][column-1][0] == self.PAWN and \
           not is_same_color(self.position[row][column-1]) and \
           self.piece_moved and \
           self.piece_moved[1] == (row, column-1) and \
           abs(self.piece_moved[1][0] - self.piece_moved[0][0]) == 2:
            position = self.copy_position(self.position)
            position[row][column] = None
            position[row][column-1] = None
            position[next_row][column-1] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1,
                                                piece_moved=[(row, column), (row, column-1)]))
        # en passent right
        # if on opposite side row + 2 and last move was a double step
        # and on right side
        if column != 7 and row == en_passent_row and self.position[row][column+1] != None and \
           self.position[row][column+1][0] == self.PAWN and \
           not is_same_color(self.position[row][column+1]) and \
           self.piece_moved and \
           self.piece_moved[1] == (row, column+1) and \
           abs(self.piece_moved[1][0] - self.piece_moved[0][0]) == 2:
            position = self.copy_position(self.position)
            position[row][column] = None
            position[row][column+1] = None
            position[next_row][column+1] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1,
                                                piece_moved=[(row, column), (row, column+1)]))
        return possible_moves

    def _get_knight_moves(self, piece, row, column):
        color = piece[1]
        if color == self.WHITE:
            is_same_color = lambda piece: piece[1] == self.WHITE
        else:
            is_same_color = lambda piece: piece[1] == self.BLACK
        movement_vectors = [[2, 1], [1, 2], [-1, 2], [1, -2], [-2, 1], [2, -1], [-2, -1], [-1, -2]]
        def within_bounds(position):
            return position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7
        possible_moves = []
        for movement_vector in movement_vectors:
            change = [row + movement_vector[0], column + movement_vector[1]]
            if within_bounds(change) and \
               (self.position[change[0]][change[1]] == None or
                not is_same_color(self.position[change[0]][change[1]])):
                position = self.copy_position(self.position)
                position[row][column] = None
                position[change[0]][change[1]] = piece
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), change]))
        return possible_moves

    def _get_bishop_moves(self, piece, row, column):
        color = piece[1]
        if color == self.WHITE:
            is_same_color = lambda piece: piece[1] == self.WHITE
        else:
            is_same_color = lambda piece: piece[1] == self.BLACK
        movement_vectors = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        def within_bounds(position):
            return position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7
        possible_moves = []
        for movement_vector in movement_vectors:
            for multiplier in range(1, 8):
                change = [row + multiplier * movement_vector[0],
                          column + multiplier * movement_vector[1]]
                if not within_bounds(change):
                    break
                movement_square = self.position[change[0]][change[1]]
                if movement_square is not None and is_same_color(movement_square):
                    break
                position = self.copy_position(self.position)
                position[row][column] = None
                position[change[0]][change[1]] = piece
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), change]))
                if movement_square is not None:
                    # Another color take or stop
                    break
        return possible_moves

    def _get_tower_moves(self, piece, row, column):
        color = piece[1]
        if color == self.WHITE:
            is_same_color = lambda piece: piece[1] == self.WHITE
        else:
            is_same_color = lambda piece: piece[1] == self.BLACK
        movement_vectors = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        def within_bounds(position):
            return position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7
        possible_moves = []
        for movement_vector in movement_vectors:
            for multiplier in range(1, 8):
                change = [row + multiplier * movement_vector[0],
                          column + multiplier * movement_vector[1]]
                if not within_bounds(change):
                    break
                movement_square = self.position[change[0]][change[1]]
                if movement_square is not None and is_same_color(movement_square):
                    break
                position = self.copy_position(self.position)
                position[row][column] = None
                position[change[0]][change[1]] = piece
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), change]))
                if movement_square is not None:
                    # Another color take or stop
                    break
        return possible_moves

    def _get_queen_moves(self, piece, row, column):
        return self._get_queenlike_moves(piece, row, column, use_multiplier=True)

    def _get_king_moves(self, piece, row, column, no_mate_checking=False):
        regular_moves = self._get_queenlike_moves(piece, row, column,
                                                  use_multiplier=False)
        castle_moves = self._get_castle_moves(piece, row, column, no_mate_checking=no_mate_checking)
        return regular_moves + castle_moves

    def _get_castle_moves(self, piece, row, column, no_mate_checking=False):
        '''
        - Tower in correct file
        - King in correct file
        - Nothing in between
        - Nothing under attack in all squares
        '''
        color = piece[1]
        king_file = 4
        tower_files = [0, 7]
        if color == self.WHITE:
            castle_row = 0
            attacking_color = self.BLACK
            castle_right = self.wc_rights
        else:
            castle_row = 7
            attacking_color = self.WHITE
            castle_right = self.bc_rights
        if not castle_right or row != castle_row or column != king_file:
            return []
        moves = []
        for tower_file in tower_files:
            tower_square = self.position[castle_row][tower_file]
            if tower_square is None or tower_square[0] != self.TOWER or tower_square[1] != color:
                continue
            if tower_file == 0:
                squares = range(0, 5)
            if tower_file == 7:
                squares = range(4, 8)
            illegal_castle = False
            for square in squares:
                if square not in [0, 4, 7] and self.position[castle_row][square] != None:
                    illegal_castle = True
                    break
                if not no_mate_checking and self.square_under_attack(attacking_color, castle_row, square):
                    illegal_castle = True
                    break
            if illegal_castle:
                continue
            position = self.copy_position(self.position)
            if tower_file == 0:
                position[castle_row][3] = position[castle_row][0]
                position[castle_row][2] = position[castle_row][4]
                change = [(castle_row, 4), (castle_row, 2)]
            else:
                position[castle_row][5] = position[castle_row][0]
                position[castle_row][6] = position[castle_row][4]
                change = [(castle_row, 4), (castle_row, 6)]
            position[castle_row][column] = None
            position[castle_row][tower_file] = None
            new_position = ChessPosition(position, self.move_number+1,
                                         piece_moved=[(row, column), change])
            moves.append(new_position)
        return moves

    def _get_queenlike_moves(self, piece, row, column, use_multiplier=True):
        color = piece[1]
        if color == self.WHITE:
            is_same_color = lambda piece: piece[1] == self.WHITE
        else:
            is_same_color = lambda piece: piece[1] == self.BLACK
        movement_vectors = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        def within_bounds(position):
            return position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7
        possible_moves = []
        for movement_vector in movement_vectors:
            multiplier_range = 8 if use_multiplier else 2
            for multiplier in range(1, multiplier_range):
                change = [row + multiplier * movement_vector[0],
                          column + multiplier * movement_vector[1]]
                if not within_bounds(change):
                    break
                movement_square = self.position[change[0]][change[1]]
                if movement_square is not None and is_same_color(movement_square):
                    break
                position = self.copy_position(self.position)
                position[row][column] = None
                position[change[0]][change[1]] = piece
                new_position = ChessPosition(position, self.move_number+1,
                                             piece_moved=[(row, column), change])
                possible_moves.append(new_position)
                if movement_square is not None:
                    # Another color take or stop
                    break
        return possible_moves

    def legal_move(self):
        color_to_move = self.BLACK if self.white_to_move else self.WHITE

        king, x, y = self.get_king(color_to_move) or (None, None, None)
        if king and self.king_in_check(king, x, y):
            return False
        return True

    def get_king(self, color):
        for i, row in enumerate(self.position):
            for j, piece in enumerate(row):
                if piece and piece[0] == self.KING and piece[1] == color:
                    return piece, i, j

    def square_under_attack(self, attacking_color, original_row, original_column):
        for i, row in enumerate(self.position):
            for j, piece in enumerate(row):
                if piece is not None and piece[1] == attacking_color:
                    if piece[0] == self.PAWN and abs(original_row - i) > 1:
                        # PAWNS can not attack further than 1 row away
                        continue
                    if piece[0] == self.HORSE and abs(original_row - i) > 3:
                        # HORSES can not attack further than 3 rows away
                        continue
                    if piece[0] == self.HORSE and abs(original_column - j) > 3:
                        # HORSES can not attack further than 3 columns away
                        continue
                    for move in self._get_moves(piece, i, j, no_mate_checking=True):
                        attacked_square = move.position[original_row][original_column]
                        if attacked_square != None and attacked_square[1] == attacking_color:
                            return True
        return False

    def king_in_check(self, original_piece, original_row, original_column):
        if original_piece[1] == self.WHITE:
            color = self.BLACK
        else:
            color = self.WHITE
        return self.square_under_attack(color, original_row, original_column)

    def get_strength(self):
        pass

if __name__ == '__main__':
    BLACK = ChessPosition.BLACK
    WHITE = ChessPosition.WHITE
    QUEEN = ChessPosition.QUEEN
    KING = ChessPosition.KING
    HORSE = ChessPosition.HORSE
    BISHOP = ChessPosition.BISHOP
    PAWN = ChessPosition.PAWN
    TOWER = ChessPosition.TOWER
    position2 = [
            [(TOWER, WHITE), (HORSE, WHITE), (BISHOP, WHITE), (QUEEN, WHITE), (KING, WHITE), (BISHOP, WHITE), (HORSE, WHITE), (TOWER, WHITE)],
            [(PAWN, WHITE), (PAWN, WHITE), (PAWN, WHITE), (PAWN, WHITE), (PAWN, WHITE), (PAWN, WHITE), (PAWN, WHITE), (PAWN, WHITE)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [(PAWN, BLACK), (PAWN, BLACK), (PAWN, BLACK), (PAWN, BLACK), (PAWN, BLACK), (PAWN, BLACK), (PAWN, BLACK), (PAWN, BLACK)],
            [(TOWER, BLACK), (HORSE, BLACK), (BISHOP, BLACK), (QUEEN, BLACK), (KING, BLACK), (BISHOP, BLACK), (HORSE, BLACK), (TOWER, BLACK)]]
    chess_position = ChessPosition(position2, 1)
    moves = chess_position.get_moves_for_depth(4)
    print len(moves)
