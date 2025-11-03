"""
Configuration settings for the game
"""

from shared.constants import *

class Config:
    """Application configuration"""
    
    # Server settings
    SERVER_HOST = DEFAULT_SERVER_HOST
    SERVER_PORT = DEFAULT_SERVER_PORT
    
    # Game settings
    BOARD_SIZE = BOARD_SIZE
    WIN_CONDITION = WIN_CONDITION
    TURN_TIME_LIMIT = TURN_TIME_LIMIT
    CELL_SIZE = CELL_SIZE
    
    # Database
    DATABASE_PATH = DATABASE_PATH
    
    # Debug mode
    DEBUG = True
    
    @classmethod
    def get_server_address(cls):
        """Get server address tuple"""
        return (cls.SERVER_HOST, cls.SERVER_PORT)
    
    @classmethod
    def set_server_host(cls, host):
        """Set server host"""
        cls.SERVER_HOST = host
    
    @classmethod
    def set_server_port(cls, port):
        """Set server port"""
        cls.SERVER_PORT = port
