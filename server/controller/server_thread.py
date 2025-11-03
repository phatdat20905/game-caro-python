"""
Server thread - handles individual client connection
"""

import socket
import threading
from server.dao.user_dao import UserDAO
from server.controller.room import Room
from shared.user import User
from shared.utils import log, create_message
from shared.constants import *

class ServerThread(threading.Thread):
    """Thread handling one client connection"""
    
    def __init__(self, client_socket, client_number, server_thread_bus, admin=None):
        """
        Initialize server thread
        
        Args:
            client_socket: Client socket connection
            client_number: Unique client identifier
            server_thread_bus: Reference to ServerThreadBus
            admin: Reference to admin panel
        """
        super().__init__()
        self.client_socket = client_socket
        self.client_number = client_number
        self.server_thread_bus = server_thread_bus
        self.admin = admin
        
        self.user = None
        self.room = None
        self.is_closed = False
        self.user_dao = UserDAO()
        
        # Get client IP
        try:
            client_ip = client_socket.getpeername()[0]
            self.client_ip = "127.0.0.1" if client_ip == "127.0.0.1" else client_ip
        except:
            self.client_ip = "unknown"
        
        log(f"ServerThread {client_number} initialized for {self.client_ip}")
    
    def get_client_number(self):
        return self.client_number
    
    def get_user(self):
        return self.user
    
    def set_user(self, user):
        self.user = user
    
    def get_room(self):
        return self.room
    
    def set_room(self, room):
        self.room = room
    
    def get_client_ip(self):
        return self.client_ip
    
    def get_string_from_user(self, user):
        """Convert user to string for transmission"""
        if user:
            return user.to_string()
        return ""
    
    def go_to_own_room(self):
        """Player 1 enters room (starts game)"""
        try:
            competitor = self.room.get_competitor(self.client_number)
            if competitor:
                # Send to self
                msg = create_message(
                    PROTOCOL_GO_TO_ROOM,
                    self.room.get_id(),
                    competitor.get_client_ip(),
                    1,  # is_start = 1
                    self.get_string_from_user(competitor.get_user())
                )
                self.write(msg)
                
                # Send to competitor
                msg = create_message(
                    PROTOCOL_GO_TO_ROOM,
                    self.room.get_id(),
                    self.client_ip,
                    0,  # is_start = 0
                    self.get_string_from_user(self.user)
                )
                competitor.write(msg)
        except Exception as e:
            log(f"go_to_own_room error: {e}", "ERROR")
    
    def go_to_partner_room(self):
        """Player 2 enters room (joins game)"""
        try:
            competitor = self.room.get_competitor(self.client_number)
            if competitor:
                # Send to self
                msg = create_message(
                    PROTOCOL_GO_TO_ROOM,
                    self.room.get_id(),
                    competitor.get_client_ip(),
                    0,  # is_start = 0
                    self.get_string_from_user(competitor.get_user())
                )
                self.write(msg)
                
                # Send to competitor
                msg = create_message(
                    PROTOCOL_GO_TO_ROOM,
                    self.room.get_id(),
                    self.client_ip,
                    1,  # is_start = 1
                    self.get_string_from_user(self.user)
                )
                competitor.write(msg)
        except Exception as e:
            log(f"go_to_partner_room error: {e}", "ERROR")
    
    def run(self):
        """Main thread execution"""
        try:
            log(f"Client {self.client_number} thread started")
            
            # Send client ID
            self.write(create_message(PROTOCOL_SERVER_SEND_ID, self.client_number))
            
            # Main message loop
            while not self.is_closed:
                try:
                    message = self.client_socket.recv(BUFFER_SIZE).decode(ENCODING).strip()
                    if not message:
                        break
                    
                    # Handle message
                    self.handle_message(message)
                
                except socket.timeout:
                    continue
                except Exception as e:
                    log(f"Client {self.client_number} receive error: {e}", "ERROR")
                    break
        
        except Exception as e:
            log(f"Client {self.client_number} thread error: {e}", "ERROR")
        
        finally:
            self.cleanup()
    
    def handle_message(self, message):
        """
        Handle incoming message
        
        Args:
            message: Message string from client
        """
        try:
            parts = message.split(',')
            if not parts:
                return
            
            command = parts[0]
            
            # Login/Register
            if command == PROTOCOL_CLIENT_VERIFY:
                self.handle_login(parts)
            
            elif command == PROTOCOL_REGISTER:
                self.handle_register(parts)
            
            elif command == PROTOCOL_OFFLINE:
                self.handle_offline(parts)
            
            # Friends
            elif command == PROTOCOL_VIEW_FRIEND_LIST:
                self.handle_view_friend_list()
            
            elif command == PROTOCOL_CHECK_FRIEND:
                self.handle_check_friend(parts)
            
            elif command == PROTOCOL_MAKE_FRIEND:
                self.handle_make_friend(parts)
            
            elif command == PROTOCOL_MAKE_FRIEND_CONFIRM:
                self.handle_make_friend_confirm(parts)
            
            # Rooms
            elif command == PROTOCOL_CREATE_ROOM:
                self.handle_create_room(parts)
            
            elif command == PROTOCOL_VIEW_ROOM_LIST:
                self.handle_view_room_list()
            
            elif command == PROTOCOL_QUICK_ROOM:
                self.handle_quick_room()
            
            elif command == PROTOCOL_GO_TO_ROOM:
                self.handle_go_to_room(parts)
            
            elif command == PROTOCOL_JOIN_ROOM:
                self.handle_join_room(parts)
            
            elif command == PROTOCOL_CANCEL_ROOM:
                self.handle_cancel_room()
            
            # Game
            elif command == PROTOCOL_CARO:
                self.handle_caro(message)
            
            elif command == PROTOCOL_WIN:
                self.handle_win(parts)
            
            elif command == PROTOCOL_LOSE:
                self.handle_lose()
            
            elif command == PROTOCOL_DRAW_REQUEST:
                self.handle_draw_request(message)
            
            elif command == PROTOCOL_DRAW_CONFIRM:
                self.handle_draw_confirm()
            
            elif command == PROTOCOL_DRAW_REFUSE:
                self.handle_draw_refuse()
            
            # Chat
            elif command == PROTOCOL_CHAT_SERVER:
                self.handle_chat_server(parts)
            
            elif command == PROTOCOL_CHAT:
                self.handle_chat(message)
            
            # Rank
            elif command == PROTOCOL_GET_RANK_CHARTS:
                self.handle_get_rank_charts()
            
            # Duel
            elif command == PROTOCOL_DUEL_REQUEST:
                self.handle_duel_request(parts)
            
            elif command == PROTOCOL_AGREE_DUEL:
                self.handle_agree_duel(parts)
            
            elif command == PROTOCOL_DISAGREE_DUEL:
                self.handle_disagree_duel(parts)
            
            # Voice
            elif command == PROTOCOL_VOICE_MESSAGE:
                self.handle_voice_message(message)
            
            # Leave room
            elif command == PROTOCOL_LEFT_ROOM:
                self.handle_left_room()
        
        except Exception as e:
            log(f"Handle message error: {e}", "ERROR")
            log(f"Message: {message}", "ERROR")
    
    def handle_login(self, parts):
        """Handle login verification"""
        if len(parts) < 3:
            return
        
        username = parts[1]
        password = parts[2]
        
        user = self.user_dao.verify_user(username, password)
        
        if user is None:
            self.write(create_message(PROTOCOL_WRONG_USER, username, password))
        
        elif self.user_dao.check_is_banned(user.get_id()):
            self.write(create_message(PROTOCOL_BANNED_USER, username, password))
        
        elif user.get_is_online():
            # User already online - try to cleanup old connection
            log(f"User {username} already online - attempting cleanup", "WARNING")
            
            # Find and close old connection
            old_thread = None
            for thread in self.server_thread_bus.get_list_server_threads():
                if thread.user and thread.user.get_id() == user.get_id():
                    old_thread = thread
                    break
            
            if old_thread:
                log(f"Forcing disconnect of old connection for {username}")
                try:
                    old_thread.cleanup()
                except:
                    pass
                # Force database update
                self.user_dao.update_to_offline(user.get_id())
                self.user_dao.update_to_not_playing(user.get_id())
            
            # Allow new login
            self.write(create_message(PROTOCOL_LOGIN_SUCCESS, self.get_string_from_user(user)))
            self.user = user
            self.user_dao.update_to_online(self.user.get_id())
            self.server_thread_bus.broadcast(
                self.client_number,
                create_message(PROTOCOL_CHAT_SERVER, f"{user.get_nickname()} đang online")
            )
            if self.admin:
                self.admin.add_message(f"[{user.get_id()}] {user.get_nickname()} đang online")
        
        else:
            # Normal login
            self.write(create_message(PROTOCOL_LOGIN_SUCCESS, self.get_string_from_user(user)))
            self.user = user
            self.user_dao.update_to_online(self.user.get_id())
            self.server_thread_bus.broadcast(
                self.client_number,
                create_message(PROTOCOL_CHAT_SERVER, f"{user.get_nickname()} đang online")
            )
            if self.admin:
                self.admin.add_message(f"[{user.get_id()}] {user.get_nickname()} đang online")
    
    def handle_register(self, parts):
        """Handle user registration"""
        if len(parts) < 5:
            return
        
        username = parts[1]
        password = parts[2]
        nickname = parts[3]
        avatar = parts[4]
        
        if self.user_dao.check_duplicated(username):
            self.write(create_message(PROTOCOL_DUPLICATE_USERNAME))
        else:
            self.user_dao.add_user(username, password, nickname, avatar)
            user = self.user_dao.verify_user(username, password)
            if user:
                self.user = user
                self.user_dao.update_to_online(self.user.get_id())
                self.server_thread_bus.broadcast(
                    self.client_number,
                    create_message(PROTOCOL_CHAT_SERVER, f"{self.user.get_nickname()} đang online")
                )
                self.write(create_message(PROTOCOL_LOGIN_SUCCESS, self.get_string_from_user(self.user)))
    
    def handle_offline(self, parts):
        """Handle user offline"""
        if self.user:
            self.user_dao.update_to_offline(self.user.get_id())
            if self.admin:
                self.admin.add_message(f"[{self.user.get_id()}] {self.user.get_nickname()} đã offline")
            self.server_thread_bus.broadcast(
                self.client_number,
                create_message(PROTOCOL_CHAT_SERVER, f"{self.user.get_nickname()} đã offline")
            )
            self.user = None
    
    def handle_view_friend_list(self):
        """Send friend list to client"""
        if not self.user:
            return
        
        friends = self.user_dao.get_list_friend(self.user.get_id())
        result = [PROTOCOL_RETURN_FRIEND_LIST]
        
        for friend in friends:
            result.extend([
                str(friend.get_id()),
                friend.get_nickname(),
                "1" if friend.get_is_online() else "0",
                "1" if friend.get_is_playing() else "0"
            ])
        
        self.write(create_message(*result))
    
    def handle_check_friend(self, parts):
        """Check if two users are friends"""
        if len(parts) < 2 or not self.user:
            return
        
        friend_id = int(parts[1])
        is_friend = self.user_dao.check_is_friend(self.user.get_id(), friend_id)
        self.write(create_message(PROTOCOL_CHECK_FRIEND_RESPONSE, "1" if is_friend else "0"))
    
    def handle_make_friend(self, parts):
        """Send friend request"""
        if len(parts) < 2 or not self.user:
            return
        
        friend_id = int(parts[1])
        nickname = self.user_dao.get_nickname_by_id(self.user.get_id())
        
        self.server_thread_bus.send_message_to_user_id(
            friend_id,
            create_message(PROTOCOL_MAKE_FRIEND_REQUEST, self.user.get_id(), nickname)
        )
    
    def handle_make_friend_confirm(self, parts):
        """Confirm friend request"""
        if len(parts) < 2 or not self.user:
            return
        
        friend_id = int(parts[1])
        self.user_dao.make_friend(self.user.get_id(), friend_id)
        log(f"Friend added: {self.user.get_id()} <-> {friend_id}")
    
    def handle_create_room(self, parts):
        """Create new room"""
        if not self.user:
            return
        
        self.room = Room(self)
        
        if len(parts) >= 2:
            password = parts[1]
            self.room.set_password(password)
            self.write(create_message(PROTOCOL_YOUR_CREATED_ROOM, self.room.get_id(), password))
            log(f"Room {self.room.get_id()} created with password")
        else:
            self.write(create_message(PROTOCOL_YOUR_CREATED_ROOM, self.room.get_id()))
            log(f"Room {self.room.get_id()} created without password")
        
        self.user_dao.update_to_playing(self.user.get_id())
    
    def handle_view_room_list(self):
        """Send list of available rooms"""
        result = [PROTOCOL_ROOM_LIST]
        count = 0
        
        for thread in self.server_thread_bus.get_list_server_threads():
            if count >= 8:
                break
            
            if thread.get_room() and thread.get_room().get_number_of_user() == 1:
                result.extend([
                    str(thread.get_room().get_id()),
                    thread.get_room().get_password()
                ])
                count += 1
        
        self.write(create_message(*result))
    
    def handle_quick_room(self):
        """Quick match - find or create room"""
        if not self.user:
            return
        
        found = False
        
        # Try to find existing room
        for thread in self.server_thread_bus.get_list_server_threads():
            room = thread.get_room()
            if room and room.get_number_of_user() == 1 and room.get_password() == " ":
                thread.get_room().set_user2(self)
                self.room = thread.get_room()
                self.room.increase_number_of_game()
                log(f"Quick joined room {self.room.get_id()}")
                self.go_to_partner_room()
                self.user_dao.update_to_playing(self.user.get_id())
                found = True
                break
        
        # Create new room if not found
        if not found:
            self.room = Room(self)
            self.user_dao.update_to_playing(self.user.get_id())
            log(f"Quick created room {self.room.get_id()} - waiting for opponent...")
            # Send created room notification
            self.write(create_message(PROTOCOL_YOUR_CREATED_ROOM, self.room.get_id()))
    
    def handle_go_to_room(self, parts):
        """Go to specific room by ID"""
        if len(parts) < 2 or not self.user:
            return
        
        room_id = int(parts[1])
        password = parts[2] if len(parts) >= 3 else ""
        found = False
        
        for thread in self.server_thread_bus.get_list_server_threads():
            room = thread.get_room()
            if room and room.get_id() == room_id:
                found = True
                
                if room.get_number_of_user() == 2:
                    self.write(create_message(PROTOCOL_ROOM_FULLY))
                
                elif room.get_password() == " " or room.get_password() == password:
                    self.room = room
                    room.set_user2(self)
                    room.increase_number_of_game()
                    self.user_dao.update_to_playing(self.user.get_id())
                    self.go_to_partner_room()
                
                else:
                    self.write(create_message(PROTOCOL_ROOM_WRONG_PASSWORD))
                
                break
        
        if not found:
            self.write(create_message(PROTOCOL_ROOM_NOT_FOUND))
    
    def handle_join_room(self, parts):
        """Join room by ID"""
        if len(parts) < 2 or not self.user:
            return
        
        room_id = int(parts[1])
        
        for thread in self.server_thread_bus.get_list_server_threads():
            room = thread.get_room()
            if room and room.get_id() == room_id:
                thread.get_room().set_user2(self)
                self.room = thread.get_room()
                log(f"Joined room {self.room.get_id()}")
                self.room.increase_number_of_game()
                self.go_to_partner_room()
                self.user_dao.update_to_playing(self.user.get_id())
                break
    
    def handle_cancel_room(self):
        """Cancel waiting room"""
        if self.user:
            self.user_dao.update_to_not_playing(self.user.get_id())
            log("Room cancelled")
            self.room = None
    
    def handle_caro(self, message):
        """Handle game move"""
        if self.room:
            competitor = self.room.get_competitor(self.client_number)
            if competitor:
                competitor.write(message)
    
    def handle_win(self, parts):
        """Handle win condition"""
        if not self.room:
            return
        
        self.user_dao.add_win_game(self.user.get_id())
        self.room.increase_number_of_game()
        
        competitor = self.room.get_competitor(self.client_number)
        if competitor and len(parts) >= 3:
            competitor.write(create_message(PROTOCOL_CARO, parts[1], parts[2]))
        
        self.room.broadcast(create_message(PROTOCOL_NEW_GAME))
    
    def handle_lose(self):
        """Handle lose/timeout"""
        if not self.room:
            return
        
        competitor = self.room.get_competitor(self.client_number)
        if competitor:
            self.user_dao.add_win_game(competitor.get_user().get_id())
            self.room.increase_number_of_game()
            competitor.write(create_message(PROTOCOL_COMPETITOR_TIME_OUT))
        
        self.write(create_message(PROTOCOL_NEW_GAME))
    
    def handle_draw_request(self, message):
        """Forward draw request to competitor"""
        if self.room:
            competitor = self.room.get_competitor(self.client_number)
            if competitor:
                competitor.write(message)
    
    def handle_draw_confirm(self):
        """Confirm draw game"""
        if self.room:
            self.room.increase_number_of_draw()
            self.room.increase_number_of_game()
            self.room.broadcast(create_message(PROTOCOL_DRAW_GAME))
    
    def handle_draw_refuse(self):
        """Refuse draw request"""
        if self.room:
            competitor = self.room.get_competitor(self.client_number)
            if competitor:
                competitor.write(create_message(PROTOCOL_DRAW_REFUSE))
    
    def handle_chat_server(self, parts):
        """Broadcast chat to server"""
        if not self.user or len(parts) < 2:
            return
        
        msg = create_message(PROTOCOL_CHAT_SERVER, f"{self.user.get_nickname()} : {parts[1]}")
        self.server_thread_bus.broadcast(self.client_number, msg)
        
        if self.admin:
            self.admin.add_message(f"[{self.user.get_id()}] {self.user.get_nickname()} : {parts[1]}")
    
    def handle_chat(self, message):
        """Forward chat to competitor"""
        if self.room:
            competitor = self.room.get_competitor(self.client_number)
            if competitor:
                competitor.write(message)
    
    def handle_get_rank_charts(self):
        """Send ranking list"""
        users = self.user_dao.get_user_static_rank()
        result = [PROTOCOL_RETURN_GET_RANK_CHARTS]
        
        for user in users:
            result.append(self.get_string_from_user(user))
        
        self.write(','.join(result))
    
    def handle_duel_request(self, parts):
        """Send duel request to friend"""
        if len(parts) < 2 or not self.user:
            return
        
        friend_id = int(parts[1])
        self.server_thread_bus.send_message_to_user_id(
            friend_id,
            create_message(PROTOCOL_DUEL_NOTICE, self.user.get_id(), self.user.get_nickname())
        )
    
    def handle_agree_duel(self, parts):
        """Accept duel request"""
        if len(parts) < 2 or not self.user:
            return
        
        self.room = Room(self)
        user2_id = int(parts[1])
        user2_thread = self.server_thread_bus.get_server_thread_by_user_id(user2_id)
        
        if user2_thread:
            self.room.set_user2(user2_thread)
            user2_thread.set_room(self.room)
            self.room.increase_number_of_game()
            self.go_to_own_room()
            self.user_dao.update_to_playing(self.user.get_id())
    
    def handle_disagree_duel(self, parts):
        """Refuse duel request"""
        if len(parts) < 2:
            return
        
        user_id = int(parts[1])
        self.server_thread_bus.send_message_to_user_id(user_id, create_message(PROTOCOL_DISAGREE_DUEL))
    
    def handle_voice_message(self, message):
        """Forward voice message"""
        if self.room:
            competitor = self.room.get_competitor(self.client_number)
            if competitor:
                competitor.write(message)
    
    def handle_left_room(self):
        """Handle leaving room"""
        if self.room:
            self.room.set_users_to_not_playing()
            self.room.decrease_number_of_game()
            
            competitor = self.room.get_competitor(self.client_number)
            if competitor:
                competitor.write(create_message(PROTOCOL_LEFT_ROOM))
                competitor.set_room(None)
            
            self.room = None
    
    def write(self, message):
        """
        Send message to client
        
        Args:
            message: Message string
        """
        try:
            self.client_socket.send((message + '\n').encode(ENCODING))
        except Exception as e:
            log(f"Write error to client {self.client_number}: {e}", "ERROR")
    
    def cleanup(self):
        """Cleanup on disconnect"""
        self.is_closed = True
        
        # Update user status in database
        if self.user:
            try:
                # Force update to offline and not playing
                self.user_dao.update_to_offline(self.user.get_id())
                self.user_dao.update_to_not_playing(self.user.get_id())
                log(f"User {self.user.get_nickname()} ({self.user.get_id()}) set to offline")
                
                # Broadcast offline status
                self.server_thread_bus.broadcast(
                    self.client_number,
                    create_message(PROTOCOL_CHAT_SERVER, f"{self.user.get_nickname()} đã offline")
                )
                
                if self.admin:
                    self.admin.add_message(f"[{self.user.get_id()}] {self.user.get_nickname()} đã offline")
            except Exception as e:
                log(f"User cleanup error: {e}", "ERROR")
        
        # Clean up room
        if self.room:
            try:
                competitor = self.room.get_competitor(self.client_number)
                if competitor:
                    self.room.decrease_number_of_game()
                    competitor.write(create_message(PROTOCOL_LEFT_ROOM))
                    competitor.set_room(None)
            except Exception as e:
                log(f"Room cleanup error: {e}", "ERROR")
        
        # Remove from bus
        try:
            self.server_thread_bus.remove(self.client_number)
        except Exception as e:
            log(f"Bus removal error: {e}", "ERROR")
        
        # Close socket
        try:
            self.client_socket.close()
        except:
            pass
        
        log(f"Client {self.client_number} disconnected and cleaned up")
