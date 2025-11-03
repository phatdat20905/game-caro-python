"""
User model class
"""

class User:
    """User model representing a player"""
    
    def __init__(self, user_id=None, username="", password="", nickname="", 
                 avatar="0", number_of_game=0, number_of_win=0, 
                 number_of_draw=0, is_online=False, is_playing=False, rank=0):
        self.id = user_id
        self.username = username
        self.password = password
        self.nickname = nickname
        self.avatar = avatar
        self.number_of_game = number_of_game
        self.number_of_win = number_of_win
        self.number_of_draw = number_of_draw
        self.is_online = is_online
        self.is_playing = is_playing
        self.rank = rank
    
    def get_id(self):
        return self.id
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_nickname(self):
        return self.nickname
    
    def get_avatar(self):
        return self.avatar
    
    def get_number_of_game(self):
        return self.number_of_game
    
    def get_number_of_win(self):
        return self.number_of_win
    
    def get_number_of_draw(self):
        return self.number_of_draw
    
    def get_is_online(self):
        return self.is_online
    
    def get_is_playing(self):
        return self.is_playing
    
    def get_rank(self):
        return self.rank
    
    def set_id(self, user_id):
        self.id = user_id
    
    def set_username(self, username):
        self.username = username
    
    def set_password(self, password):
        self.password = password
    
    def set_nickname(self, nickname):
        self.nickname = nickname
    
    def set_avatar(self, avatar):
        self.avatar = avatar
    
    def set_number_of_game(self, number):
        self.number_of_game = number
    
    def set_number_of_win(self, number):
        self.number_of_win = number
    
    def set_number_of_draw(self, number):
        self.number_of_draw = number
    
    def set_is_online(self, online):
        self.is_online = online
    
    def set_is_playing(self, playing):
        self.is_playing = playing
    
    def set_rank(self, rank):
        self.rank = rank
    
    def to_string(self):
        """Convert user to comma-separated string for network transmission"""
        return f"{self.id},{self.username},{self.password},{self.nickname},{self.avatar},{self.number_of_game},{self.number_of_win},{self.number_of_draw},{self.rank}"
    
    @staticmethod
    def from_string(data):
        """Create User from comma-separated string"""
        parts = data.split(',')
        if len(parts) >= 9:
            return User(
                user_id=int(parts[0]),
                username=parts[1],
                password=parts[2],
                nickname=parts[3],
                avatar=parts[4],
                number_of_game=int(parts[5]),
                number_of_win=int(parts[6]),
                number_of_draw=int(parts[7]),
                rank=int(parts[8])
            )
        return None
    
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, nickname={self.nickname})"
    
    def __repr__(self):
        return self.__str__()
