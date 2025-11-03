"""
Utility functions
"""

import os
import hashlib
from datetime import datetime

def get_project_root():
    """Get project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)

def get_asset_path(asset_type, filename):
    """
    Get full path to asset file
    
    Args:
        asset_type: 'avatar', 'game', 'icon', 'image', 'sound'
        filename: asset filename
    
    Returns:
        Full path to asset
    """
    root = get_project_root()
    return os.path.join(root, 'assets', asset_type, filename)

def hash_password(password):
    """
    Hash password using SHA-256
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    """
    Verify password against hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
    
    Returns:
        True if match, False otherwise
    """
    return hash_password(plain_password) == hashed_password

def get_timestamp():
    """Get current timestamp string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_win_ratio(wins, total_games):
    """
    Calculate win ratio as a number
    
    Args:
        wins: Number of wins
        total_games: Total number of games
    
    Returns:
        Win ratio as float (0-100)
    """
    if total_games == 0:
        return 0.0
    return (wins / total_games) * 100

def format_win_ratio(wins, total_games):
    """
    Calculate and format win ratio
    
    Args:
        wins: Number of wins
        total_games: Total number of games
    
    Returns:
        Formatted win ratio string (e.g., "75.50%")
    """
    if total_games == 0:
        return "-"
    ratio = calculate_win_ratio(wins, total_games)
    return f"{ratio:.2f}%"

def calculate_mark(total_games, wins):
    """
    Calculate player mark/score
    
    Args:
        total_games: Total number of games
        wins: Number of wins
    
    Returns:
        Calculated mark
    """
    return total_games + (wins * 10)

def get_rank_name(mark):
    """
    Get rank name based on mark
    
    Args:
        mark: Player mark/score
    
    Returns:
        Rank name string
    """
    from shared.constants import RANK_BRONZE, RANK_SILVER, RANK_GOLD
    
    if mark >= RANK_GOLD:
        return "Gold"
    elif mark >= RANK_SILVER:
        return "Silver"
    else:
        return "Bronze"

def parse_message(message):
    """
    Parse network message
    
    Args:
        message: Raw message string
    
    Returns:
        List of message parts
    """
    return message.split(',')

def create_message(*parts):
    """
    Create network message from parts
    
    Args:
        *parts: Message parts
    
    Returns:
        Formatted message string
    """
    return ','.join(str(part) for part in parts)

def safe_int(value, default=0):
    """
    Safely convert to int
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Integer value or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """
    Safely convert to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Float value or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def log(message, level="INFO"):
    """
    Simple logging function
    
    Args:
        message: Log message
        level: Log level (INFO, WARNING, ERROR, DEBUG)
    """
    timestamp = get_timestamp()
    print(f"[{timestamp}] [{level}] {message}")

def create_dirs_if_not_exists(path):
    """
    Create directories if they don't exist
    
    Args:
        path: Directory path
    """
    os.makedirs(path, exist_ok=True)
