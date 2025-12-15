import unittest
from othello import OthelloGame

class TestOthelloGame(unittest.TestCase):
    def setUp(self):
        self.game = OthelloGame()

    def test_initial_board(self):
        board = self.game.get_board()
        self.assertEqual(board[3][3], 2)
        self.assertEqual(board[4][4], 2)
        self.assertEqual(board[3][4], 1)
        self.assertEqual(board[4][3], 1)
        self.assertEqual(self.game.current_turn, 1)

    def test_valid_move(self):
        # Black (1) should be able to place at (2, 3) flipping (3, 3) which is White (2)
        # Wait, (3,3) is 2. (3,4) is 1. (4,3) is 1. (4,4) is 2.
        # Initial:
        #   0 1 2 3 4 5 6 7
        # 3       W B
        # 4       B W
        # Black moves.
        # Valid moves for Black: (2,3), (3,2), (4,5), (5,4)
        
        moves = self.game.get_valid_moves()
        self.assertIn((2, 3), moves)
        
        success, msg = self.game.place_disc(2, 3)
        self.assertTrue(success)
        self.assertEqual(self.game.board[2][3], 1)
        self.assertEqual(self.game.board[3][3], 1) # Flanked piece should flip to 1
        self.assertEqual(self.game.current_turn, 2) # Turn should switch to White

    def test_invalid_move(self):
        success, msg = self.game.place_disc(0, 0)
        self.assertFalse(success)
        self.assertEqual(self.game.current_turn, 1)

if __name__ == '__main__':
    unittest.main()
