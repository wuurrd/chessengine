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

    WHITE = True
    BLACK = False

    def __init__(self, position_array, move_number, piece_moved=None):
        self.position = position_array
        self.move_number = move_number
        self.white_to_move = move_number % 2 == 1
        self.piece_moved = piece_moved

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
            return self._get_pawn_moves(piece, row, column)
        if piece[0] == self.PAWN and piece[1] == self.BLACK:
            return self._get_pawn_moves(piece, row, column, color=self.BLACK)

    def _get_pawn_moves(self, piece, row, column, color=WHITE):
        #one forward, two forward, attack left, attack right,
        #en passent, upgrade to officer
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
            position = copy.deepcopy(self.position)
            position[row][column] = None
            position[next_row][column] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1))
        if row == first_row:
            if self.position[second_next_row][column] == None and self.position[next_row][column] == None:
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[second_next_row][column] = piece
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), (second_next_row, column)]))
        if row == last_row and self.position[next_row][column] == None:
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[next_row][column] = (officer, color)
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), (next_row, column)]))
        #left attack and upgrade
        if row == last_row and column != 0 and self.position[next_row][column-1] != None and \
           not is_same_color(self.position[next_row][column-1]):
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[next_row][column-1] = (officer, color)
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), (next_row, column-1)]))
        #right attack and upgrade
        if row == last_row and column != 7 and self.position[next_row][column+1] != None and \
           not is_same_color(self.position[next_row][column+1]):
            for officer in [self.HORSE, self.BISHOP, self.TOWER, self.QUEEN]:
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[next_row][column+1] = (officer, color)
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), (next_row, column+1)]))
        # attack left
        if row != last_row and column != 0 and self.position[next_row][column-1] != None and \
           not is_same_color(self.position[next_row][column-1]):
            position = copy.deepcopy(self.position)
            position[row][column] = None
            position[next_row][column-1] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1,
                                                piece_moved=[(row, column), (next_row, column-1)]))
        # attack right
        if row != last_row and column != 7 and self.position[next_row][column+1] != None and \
           not is_same_color(self.position[next_row][column+1]):
            position = copy.deepcopy(self.position)
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
           self.piece_moved[1] == (row, column-1) and \
           abs(self.piece_moved[1][0] - self.piece_moved[0][0]) == 2:
            position = copy.deepcopy(self.position)
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
           self.piece_moved[1] == (row, column+1) and \
           abs(self.piece_moved[1][0] - self.piece_moved[0][0]) == 2:
            position = copy.deepcopy(self.position)
            position[row][column] = None
            position[row][column+1] = None
            position[next_row][column+1] = piece
            possible_moves.append(ChessPosition(position, self.move_number+1,
                                                piece_moved=[(row, column), (row, column+1)]))
        return possible_moves

    def _get_knight_moves(self, piece, row, column, color=WHITE):
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
                position = copy.deepcopy(self.position)
                position[row][column] = None
                position[change[0]][change[1]] = piece
                possible_moves.append(ChessPosition(position, self.move_number+1,
                                                    piece_moved=[(row, column), change]))
        return possible_moves

    def get_strength(self):
        pass
