"""
Room controller - manages game rooms
"""

from server.dao.user_dao import UserDAO
from shared.utils import log
from shared.constants import MIN_ROOM_ID

class Room:
    """Game room managing two players"""
    
    # Class variable for room ID counter
    _next_room_id = MIN_ROOM_ID
    
    def __init__(self, user1_thread):
        """
        Initialize room with first user
        
        Args:
            user1_thread: ServerThread of first player
        """
        self.id = Room._next_room_id
        Room._next_room_id += 1
        
        self.user1 = user1_thread
        self.user2 = None
        self.password = " "  # Default no password
        self.user_dao = UserDAO()
        
        log(f"Room created: ID={self.id}")
    
    def get_id(self):
        return self.id
    
    def get_user1(self):
        return self.user1
    
    def get_user2(self):
        return self.user2
    
    def set_user2(self, user2_thread):
        """Set second player"""
        self.user2 = user2_thread
    
    def get_password(self):
        return self.password
    
    def set_password(self, password):
        """Set room password"""
        self.password = password
    
    def get_number_of_user(self):
        """Get number of users in room"""
        return 1 if self.user2 is None else 2
    
    def broadcast(self, message):
        """
        Send message to both players
        
        Args:
            message: Message string
        """
        try:
            if self.user1:
                self.user1.write(message)
            if self.user2:
                self.user2.write(message)
        except Exception as e:
            log(f"Broadcast error in room {self.id}: {e}", "ERROR")
    
    def get_competitor_id(self, client_number):
        """
        Get competitor's user ID
        
        Args:
            client_number: Client number of requesting user
        
        Returns:
            Competitor's user ID
        """
        if self.user1 and self.user1.get_client_number() == client_number:
            return self.user2.get_user().get_id() if self.user2 else None
        return self.user1.get_user().get_id() if self.user1 else None
    
    def get_competitor(self, client_number):
        """
        Get competitor's ServerThread
        
        Args:
            client_number: Client number of requesting user
        
        Returns:
            ServerThread of competitor
        """
        if self.user1 and self.user1.get_client_number() == client_number:
            return self.user2
        return self.user1
    
    def set_users_to_playing(self):
        """Set both users to playing status"""
        if self.user1 and self.user1.get_user():
            self.user_dao.update_to_playing(self.user1.get_user().get_id())
        if self.user2 and self.user2.get_user():
            self.user_dao.update_to_playing(self.user2.get_user().get_id())
    
    def set_users_to_not_playing(self):
        """Set both users to not playing status"""
        if self.user1 and self.user1.get_user():
            self.user_dao.update_to_not_playing(self.user1.get_user().get_id())
        if self.user2 and self.user2.get_user():
            self.user_dao.update_to_not_playing(self.user2.get_user().get_id())
    
    def increase_number_of_game(self):
        """Increment game count for both players"""
        if self.user1 and self.user1.get_user():
            self.user_dao.add_game(self.user1.get_user().get_id())
        if self.user2 and self.user2.get_user():
            self.user_dao.add_game(self.user2.get_user().get_id())
    
    def increase_number_of_draw(self):
        """Increment draw count for both players"""
        if self.user1 and self.user1.get_user():
            self.user_dao.add_draw_game(self.user1.get_user().get_id())
        if self.user2 and self.user2.get_user():
            self.user_dao.add_draw_game(self.user2.get_user().get_id())
    
    def decrease_number_of_game(self):
        """Decrement game count for both players"""
        if self.user1 and self.user1.get_user():
            self.user_dao.decrease_game(self.user1.get_user().get_id())
        if self.user2 and self.user2.get_user():
            self.user_dao.decrease_game(self.user2.get_user().get_id())
    
    def __str__(self):
        return f"Room(id={self.id}, users={self.get_number_of_user()})"
