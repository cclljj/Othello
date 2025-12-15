
class OthelloGame:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_turn = 1 # 1 for Black, 2 for White
        self.game_over = False
        self.winner = None
        self._initialize_board()

    def _initialize_board(self, reset=True):
        if reset:
            self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # Standard Othello setup
        # 0: Empty, 1: Black, 2: White
        mid = self.rows // 2
        self.board[mid-1][mid-1] = 2
        self.board[mid][mid] = 2
        self.board[mid-1][mid] = 1
        self.board[mid][mid-1] = 1
        self.current_turn = 1
        self.game_over = False
        self.winner = None

    def get_board(self):
        return self.board

    def get_score(self):
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(2) for row in self.board)
        return {"black": black_count, "white": white_count}

    def place_disc(self, row, col):
        if self.game_over:
            return False, "Game is over"
        
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False, "Invalid position"
            
        if self.board[row][col] != 0:
            return False, "Cell occupied"

        flipped = self._get_flipped_discs(row, col, self.current_turn)
        if not flipped:
            return False, "Invalid move: Must flank opponent"

        # Apply move
        self.board[row][col] = self.current_turn
        for r, c in flipped:
            self.board[r][c] = self.current_turn

        # Switch turn
        self.current_turn = 3 - self.current_turn
        
        # Check if next player has valid moves
        if not self._has_valid_moves(self.current_turn):
            # Pass turn
            self.current_turn = 3 - self.current_turn
            # Check if original player has moves
            if not self._has_valid_moves(self.current_turn):
                self._end_game()
        
        return True, "Move successful"

    def _get_flipped_discs(self, row, col, player):
        opponent = 3 - player
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        flipped_total = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            temp_flipped = []
            while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == opponent:
                temp_flipped.append((r, c))
                r += dr
                c += dc
            
            # If we ended on the current player's piece, add the temp flipped to total
            if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                flipped_total.extend(temp_flipped)
                
        return flipped_total

    def _has_valid_moves(self, player):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    if self._get_flipped_discs(r, c, player):
                        return True
        return False

    def _end_game(self):
        self.game_over = True
        scores = self.get_score()
        if scores["black"] > scores["white"]:
            self.winner = 1
        elif scores["white"] > scores["black"]:
            self.winner = 2
        else:
            self.winner = 0 # Tie

    def reset_game(self):
        self._initialize_board()

    def get_valid_moves(self):
        moves = []
        if self.game_over:
            return moves
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    if self._get_flipped_discs(r, c, self.current_turn):
                        moves.append((r, c))
        return moves
