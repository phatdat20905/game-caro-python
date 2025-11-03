"""
Game Logic - Core game rules and AI
"""

from shared.constants import *
from shared.point import Point
import random

class GameLogic:
    """Core game logic for Caro game"""
    
    @staticmethod
    def check_win(board, x, y, player):
        """
        Check if the move at (x, y) creates a winning condition
        
        Args:
            board: 2D array representing the game board
            x: Row position
            y: Column position
            player: Player marker (1 for X, 2 for O)
        
        Returns:
            True if this move wins the game, False otherwise
        """
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal \
            (1, -1),  # Diagonal /
        ]
        
        for dx, dy in directions:
            count = 1  # Count the current piece
            
            # Check in positive direction
            count += GameLogic._count_consecutive(board, x, y, dx, dy, player)
            
            # Check in negative direction
            count += GameLogic._count_consecutive(board, x, y, -dx, -dy, player)
            
            if count >= WIN_CONDITION:
                return True
        
        return False
    
    @staticmethod
    def _count_consecutive(board, x, y, dx, dy, player):
        """
        Count consecutive pieces in one direction
        
        Args:
            board: 2D array representing the game board
            x, y: Starting position
            dx, dy: Direction to check
            player: Player marker
        
        Returns:
            Number of consecutive pieces (not including starting position)
        """
        count = 0
        nx, ny = x + dx, y + dy
        
        while (0 <= nx < BOARD_SIZE and 
               0 <= ny < BOARD_SIZE and 
               board[nx][ny] == player):
            count += 1
            nx += dx
            ny += dy
        
        return count
    
    @staticmethod
    def get_winning_cells(board, x, y, player):
        """
        Get the cells that form the winning line
        
        Args:
            board: 2D array representing the game board
            x, y: Position of the winning move
            player: Player marker
        
        Returns:
            List of Point objects forming the winning line, or empty list
        """
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal \
            (1, -1),  # Diagonal /
        ]
        
        for dx, dy in directions:
            cells = [Point(x, y)]
            
            # Collect in positive direction
            nx, ny = x + dx, y + dy
            while (0 <= nx < BOARD_SIZE and 
                   0 <= ny < BOARD_SIZE and 
                   board[nx][ny] == player):
                cells.append(Point(nx, ny))
                nx += dx
                ny += dy
            
            # Collect in negative direction
            nx, ny = x - dx, y - dy
            while (0 <= nx < BOARD_SIZE and 
                   0 <= ny < BOARD_SIZE and 
                   board[nx][ny] == player):
                cells.append(Point(nx, ny))
                nx -= dx
                ny -= dy
            
            if len(cells) >= WIN_CONDITION:
                return cells
        
        return []
    
    @staticmethod
    def is_board_full(board):
        """
        Check if the board is full (draw condition)
        
        Args:
            board: 2D array representing the game board
        
        Returns:
            True if board is full, False otherwise
        """
        for row in board:
            for cell in row:
                if cell == 0:  # Empty cell
                    return False
        return True
    
    @staticmethod
    def get_valid_moves(board):
        """
        Get all valid (empty) moves on the board
        
        Args:
            board: 2D array representing the game board
        
        Returns:
            List of Point objects representing valid moves
        """
        valid_moves = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == 0:
                    valid_moves.append(Point(x, y))
        return valid_moves


class SimpleAI:
    """Simple AI opponent for practice mode"""
    
    @staticmethod
    def get_best_move(board, ai_player, human_player):
        """
        Get the best move for AI using simple strategy
        
        Strategy:
        1. Check if AI can win in next move
        2. Check if need to block human from winning
        3. Look for good offensive positions
        4. Random move near existing pieces
        
        Args:
            board: 2D array representing the game board
            ai_player: AI's player marker (1 or 2)
            human_player: Human's player marker (1 or 2)
        
        Returns:
            Point object representing the best move
        """
        # 1. Check if AI can win
        winning_move = SimpleAI._find_winning_move(board, ai_player)
        if winning_move:
            return winning_move
        
        # 2. Block human from winning
        blocking_move = SimpleAI._find_winning_move(board, human_player)
        if blocking_move:
            return blocking_move
        
        # 3. Find offensive move (create threat)
        offensive_move = SimpleAI._find_offensive_move(board, ai_player)
        if offensive_move:
            return offensive_move
        
        # 4. Move near existing pieces
        nearby_move = SimpleAI._find_nearby_move(board)
        if nearby_move:
            return nearby_move
        
        # 5. Random move (fallback)
        valid_moves = GameLogic.get_valid_moves(board)
        if valid_moves:
            return random.choice(valid_moves)
        
        return None
    
    @staticmethod
    def _find_winning_move(board, player):
        """Find a move that wins the game"""
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == 0:
                    # Try this move
                    board[x][y] = player
                    if GameLogic.check_win(board, x, y, player):
                        board[x][y] = 0  # Undo
                        return Point(x, y)
                    board[x][y] = 0  # Undo
        return None
    
    @staticmethod
    def _find_offensive_move(board, player):
        """Find a move that creates a strong threat (3 in a row)"""
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == 0:
                    # Try this move
                    board[x][y] = player
                    threat_count = SimpleAI._count_threats(board, x, y, player)
                    board[x][y] = 0  # Undo
                    
                    if threat_count >= 3:  # Creates 3+ in a row
                        return Point(x, y)
        return None
    
    @staticmethod
    def _count_threats(board, x, y, player):
        """Count consecutive pieces for threat evaluation"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        max_count = 0
        
        for dx, dy in directions:
            count = 1
            count += GameLogic._count_consecutive(board, x, y, dx, dy, player)
            count += GameLogic._count_consecutive(board, x, y, -dx, -dy, player)
            max_count = max(max_count, count)
        
        return max_count
    
    @staticmethod
    def _find_nearby_move(board):
        """Find a move near existing pieces"""
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] != 0:
                    # Check adjacent cells
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < BOARD_SIZE and 
                                0 <= ny < BOARD_SIZE and 
                                board[nx][ny] == 0):
                                return Point(nx, ny)
        return None
