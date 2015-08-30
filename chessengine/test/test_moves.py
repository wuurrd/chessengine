# -*-coding: utf-8-*-
# pylint: disable=W0212
import unittest
from chessengine.base import ChessPosition

BLACK = ChessPosition.BLACK
WHITE = ChessPosition.WHITE

QUEEN = ChessPosition.QUEEN
KING = ChessPosition.KING
HORSE = ChessPosition.HORSE
BISHOP = ChessPosition.BISHOP
PAWN = ChessPosition.PAWN
TOWER = ChessPosition.TOWER

class TestPawnMoves(unittest.TestCase):
    def assertOnlyPiece(self, board, expected_piece, x, y):
        for i, row in enumerate(board.position):
            for j, piece in enumerate(row):
                if i == x and j == y:
                    self.assertEquals(piece, expected_piece)
                else:
                    self.assertEquals(piece, None)

    def test_white_pawn_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, (PAWN, WHITE), None, None, None, None, None, None],
            [(QUEEN, BLACK), (PAWN, BLACK), (PAWN, WHITE), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 1)
        moves = chess_position._get_pawn_moves(position[1][1], 1, 1)
        self.assertEquals(len(moves), 1, moves)
        attack_move = moves[0]
        self.assertEquals(attack_move.position[1][1], None)
        self.assertEquals(attack_move.position[2][0], (PAWN, WHITE))

        position = [
            [None, None, None, None, None, None, None, None],
            [None, (PAWN, WHITE), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_pawn_moves(position[1][1], 1, 1)
        self.assertEquals(len(moves), 2, moves)
        attack_move = moves[0]
        self.assertOnlyPiece(attack_move, (PAWN, WHITE), 2, 1)
        attack_move = moves[1]
        self.assertOnlyPiece(attack_move, (PAWN, WHITE), 3, 1)

    def test_white_upgrade_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, (PAWN, WHITE), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 2)
        moves = chess_position._get_pawn_moves(position[6][1], 6, 1)
        self.assertEquals(len(moves), 4, moves)
        attack_move = moves[0]
        self.assertOnlyPiece(attack_move, (HORSE, WHITE), 7, 1)
        attack_move = moves[1]
        self.assertOnlyPiece(attack_move, (BISHOP, WHITE), 7, 1)
        attack_move = moves[2]
        self.assertOnlyPiece(attack_move, (TOWER, WHITE), 7, 1)
        attack_move = moves[3]
        self.assertOnlyPiece(attack_move, (QUEEN, WHITE), 7, 1)

        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, (PAWN, WHITE), None, None, None, None, None, None],
            [(QUEEN, WHITE), (KING, WHITE), (PAWN, BLACK), None, None, None, None, None]]
        chess_position = ChessPosition(position, 2)
        moves = chess_position._get_pawn_moves(position[6][1], 6, 1)
        self.assertEquals(len(moves), 4, moves)
        attack_move = moves[0]
        self.assertEquals(attack_move.position[7][2], (HORSE, WHITE))
        attack_move = moves[1]
        self.assertEquals(attack_move.position[7][2], (BISHOP, WHITE))
        attack_move = moves[2]
        self.assertEquals(attack_move.position[7][2], (TOWER, WHITE))
        attack_move = moves[3]
        self.assertEquals(attack_move.position[7][2], (QUEEN, WHITE))

        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, (PAWN, WHITE), None, None, None, None, None, None],
            [(QUEEN, BLACK), (KING, WHITE), (HORSE, WHITE), None, None, None, None, None]]
        chess_position = ChessPosition(position, 2)
        moves = chess_position._get_pawn_moves(position[6][1], 6, 1)
        self.assertEquals(len(moves), 4, moves)
        attack_move = moves[0]
        self.assertEquals(attack_move.position[7][0], (HORSE, WHITE))
        attack_move = moves[1]
        self.assertEquals(attack_move.position[7][0], (BISHOP, WHITE))
        attack_move = moves[2]
        self.assertEquals(attack_move.position[7][0], (TOWER, WHITE))
        attack_move = moves[3]
        self.assertEquals(attack_move.position[7][0], (QUEEN, WHITE))

    def test_white_en_passent_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [(PAWN, WHITE), (PAWN, BLACK), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 2, piece_moved=[(6, 1), (4, 1)])
        moves = chess_position._get_pawn_moves(position[4][0], 4, 0)
        self.assertEquals(len(moves), 2, moves)
        forward_move = moves[0]
        self.assertEquals(forward_move.position[5][0], (PAWN, WHITE))
        en_passent_move = moves[1]
        self.assertOnlyPiece(en_passent_move, (PAWN, WHITE), 5, 1)
        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, (PAWN, BLACK), (PAWN, WHITE)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 2, piece_moved=[(6, 6), (4, 6)])
        moves = chess_position._get_pawn_moves(position[4][7], 4, 7)
        self.assertEquals(len(moves), 2, moves)
        forward_move = moves[0]
        self.assertEquals(forward_move.position[5][7], (PAWN, WHITE))
        en_passent_move = moves[1]
        self.assertOnlyPiece(en_passent_move, (PAWN, WHITE), 5, 6)

    def test_black_pawn_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [(PAWN, WHITE), (PAWN, WHITE), (PAWN, WHITE), None, None, None, None, None],
            [None, (PAWN, BLACK), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 2)
        moves = chess_position._get_pawn_moves(position[6][1], 6, 1)
        self.assertEquals(len(moves), 2, moves)
        attack_move = moves[0]
        self.assertEquals(attack_move.position[6][1], None)
        self.assertEquals(attack_move.position[5][0], (PAWN, BLACK))
        attack_move = moves[1]
        self.assertEquals(attack_move.position[6][1], None)
        self.assertEquals(attack_move.position[5][2], (PAWN, BLACK))

        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, (PAWN, BLACK), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 1)
        moves = chess_position._get_pawn_moves(position[6][1], 6, 1)
        self.assertEquals(len(moves), 2, moves)
        attack_move = moves[0]
        self.assertOnlyPiece(attack_move, (PAWN, BLACK), 5, 1)
        attack_move = moves[1]
        self.assertOnlyPiece(attack_move, (PAWN, BLACK), 4, 1)


    def test_black_en_passent_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [(PAWN, BLACK), (PAWN, WHITE), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 2, piece_moved=[(1, 1), (3, 1)])
        moves = chess_position._get_pawn_moves(position[3][0], 3, 0)
        self.assertEquals(len(moves), 2, moves)
        forward_move = moves[0]
        self.assertEquals(forward_move.position[2][0], (PAWN, BLACK))
        en_passent_move = moves[1]
        self.assertOnlyPiece(en_passent_move, (PAWN, BLACK), 2, 1)
        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, (PAWN, WHITE), (PAWN, BLACK)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 2, piece_moved=[(1, 6), (3, 6)])
        moves = chess_position._get_pawn_moves(position[3][7], 3, 7)
        self.assertEquals(len(moves), 2, moves)
        forward_move = moves[0]
        self.assertEquals(forward_move.position[2][7], (PAWN, BLACK))
        en_passent_move = moves[1]
        self.assertOnlyPiece(en_passent_move, (PAWN, BLACK), 2, 6)

class TestKnightMoves(unittest.TestCase):
    def assertOnlyPiece(self, board, expected_piece, x, y):
        for i, row in enumerate(board.position):
            for j, piece in enumerate(row):
                if i == x and j == y:
                    self.assertEquals(piece, expected_piece)
                else:
                    self.assertEquals(piece, None)

    def assertExistsPiece(self, board, expected_piece, x, y):
        self.assertEquals(board.position[x][y], expected_piece)

    def test_middle_knight_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, (HORSE, WHITE), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_knight_moves(position[1][1], 1, 1)
        self.assertEquals(len(moves), 4, moves)
        move = moves[0]
        self.assertOnlyPiece(move, (HORSE, WHITE), 3, 2)
        move = moves[1]
        self.assertOnlyPiece(move, (HORSE, WHITE), 2, 3)
        move = moves[2]
        self.assertOnlyPiece(move, (HORSE, WHITE), 0, 3)
        move = moves[3]
        self.assertOnlyPiece(move, (HORSE, WHITE), 3, 0)

    def test_blocked_moves(self):
        position = [
            [None, None, None, (HORSE, WHITE), None, None, None, None],
            [None, (HORSE, WHITE), None, None, None, None, None, None],
            [None, None, None, (HORSE, WHITE), None, None, None, None],
            [None, None, (HORSE, WHITE), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_knight_moves(position[1][1], 1, 1)
        self.assertEquals(len(moves), 1, moves)
        move = moves[0]
        self.assertExistsPiece(move, (HORSE, WHITE), 3, 0)

    def test_capture_moves(self):
        position = [
            [None, None, None, (HORSE, WHITE), None, None, None, None],
            [None, (HORSE, WHITE), None, None, None, None, None, None],
            [None, None, None, (HORSE, WHITE), None, None, None, None],
            [(HORSE, BLACK), None, (HORSE, WHITE), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_knight_moves(position[1][1], 1, 1)
        self.assertEquals(len(moves), 1, moves)
        move = moves[0]
        self.assertExistsPiece(move, (HORSE, WHITE), 3, 0)

class TestBishopMoves(unittest.TestCase):
    def assertOnlyPiece(self, board, expected_piece, x, y):
        for i, row in enumerate(board.position):
            for j, piece in enumerate(row):
                if i == x and j == y:
                    self.assertEquals(piece, expected_piece)
                else:
                    self.assertEquals(piece, None)

    def assertExistsPiece(self, board, expected_piece, x, y):
        self.assertEquals(board.position[x][y], expected_piece)


    def test_blocked_moves(self):
        position = [
            [(BISHOP, WHITE), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, (BISHOP, WHITE), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)

        moves = chess_position._get_bishop_moves(position[0][0], 0, 0)
        self.assertEquals(len(moves), 1, moves)
        move = moves[0]
        self.assertExistsPiece(move, (BISHOP, WHITE), 1, 1)
        position = [
            [(BISHOP, WHITE), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, (BISHOP, BLACK), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_bishop_moves(position[0][0], 0, 0)
        self.assertEquals(len(moves), 2, moves)
        move = moves[0]
        self.assertExistsPiece(move, (BISHOP, WHITE), 1, 1)
        move = moves[1]
        self.assertOnlyPiece(move, (BISHOP, WHITE), 2, 2)

    def test_all_side_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, (BISHOP, BLACK), None, (BISHOP, BLACK), None, None, None, None],
            [None, None, (BISHOP, WHITE), None, None, None, None, None],
            [None, (BISHOP, BLACK), None, (BISHOP, BLACK), None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)

        moves = chess_position._get_bishop_moves(position[2][2], 2, 2)
        self.assertEquals(len(moves), 4, moves)
        move = moves[0]
        self.assertExistsPiece(move, (BISHOP, WHITE), 3, 3)
        move = moves[1]
        self.assertExistsPiece(move, (BISHOP, WHITE), 3, 1)
        move = moves[2]
        self.assertExistsPiece(move, (BISHOP, WHITE), 1, 3)
        move = moves[3]
        self.assertExistsPiece(move, (BISHOP, WHITE), 1, 1)

class TestTowerMoves(unittest.TestCase):
    def assertOnlyPiece(self, board, expected_piece, x, y):
        for i, row in enumerate(board.position):
            for j, piece in enumerate(row):
                if i == x and j == y:
                    self.assertEquals(piece, expected_piece)
                else:
                    self.assertEquals(piece, None)

    def assertExistsPiece(self, board, expected_piece, x, y):
        self.assertEquals(board.position[x][y], expected_piece)


    def test_blocked_moves(self):
        position = [
            [(TOWER, WHITE), (TOWER, WHITE), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [(TOWER, WHITE), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_tower_moves(position[0][0], 0, 0)
        self.assertEquals(len(moves), 1, moves)
        move = moves[0]
        self.assertExistsPiece(move, (TOWER, WHITE), 1, 0)
        position = [
            [(TOWER, WHITE), (TOWER, WHITE), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [(TOWER, BLACK), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_tower_moves(position[0][0], 0, 0)
        self.assertEquals(len(moves), 2, moves)
        move = moves[0]
        self.assertExistsPiece(move, (TOWER, WHITE), 1, 0)
        move = moves[1]
        self.assertExistsPiece(move, (TOWER, WHITE), 2, 0)

    def test_all_side_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, None, (TOWER, BLACK), None, None, None, None, None],
            [None, (TOWER, BLACK), (TOWER, WHITE), (TOWER, BLACK), None, None, None, None],
            [None, None, (TOWER, BLACK), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)

        moves = chess_position._get_tower_moves(position[2][2], 2, 2)
        self.assertEquals(len(moves), 4, moves)
        move = moves[0]
        self.assertExistsPiece(move, (TOWER, WHITE), 3, 2)
        move = moves[1]
        self.assertExistsPiece(move, (TOWER, WHITE), 2, 3)
        move = moves[2]
        self.assertExistsPiece(move, (TOWER, WHITE), 1, 2)
        move = moves[3]
        self.assertExistsPiece(move, (TOWER, WHITE), 2, 1)

class TestQueenMoves(unittest.TestCase):
    def assertOnlyPiece(self, board, expected_piece, x, y):
        for i, row in enumerate(board.position):
            for j, piece in enumerate(row):
                if i == x and j == y:
                    self.assertEquals(piece, expected_piece)
                else:
                    self.assertEquals(piece, None)

    def assertExistsPiece(self, board, expected_piece, x, y):
        self.assertEquals(board.position[x][y], expected_piece)


    def test_blocked_moves(self):
        position = [
            [(QUEEN, WHITE), (TOWER, WHITE), None, None, None, None, None, None],
            [None, (TOWER, WHITE), None, None, None, None, None, None],
            [(TOWER, WHITE), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_moves(position[0][0], 0, 0)
        self.assertEquals(len(moves), 1, moves)
        move = moves[0]
        self.assertExistsPiece(move, (QUEEN, WHITE), 1, 0)
        position = [
            [(QUEEN, WHITE), (TOWER, WHITE), None, None, None, None, None, None],
            [(TOWER, WHITE), None, None, None, None, None, None, None],
            [None, None, (BISHOP, WHITE), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)

        moves = chess_position._get_moves(position[0][0], 0, 0)
        self.assertEquals(len(moves), 1, moves)
        move = moves[0]
        self.assertExistsPiece(move, (QUEEN, WHITE), 1, 1)

    def test_all_side_moves(self):
        position = [
            [None, None, None, None, None, None, None, None],
            [None, (TOWER, BLACK), (TOWER, BLACK), (TOWER, BLACK), None, None, None, None],
            [None, (TOWER, BLACK), (QUEEN, WHITE), (TOWER, BLACK), None, None, None, None],
            [None, (TOWER, BLACK), (TOWER, BLACK), (TOWER, BLACK), None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)

        moves = chess_position._get_moves(position[2][2], 2, 2)
        self.assertEquals(len(moves), 8, moves)

class TestKingMoves(unittest.TestCase):
    def fen_to_board(self, fen_string):
        position = []
        char_map = {
            'k': (KING, WHITE),
            'q': (QUEEN, WHITE),
            'r': (TOWER, WHITE),
            'b': (BISHOP, WHITE),
            'n': (HORSE, WHITE),
            'p': (PAWN, WHITE),
        }
        char_map.update({k.upper(): (piece[0], BLACK) for k, piece in char_map.items()})
        data = []
        for row in fen_string.split('/'):
            current_row = []
            for char in row:
                if char.isdigit():
                    skips = int(char)
                    current_row.extend([None] * skips)
                else:
                    current_row.append(char_map[char])
            data.append(current_row)
        return data

    def assertOnlyPiece(self, board, expected_piece, x, y):
        for i, row in enumerate(board.position):
            for j, piece in enumerate(row):
                if i == x and j == y:
                    self.assertEquals(piece, expected_piece)
                else:
                    self.assertEquals(piece, None)

    def assertExistsPiece(self, board, expected_piece, x, y):
        self.assertEquals(board.position[x][y], expected_piece)


    def test_do_not_put_king_in_mate(self):
        position = [
            [(KING, WHITE), (BISHOP, WHITE), None, None, None, None, None, None],
            [None, (QUEEN, BLACK), None, None, None, None, None, None],
            [(TOWER, WHITE), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)
        moves = chess_position._get_moves(position[0][0], 0, 0)
        self.assertEquals(len(moves), 1, moves)
        move = moves[0]
        self.assertExistsPiece(move, (KING, WHITE), 1, 1)

    def test_blocked_moves(self):
        position = [
            [(KING, WHITE), (TOWER, WHITE), None, None, None, None, None, None],
            [(TOWER, WHITE), None, None, None, None, None, None, None],
            [None, None, (BISHOP, WHITE), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        chess_position = ChessPosition(position, 3)

        moves = chess_position._get_moves(position[0][0], 0, 0)
        self.assertEquals(len(moves), 1, moves)
        move = moves[0]
        self.assertExistsPiece(move, (KING, WHITE), 1, 1)

    def test_king_bug(self):
        position = self.fen_to_board('n1n5/PPPk4/8/8/8/8/4Kppp/5N1N')
        chess_position = ChessPosition(position, 2)
        king_moves = chess_position._get_moves(position[6][4], 6, 4)
        self.assertEquals(len(king_moves), 6)

class TestPerft(unittest.TestCase):
    def fen_to_board(self, fen_string):
        char_map = {
            'k': (KING, WHITE),
            'q': (QUEEN, WHITE),
            'r': (TOWER, WHITE),
            'b': (BISHOP, WHITE),
            'n': (HORSE, WHITE),
            'p': (PAWN, WHITE),
        }
        char_map.update({k.upper(): (piece[0], BLACK) for k, piece in char_map.items()})
        data = []
        for row in fen_string.split('/'):
            current_row = []
            for char in row:
                if char.isdigit():
                    skips = int(char)
                    current_row.extend([None] * skips)
                else:
                    current_row.append(char_map[char])
            data.append(current_row)
        return data

    def test_starting_position(self):
        position = self.fen_to_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        chess_position = ChessPosition(position, 1)
        moves = chess_position.get_moves_for_depth(1)
        self.assertEqual(len(moves), 20)
        moves = chess_position.get_moves_for_depth(2)
        self.assertEqual(len(moves), 420)
        moves = chess_position.get_moves_for_depth(3)
        self.assertEqual(len(moves), 9322)

    def test_promotion_errors(self):
        position = self.fen_to_board('n1n5/PPPk4/8/8/8/8/4Kppp/5N1N')
        chess_position = ChessPosition(position, 1)
        moves = chess_position.get_moves_for_depth(1)
        self.assertEqual(len(moves), 24)
        # moves = chess_position.get_moves_for_depth(2)
        # self.assertEqual(len(moves), 566)

    def test_king_loose(self):
        position = self.fen_to_board('4k3/8/8/8/8/8/8/4K2R')
        chess_position = ChessPosition(position, 2)
        moves = chess_position.get_moves()
        self.assertEqual(len(moves), 14)

    def test_king_check(self):
        position = self.fen_to_board('k7/Q7/7b/8/8/8/8/8')
        chess_position = ChessPosition(position, 2)
        moves = chess_position.get_moves()
        self.assertEqual(len(moves), 1)
