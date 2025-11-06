"""
Socket handler for client - handles server communication
"""

import socket
import threading
from shared.user import User
from shared.utils import log, create_message
from shared.constants import *

class SocketHandle(threading.Thread):
    """Handles socket communication with server"""
    
    def __init__(self, client):
        """
        Initialize socket handler
        
        Args:
            client: Reference to Client instance
        """
        super().__init__(daemon=True)
        self.client = client
        self.socket = None
        self.running = False
    
    def connect(self, host, port):
        """
        Connect to server
        
        Args:
            host: Server host
            port: Server port
        
        Returns:
            True if connected, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.running = True
            log(f"Connected to server {host}:{port}")
            return True
        except Exception as e:
            log(f"Connection error: {e}", "ERROR")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        log("Disconnected from server")
    
    def write(self, message):
        """
        Send message to server
        
        Args:
            message: Message string
        """
        try:
            if self.socket:
                self.socket.send((message + '\n').encode(ENCODING))
        except Exception as e:
            log(f"Send error: {e}", "ERROR")
    
    def get_list_user(self, message_parts):
        """Parse user list from message"""
        users = []
        i = 1
        while i < len(message_parts):
            if i + 3 < len(message_parts):
                user = User(
                    user_id=int(message_parts[i]),
                    nickname=message_parts[i + 1],
                    is_online=(message_parts[i + 2] == "1"),
                    is_playing=(message_parts[i + 3] == "1")
                )
                users.append(user)
                i += 4
            else:
                break
        return users
    
    def get_list_rank(self, message_parts):
        """Parse rank list from message"""
        users = []
        i = 1
        while i < len(message_parts):
            if i + 8 < len(message_parts):
                user = User(
                    user_id=int(message_parts[i]),
                    username=message_parts[i + 1],
                    password=message_parts[i + 2],
                    nickname=message_parts[i + 3],
                    avatar=message_parts[i + 4],
                    number_of_game=int(message_parts[i + 5]),
                    number_of_win=int(message_parts[i + 6]),
                    number_of_draw=int(message_parts[i + 7]),
                    rank=int(message_parts[i + 8])
                )
                users.append(user)
                i += 9
            else:
                break
        return users
    
    def get_user_from_string(self, start, message_parts):
        """Parse single user from message"""
        if start + 8 < len(message_parts):
            return User(
                user_id=int(message_parts[start]),
                username=message_parts[start + 1],
                password=message_parts[start + 2],
                nickname=message_parts[start + 3],
                avatar=message_parts[start + 4],
                number_of_game=int(message_parts[start + 5]),
                number_of_win=int(message_parts[start + 6]),
                number_of_draw=int(message_parts[start + 7]),
                rank=int(message_parts[start + 8])
            )
        return None
    
    def run(self):
        """Main message receiving loop"""
        while self.running:
            try:
                message = self.socket.recv(BUFFER_SIZE).decode(ENCODING).strip()
                if not message:
                    break
                
                # Handle message
                self.handle_message(message)
            
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    log(f"Receive error: {e}", "ERROR")
                break
        
        self.disconnect()
    
    def handle_message(self, message):
        """Handle incoming message from server"""
        parts = message.split(',')
        if not parts:
            return
        
        command = parts[0]
        
        try:
            # Authentication responses
            if command == PROTOCOL_LOGIN_SUCCESS:
                self.handle_login_success(parts)
            
            elif command == PROTOCOL_WRONG_USER:
                self.handle_wrong_user(parts)
            
            elif command == PROTOCOL_DUPLICATE_LOGIN:
                self.handle_duplicate_login(parts)
            
            elif command == PROTOCOL_BANNED_USER:
                self.handle_banned_user(parts)
            
            elif command == PROTOCOL_DUPLICATE_USERNAME:
                self.handle_duplicate_username()
            
            # Chat
            elif command == PROTOCOL_CHAT_SERVER:
                self.handle_chat_server(parts)
            
            elif command == PROTOCOL_CHAT:
                self.handle_chat(parts)
            
            # Friends
            elif command == PROTOCOL_RETURN_FRIEND_LIST:
                self.handle_return_friend_list(parts)
            
            elif command == PROTOCOL_CHECK_FRIEND_RESPONSE:
                self.handle_check_friend_response(parts)
            
            elif command == PROTOCOL_MAKE_FRIEND_REQUEST:
                self.handle_make_friend_request(parts)
            
            # Rooms
            elif command == PROTOCOL_ROOM_LIST:
                self.handle_room_list(parts)
            
            elif command == PROTOCOL_YOUR_CREATED_ROOM:
                self.handle_your_created_room(parts)
            
            elif command == PROTOCOL_GO_TO_ROOM:
                self.handle_go_to_room(parts)
            
            elif command == PROTOCOL_ROOM_FULLY:
                self.handle_room_fully()
            
            elif command == PROTOCOL_ROOM_NOT_FOUND:
                self.handle_room_not_found()
            
            elif command == PROTOCOL_ROOM_WRONG_PASSWORD:
                self.handle_room_wrong_password()
            
            # Rank
            elif command == PROTOCOL_RETURN_GET_RANK_CHARTS:
                self.handle_return_get_rank_charts(parts)
            
            # Game
            elif command == PROTOCOL_CARO:
                self.handle_caro(parts)
            
            elif command == PROTOCOL_NEW_GAME:
                self.handle_new_game()
            
            # CRITICAL FIX: Add WIN/LOSE handlers
            elif command == PROTOCOL_WIN:
                self.handle_win()
            
            elif command == PROTOCOL_LOSE:
                self.handle_lose()
            
            elif command == PROTOCOL_DRAW_REQUEST:
                self.handle_draw_request()
            
            elif command == PROTOCOL_DRAW_REFUSE:
                self.handle_draw_refuse()
            
            elif command == PROTOCOL_DRAW_GAME:
                self.handle_draw_game()
            
            elif command == PROTOCOL_COMPETITOR_TIME_OUT:
                self.handle_competitor_time_out()
            
            # Duel
            elif command == PROTOCOL_DUEL_NOTICE:
                self.handle_duel_notice(parts)
            
            elif command == PROTOCOL_DISAGREE_DUEL:
                self.handle_disagree_duel()
            
            # Other
            elif command == PROTOCOL_LEFT_ROOM:
                self.handle_left_room()
            
            elif command == PROTOCOL_VOICE_MESSAGE:
                self.handle_voice_message(parts)
            
            elif command == PROTOCOL_BANNED_NOTICE:
                self.handle_banned_notice(parts)
            
            elif command == PROTOCOL_WARNING_NOTICE:
                self.handle_warning_notice(parts)
            
            elif command == PROTOCOL_ADMIN_BROADCAST:
                self.handle_admin_broadcast(parts)
        
        except Exception as e:
            log(f"Handle message error: {e}", "ERROR")
            log(f"Message: {message}", "ERROR")
    
    # Message handlers - these will call appropriate client methods
    
    def handle_login_success(self, parts):
        """Handle successful login"""
        user = self.get_user_from_string(1, parts)
        if user and hasattr(self.client, 'on_login_success'):
            self.client.on_login_success(user)
    
    def handle_wrong_user(self, parts):
        """Handle wrong credentials"""
        if hasattr(self.client, 'on_wrong_user'):
            self.client.on_wrong_user()
    
    def handle_duplicate_login(self, parts):
        """Handle duplicate login"""
        if hasattr(self.client, 'on_duplicate_login'):
            self.client.on_duplicate_login()
    
    def handle_banned_user(self, parts):
        """Handle banned user"""
        if hasattr(self.client, 'on_banned_user'):
            self.client.on_banned_user()
    
    def handle_duplicate_username(self):
        """Handle duplicate username"""
        if hasattr(self.client, 'on_duplicate_username'):
            self.client.on_duplicate_username()
    
    def handle_chat_server(self, parts):
        """Handle server chat message"""
        if len(parts) >= 2 and hasattr(self.client, 'on_chat_server'):
            self.client.on_chat_server(parts[1])
    
    def handle_chat(self, parts):
        """Handle room chat message"""
        log(f"[CHAT DEBUG] Received chat: parts={parts}", "DEBUG")
        if len(parts) >= 2 and hasattr(self.client, 'on_chat'):
            log(f"[CHAT DEBUG] Calling on_chat with message: {parts[1]}", "DEBUG")
            self.client.on_chat(parts[1])
        else:
            log(f"[CHAT DEBUG] Failed - len={len(parts)}, has on_chat={hasattr(self.client, 'on_chat')}", "ERROR")
    
    def handle_return_friend_list(self, parts):
        """Handle friend list response"""
        friends = self.get_list_user(parts)
        if hasattr(self.client, 'on_friend_list'):
            self.client.on_friend_list(friends)
    
    def handle_check_friend_response(self, parts):
        """Handle check friend response"""
        if len(parts) >= 2 and hasattr(self.client, 'on_check_friend_response'):
            is_friend = (parts[1] == "1")
            self.client.on_check_friend_response(is_friend)
    
    def handle_make_friend_request(self, parts):
        """Handle friend request"""
        if len(parts) >= 3 and hasattr(self.client, 'on_friend_request'):
            user_id = int(parts[1])
            nickname = parts[2]
            self.client.on_friend_request(user_id, nickname)
    
    def handle_room_list(self, parts):
        """Handle room list response"""
        rooms = []
        passwords = []
        i = 1
        while i < len(parts):
            if i + 1 < len(parts):
                rooms.append(f"Phòng {parts[i]}")
                passwords.append(parts[i + 1])
                i += 2
            else:
                break
        
        if hasattr(self.client, 'on_room_list'):
            self.client.on_room_list(rooms, passwords)
    
    def handle_your_created_room(self, parts):
        """Handle room created response"""
        if len(parts) >= 2 and hasattr(self.client, 'on_room_created'):
            room_id = parts[1]
            password = parts[2] if len(parts) >= 3 else None
            self.client.on_room_created(room_id, password)
    
    def handle_go_to_room(self, parts):
        """Handle go to room"""
        if len(parts) >= 13 and hasattr(self.client, 'on_go_to_room'):
            room_id = int(parts[1])
            competitor_ip = parts[2]
            is_start = int(parts[3])
            competitor = self.get_user_from_string(4, parts)
            self.client.on_go_to_room(room_id, competitor_ip, is_start, competitor)
    
    def handle_room_fully(self):
        """Handle room full"""
        if hasattr(self.client, 'on_room_fully'):
            self.client.on_room_fully()
    
    def handle_room_not_found(self):
        """Handle room not found"""
        if hasattr(self.client, 'on_room_not_found'):
            self.client.on_room_not_found()
    
    def handle_room_wrong_password(self):
        """Handle wrong room password"""
        if hasattr(self.client, 'on_room_wrong_password'):
            self.client.on_room_wrong_password()
    
    def handle_return_get_rank_charts(self, parts):
        """Handle rank list response"""
        users = self.get_list_rank(parts)
        if hasattr(self.client, 'on_rank_list'):
            self.client.on_rank_list(users)
    
    def handle_caro(self, parts):
        """Handle game move"""
        if len(parts) >= 3 and hasattr(self.client, 'on_caro_move'):
            x = parts[1]
            y = parts[2]
            self.client.on_caro_move(x, y)
    
    def handle_new_game(self):
        """Handle new game"""
        if hasattr(self.client, 'on_new_game'):
            self.client.on_new_game()
    
    def handle_draw_request(self):
        """Handle draw request"""
        if hasattr(self.client, 'on_draw_request'):
            self.client.on_draw_request()
    
    def handle_draw_refuse(self):
        """Handle draw refused"""
        if hasattr(self.client, 'on_draw_refuse'):
            self.client.on_draw_refuse()
    
    def handle_draw_game(self):
        """Handle draw game"""
        if hasattr(self.client, 'on_draw_game'):
            self.client.on_draw_game()
    
    def handle_win(self):
        """Handle win from server - CRITICAL FIX"""
        if hasattr(self.client, 'on_win'):
            self.client.on_win()
    
    def handle_lose(self):
        """Handle lose from server - CRITICAL FIX"""
        if hasattr(self.client, 'on_lose'):
            self.client.on_lose()
    
    def handle_competitor_time_out(self):
        """Handle competitor timeout"""
        if hasattr(self.client, 'on_competitor_time_out'):
            self.client.on_competitor_time_out()
    
    def handle_duel_notice(self, parts):
        """Handle duel request"""
        if len(parts) >= 3 and hasattr(self.client, 'on_duel_notice'):
            user_id = int(parts[1])
            nickname = parts[2]
            self.client.on_duel_notice(user_id, nickname)
    
    def handle_disagree_duel(self):
        """Handle duel disagreed"""
        if hasattr(self.client, 'on_disagree_duel'):
            self.client.on_disagree_duel()
    
    def handle_left_room(self):
        """Handle competitor left room"""
        if hasattr(self.client, 'on_left_room'):
            self.client.on_left_room()
    
    def handle_voice_message(self, parts):
        """Handle voice message"""
        if len(parts) >= 2 and hasattr(self.client, 'on_voice_message'):
            self.client.on_voice_message(parts[1])
    
    def handle_banned_notice(self, parts):
        """Handle ban notice"""
        if len(parts) >= 2 and hasattr(self.client, 'on_banned_notice'):
            self.client.on_banned_notice(parts[1])
    
    def handle_warning_notice(self, parts):
        """Handle warning notice"""
        if len(parts) >= 2 and hasattr(self.client, 'on_warning_notice'):
            self.client.on_warning_notice(parts[1])
    
    def handle_admin_broadcast(self, parts):
        """Handle admin broadcast message"""
        if len(parts) >= 2 and hasattr(self.client, 'on_admin_broadcast'):
            message = parts[1]
            self.client.on_admin_broadcast(message)

