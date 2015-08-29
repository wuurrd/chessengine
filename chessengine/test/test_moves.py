# -*-coding: utf-8-*-
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
        moves = chess_position._get_pawn_moves(position[4][0], 4, 0, color=WHITE)
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
        moves = chess_position._get_pawn_moves(position[4][7], 4, 7, color=WHITE)
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
        moves = chess_position._get_pawn_moves(position[6][1], 6, 1, color=BLACK)
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
        moves = chess_position._get_pawn_moves(position[6][1], 6, 1, color=BLACK)
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
        moves = chess_position._get_pawn_moves(position[3][0], 3, 0, color=BLACK)
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
        moves = chess_position._get_pawn_moves(position[3][7], 3, 7, color=BLACK)
        self.assertEquals(len(moves), 2, moves)
        forward_move = moves[0]
        self.assertEquals(forward_move.position[2][7], (PAWN, BLACK))
        en_passent_move = moves[1]
        self.assertOnlyPiece(en_passent_move, (PAWN, BLACK), 2, 6)
