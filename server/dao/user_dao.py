"""
User Data Access Object
"""

from server.dao.database import get_database
from shared.user import User
from shared.utils import log, calculate_mark

class UserDAO:
    """User database operations"""
    
    def __init__(self):
        self.db = get_database()
    
    def verify_user(self, username, password):
        """
        Verify user credentials
        
        Args:
            username: Username
            password: Password
        
        Returns:
            User object if verified, None otherwise
        """
        query = "SELECT * FROM user WHERE Username = ? AND Password = ?"
        row = self.db.fetch_one(query, (username, password))
        
        if row:
            user = User(
                user_id=row['ID'],
                username=row['Username'],
                password=row['Password'],
                nickname=row['Nickname'],
                avatar=row['Avatar'],
                number_of_game=row['NumberOfGame'],
                number_of_win=row['NumberOfWin'],
                number_of_draw=row['NumberOfDraw'],
                is_online=bool(row['IsOnline']),
                is_playing=bool(row['IsPlaying']),
                rank=self.get_rank(row['ID'])
            )
            return user
        return None
    
    def add_user(self, username, password, nickname, avatar):
        """
        Add new user
        
        Args:
            username: Username
            password: Password
            nickname: Nickname
            avatar: Avatar ID
        
        Returns:
            True if successful, False otherwise
        """
        query = "INSERT INTO user (Username, Password, Nickname, Avatar) VALUES (?, ?, ?, ?)"
        return self.db.execute_query(query, (username, password, nickname, avatar))
    
    def check_duplicated(self, username):
        """
        Check if username already exists
        
        Args:
            username: Username to check
        
        Returns:
            True if exists, False otherwise
        """
        query = "SELECT * FROM user WHERE Username = ?"
        row = self.db.fetch_one(query, (username,))
        return row is not None
    
    def check_is_banned(self, user_id):
        """
        Check if user is banned
        
        Args:
            user_id: User ID
        
        Returns:
            True if banned, False otherwise
        """
        query = "SELECT * FROM banned_user WHERE ID_User = ?"
        row = self.db.fetch_one(query, (user_id,))
        return row is not None
    
    def update_banned_status(self, user_id, banned, reason=""):
        """
        Update user banned status
        
        Args:
            user_id: User ID
            banned: True to ban, False to unban
            reason: Ban reason
        
        Returns:
            True if successful
        """
        if banned:
            query = "INSERT OR REPLACE INTO banned_user (ID_User, Reason) VALUES (?, ?)"
            return self.db.execute_query(query, (user_id, reason))
        else:
            query = "DELETE FROM banned_user WHERE ID_User = ?"
            return self.db.execute_query(query, (user_id,))
    
    def update_to_online(self, user_id):
        """Set user status to online"""
        query = "UPDATE user SET IsOnline = 1 WHERE ID = ?"
        return self.db.execute_query(query, (user_id,))
    
    def update_to_offline(self, user_id):
        """Set user status to offline"""
        query = "UPDATE user SET IsOnline = 0 WHERE ID = ?"
        return self.db.execute_query(query, (user_id,))
    
    def update_to_playing(self, user_id):
        """Set user status to playing"""
        query = "UPDATE user SET IsPlaying = 1 WHERE ID = ?"
        return self.db.execute_query(query, (user_id,))
    
    def update_to_not_playing(self, user_id):
        """Set user status to not playing"""
        query = "UPDATE user SET IsPlaying = 0 WHERE ID = ?"
        return self.db.execute_query(query, (user_id,))
    
    def get_list_friend(self, user_id):
        """
        Get list of friends for a user
        
        Args:
            user_id: User ID
        
        Returns:
            List of User objects
        """
        query = """
            SELECT User.ID, User.Nickname, User.IsOnline, User.IsPlaying
            FROM user
            WHERE User.ID IN (
                SELECT ID_User1 FROM friend WHERE ID_User2 = ?
            ) OR User.ID IN (
                SELECT ID_User2 FROM friend WHERE ID_User1 = ?
            )
        """
        rows = self.db.fetch_all(query, (user_id, user_id))
        
        friends = []
        for row in rows:
            user = User(
                user_id=row['ID'],
                nickname=row['Nickname'],
                is_online=bool(row['IsOnline']),
                is_playing=bool(row['IsPlaying'])
            )
            friends.append(user)
        
        # Sort: online first, then playing
        friends.sort(key=lambda u: (not u.is_online, not u.is_playing))
        return friends
    
    def check_is_friend(self, user_id1, user_id2):
        """Check if two users are friends"""
        query = """
            SELECT * FROM friend 
            WHERE (ID_User1 = ? AND ID_User2 = ?) 
               OR (ID_User1 = ? AND ID_User2 = ?)
        """
        row = self.db.fetch_one(query, (user_id1, user_id2, user_id2, user_id1))
        return row is not None
    
    def make_friend(self, user_id1, user_id2):
        """Add friendship between two users"""
        query = "INSERT OR IGNORE INTO friend (ID_User1, ID_User2) VALUES (?, ?)"
        return self.db.execute_query(query, (user_id1, user_id2))
    
    def get_user_static_rank(self):
        """
        Get user ranking sorted by stats
        
        Returns:
            List of User objects sorted by rank
        """
        query = """
            SELECT * FROM user 
            ORDER BY NumberOfWin DESC, NumberOfGame ASC
            LIMIT 100
        """
        rows = self.db.fetch_all(query)
        
        users = []
        for row in rows:
            user = User(
                user_id=row['ID'],
                username=row['Username'],
                password=row['Password'],
                nickname=row['Nickname'],
                avatar=row['Avatar'],
                number_of_game=row['NumberOfGame'],
                number_of_win=row['NumberOfWin'],
                number_of_draw=row['NumberOfDraw'],
                rank=self.get_rank(row['ID'])
            )
            users.append(user)
        
        return users
    
    def get_nickname_by_id(self, user_id):
        """Get nickname by user ID"""
        query = "SELECT Nickname FROM user WHERE ID = ?"
        row = self.db.fetch_one(query, (user_id,))
        return row['Nickname'] if row else ""
    
    def get_rank(self, user_id):
        """
        Calculate user rank based on wins
        
        Args:
            user_id: User ID
        
        Returns:
            Rank position (1-based)
        """
        query = """
            SELECT COUNT(*) + 1 as rank
            FROM user
            WHERE NumberOfWin > (
                SELECT NumberOfWin FROM user WHERE ID = ?
            )
        """
        row = self.db.fetch_one(query, (user_id,))
        return row['rank'] if row else 0
    
    def add_game(self, user_id):
        """Increment user's game count"""
        query = "UPDATE user SET NumberOfGame = NumberOfGame + 1 WHERE ID = ?"
        return self.db.execute_query(query, (user_id,))
    
    def decrease_game(self, user_id):
        """Decrement user's game count"""
        query = "UPDATE user SET NumberOfGame = NumberOfGame - 1 WHERE ID = ? AND NumberOfGame > 0"
        return self.db.execute_query(query, (user_id,))
    
    def add_win_game(self, user_id):
        """Increment user's win count"""
        query = "UPDATE user SET NumberOfWin = NumberOfWin + 1 WHERE ID = ?"
        return self.db.execute_query(query, (user_id,))
    
    def add_draw_game(self, user_id):
        """Increment user's draw count"""
        query = "UPDATE user SET NumberOfDraw = NumberOfDraw + 1 WHERE ID = ?"
        return self.db.execute_query(query, (user_id,))
    
    def get_user_by_id(self, user_id):
        """Get full user info by ID"""
        query = "SELECT * FROM user WHERE ID = ?"
        row = self.db.fetch_one(query, (user_id,))
        
        if row:
            return User(
                user_id=row['ID'],
                username=row['Username'],
                password=row['Password'],
                nickname=row['Nickname'],
                avatar=row['Avatar'],
                number_of_game=row['NumberOfGame'],
                number_of_win=row['NumberOfWin'],
                number_of_draw=row['NumberOfDraw'],
                is_online=bool(row['IsOnline']),
                is_playing=bool(row['IsPlaying']),
                rank=self.get_rank(row['ID'])
            )
        return None
    
    def get_all_users(self):
        """Get all users"""
        query = "SELECT * FROM user"
        rows = self.db.fetch_all(query)
        
        users = []
        for row in rows:
            user = User(
                user_id=row['ID'],
                username=row['Username'],
                nickname=row['Nickname'],
                is_online=bool(row['IsOnline']),
                is_playing=bool(row['IsPlaying'])
            )
            users.append(user)
        
        return users
    
    def reset_all_users_status(self):
        """Reset all users to offline and not playing status"""
        query = "UPDATE user SET IsOnline = 0, IsPlaying = 0"
        return self.db.execute_query(query)
