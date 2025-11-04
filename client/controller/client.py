"""
Main client controller
"""

from shared.user import User
from shared.config import Config

class Client:
    """Main client controller - manages all views and state"""
    
    # Class variables for views
    user = None
    socket_handle = None
    root = None  # Main Tkinter root window
    
    # GUI Forms
    login_frm = None
    register_frm = None
    homepage_frm = None
    room_list_frm = None
    friend_list_frm = None
    find_room_frm = None
    waiting_room_frm = None
    game_client_frm = None
    create_room_frm = None
    create_room_password_frm = None
    join_room_password_frm = None
    competitor_info_frm = None
    rank_frm = None
    game_notice_frm = None
    friend_request_frm = None
    game_ai_frm = None
    room_name_frm = None
    
    @classmethod
    def open_login(cls):
        """Open login form"""
        from client.view.login_frm import LoginFrm
        cls.login_frm = LoginFrm()
        cls.login_frm.show()
    
    @classmethod
    def open_register(cls):
        """Open register form"""
        from client.view.register_frm import RegisterFrm
        cls.register_frm = RegisterFrm()
        cls.register_frm.show()
    
    @classmethod
    def open_homepage(cls):
        """Open homepage"""
        from client.view.homepage_frm import HomePageFrm
        cls.homepage_frm = HomePageFrm()
        cls.homepage_frm.show()
    
    @classmethod
    def open_room_list(cls):
        """Open room list"""
        from client.view.room_list_frm import RoomListFrm
        cls.room_list_frm = RoomListFrm()
        cls.room_list_frm.show()
    
    @classmethod
    def open_friend_list(cls):
        """Open friend list"""
        from client.view.friend_list_frm import FriendListFrm
        cls.friend_list_frm = FriendListFrm()
        cls.friend_list_frm.show()
    
    @classmethod
    def open_waiting_room(cls, room_id="0", password=""):
        """Open waiting room"""
        from client.view.waiting_room_frm import WaitingRoomFrm
        cls.waiting_room_frm = WaitingRoomFrm(room_id, password)
        cls.waiting_room_frm.show()
    
    @classmethod
    def open_game_client(cls, competitor, room_id, is_start, competitor_ip):
        """Open game client"""
        from client.view.game_client_frm import GameClientFrm
        cls.game_client_frm = GameClientFrm(competitor, room_id, is_start, competitor_ip)
        cls.game_client_frm.show()
    
    @classmethod
    def open_ai_game(cls):
        """Open AI game"""
        from client.view.ai_game_frm import AIGameFrm
        cls.ai_game_frm = AIGameFrm()
    
    @classmethod
    def open_create_room(cls):
        """Open create room form"""
        from client.view.create_room_frm import CreateRoomFrm
        cls.create_room_frm = CreateRoomFrm()
        cls.create_room_frm.show()
    
    @classmethod
    def open_rank(cls):
        """Open rank board"""
        from client.view.rank_frm import RankFrm
        cls.rank_frm = RankFrm()
        cls.rank_frm.show()
    
    @classmethod
    def close_all_views(cls):
        """Close all open views"""
        views = [
            cls.login_frm, cls.register_frm, cls.homepage_frm,
            cls.room_list_frm, cls.friend_list_frm, cls.find_room_frm,
            cls.waiting_room_frm, cls.game_client_frm,
            cls.create_room_password_frm, cls.join_room_password_frm,
            cls.competitor_info_frm, cls.rank_frm, cls.game_notice_frm,
            cls.friend_request_frm, cls.game_ai_frm, cls.room_name_frm,
            cls.create_room_frm
        ]
        
        for view in views:
            if view is not None:
                try:
                    view.close()
                except:
                    pass
    
    @classmethod
    def close_view(cls, view_name):
        """Close specific view by name"""
        view_map = {
            'login': cls.login_frm,
            'register': cls.register_frm,
            'homepage': cls.homepage_frm,
            'room_list': cls.room_list_frm,
            'friend_list': cls.friend_list_frm,
            'find_room': cls.find_room_frm,
            'waiting_room': cls.waiting_room_frm,
            'game_client': cls.game_client_frm,
            'create_room_password': cls.create_room_password_frm,
            'join_room_password': cls.join_room_password_frm,
            'competitor_info': cls.competitor_info_frm,
            'rank': cls.rank_frm,
            'game_notice': cls.game_notice_frm,
            'friend_request': cls.friend_request_frm,
            'game_ai': cls.game_ai_frm,
            'room_name': cls.room_name_frm
        }
        
        view = view_map.get(view_name)
        if view is not None:
            try:
                view.close()
            except:
                pass
    
    @classmethod
    def init_connection(cls):
        """Initialize connection to server"""
        from client.controller.socket_handle import SocketHandle
        
        cls.socket_handle = SocketHandle(cls)
        if cls.socket_handle.connect(Config.SERVER_HOST, Config.SERVER_PORT):
            cls.socket_handle.start()
            return True
        return False
    
    # Callback methods for socket handle
    
    @classmethod
    def on_login_success(cls, user):
        """Handle successful login"""
        cls.user = user
        cls.close_all_views()
        cls.open_homepage()
    
    @classmethod
    def on_wrong_user(cls):
        """Handle wrong credentials"""
        if cls.login_frm:
            cls.login_frm.show_error("Tài khoản hoặc mật khẩu không chính xác!")
    
    @classmethod
    def on_duplicate_login(cls):
        """Handle duplicate login"""
        if cls.login_frm:
            cls.login_frm.show_error("Tài khoản đã đăng nhập ở nơi khác!")
    
    @classmethod
    def on_banned_user(cls):
        """Handle banned user"""
        if cls.login_frm:
            cls.login_frm.show_error("Tài khoản đã bị cấm!")
    
    @classmethod
    def on_duplicate_username(cls):
        """Handle duplicate username during registration"""
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Tên tài khoản đã tồn tại!")
    
    @classmethod
    def on_chat_server(cls, message):
        """Handle server chat message"""
        if cls.homepage_frm:
            cls.homepage_frm.add_message(message)
    
    @classmethod
    def on_chat(cls, message):
        """Handle room chat message"""
        if cls.game_client_frm:
            cls.game_client_frm.receive_chat(message)
    
    @classmethod
    def on_friend_list(cls, friends):
        """Handle friend list response"""
        if cls.friend_list_frm:
            cls.friend_list_frm.update_friend_list(friends)
    
    @classmethod
    def on_room_list(cls, rooms, passwords):
        """Handle room list response"""
        if cls.room_list_frm:
            cls.room_list_frm.update_room_list(rooms, passwords)
    
    @classmethod
    def on_room_created(cls, room_id, password):
        """Handle room created"""
        # Close homepage and open waiting room with room_id
        if cls.homepage_frm:
            cls.homepage_frm.close()
        cls.open_waiting_room(room_id, password)
    
    @classmethod
    def on_go_to_room(cls, room_id, competitor_ip, is_start, competitor):
        """Handle entering game room"""
        import time
        if cls.find_room_frm or cls.waiting_room_frm:
            time.sleep(1)  # Brief pause
        cls.close_all_views()
        cls.open_game_client(competitor, room_id, is_start, competitor_ip)
    
    @classmethod
    def on_room_fully(cls):
        """Handle room full error"""
        from tkinter import messagebox
        cls.close_all_views()
        cls.open_homepage()
        messagebox.showwarning("Thông báo", "Phòng chơi đã đủ 2 người!")
    
    @classmethod
    def on_room_not_found(cls):
        """Handle room not found"""
        from tkinter import messagebox
        cls.close_all_views()
        cls.open_homepage()
        messagebox.showwarning("Thông báo", "Không tìm thấy phòng!")
    
    @classmethod
    def on_room_wrong_password(cls):
        """Handle wrong room password"""
        from tkinter import messagebox
        cls.close_all_views()
        cls.open_homepage()
        messagebox.showwarning("Thông báo", "Mật khẩu phòng không đúng!")
    
    @classmethod
    def on_rank_list(cls, users):
        """Handle rank list response"""
        if cls.rank_frm:
            cls.rank_frm.update_rank_list(users)
    
    @classmethod
    def on_caro_move(cls, x, y):
        """Handle opponent's move"""
        if cls.game_client_frm:
            # Convert string to int (Java sends as string)
            row = int(x)
            col = int(y)
            cls.game_client_frm.add_competitor_move(row, col)
    
    @classmethod
    def on_new_game(cls):
        """Handle new game"""
        if cls.game_client_frm:
            cls.game_client_frm.new_game()
    
    @classmethod
    def on_draw_request(cls):
        """Handle draw request"""
        if cls.game_client_frm:
            cls.game_client_frm.show_draw_request()
    
    @classmethod
    def on_draw_refuse(cls):
        """Handle draw refused"""
        if cls.game_client_frm:
            cls.game_client_frm.show_draw_refuse()
    
    @classmethod
    def on_draw_game(cls):
        """Handle draw game"""
        if cls.game_client_frm:
            cls.game_client_frm.handle_draw_game()
    
    @classmethod
    def on_competitor_time_out(cls):
        """Handle competitor timeout"""
        if cls.game_client_frm:
            cls.game_client_frm.handle_competitor_timeout()
    
    @classmethod
    def on_friend_request(cls, user_id, nickname):
        """Handle friend request"""
        from tkinter import messagebox
        result = messagebox.askyesno("Yêu cầu kết bạn", 
                                    f"{nickname} (ID: {user_id}) muốn kết bạn với bạn. Đồng ý?")
        if result and cls.socket_handle:
            from shared.utils import create_message
            from shared.constants import PROTOCOL_MAKE_FRIEND_CONFIRM
            cls.socket_handle.write(create_message(PROTOCOL_MAKE_FRIEND_CONFIRM, user_id))
    
    @classmethod
    def on_duel_notice(cls, user_id, nickname):
        """Handle duel request"""
        from tkinter import messagebox
        from shared.utils import create_message
        from shared.constants import PROTOCOL_AGREE_DUEL, PROTOCOL_DISAGREE_DUEL
        
        result = messagebox.askyesno("Thách đấu", 
                                    f"{nickname} (ID: {user_id}) thách đấu bạn. Đồng ý?")
        if result and cls.socket_handle:
            cls.socket_handle.write(create_message(PROTOCOL_AGREE_DUEL, user_id))
        elif cls.socket_handle:
            cls.socket_handle.write(create_message(PROTOCOL_DISAGREE_DUEL, user_id))
    
    @classmethod
    def on_disagree_duel(cls):
        """Handle duel disagreed"""
        from tkinter import messagebox
        cls.close_all_views()
        cls.open_homepage()
        messagebox.showinfo("Thông báo", "Đối thủ từ chối thách đấu!")
    
    @classmethod
    def on_left_room(cls):
        """Handle opponent left room"""
        from tkinter import messagebox
        if cls.game_client_frm:
            cls.game_client_frm.close()
        messagebox.showinfo("Thông báo", "Đối thủ đã rời khỏi phòng!")
        cls.open_homepage()
    
    @classmethod
    def on_admin_broadcast(cls, message):
        """Handle admin broadcast message"""
        # Add to homepage chat if it exists
        if cls.homepage_frm:
            cls.homepage_frm.add_message(f"📢 [ADMIN]: {message}")

        cls.close_all_views()
        cls.open_homepage()
