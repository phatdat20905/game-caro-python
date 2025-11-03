"""
Constants used across the application
"""

# Network
DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 7777
BUFFER_SIZE = 4096
ENCODING = "utf-8"

# Game Settings
BOARD_SIZE = 15
WIN_CONDITION = 5
TURN_TIME_LIMIT = 30  # seconds
CELL_SIZE = 40  # pixels

# Room Settings
MIN_ROOM_ID = 100
MAX_ROOMS = 100
ROOM_PASSWORD_PLACEHOLDER = " "

# Thread Pool
MIN_THREADS = 10
MAX_THREADS = 100
THREAD_TIMEOUT = 10  # seconds

# Database
DATABASE_PATH = "database/caro_game.db"

# Avatar
AVATAR_COUNT = 6  # 0.jpg to 5.jpg
DEFAULT_AVATAR = "0"

# Rank Thresholds
RANK_BRONZE = 0
RANK_SILVER = 50
RANK_GOLD = 100

# Colors (Tkinter)
COLOR_PRIMARY = "#2196F3"
COLOR_SUCCESS = "#4CAF50"
COLOR_DANGER = "#F44336"
COLOR_WARNING = "#FF9800"
COLOR_INFO = "#00BCD4"
COLOR_DARK = "#212121"
COLOR_LIGHT = "#FAFAFA"
COLOR_BACKGROUND = "#ECEFF1"

# Fonts
FONT_TITLE = ("Arial", 16, "bold")
FONT_NORMAL = ("Arial", 10)
FONT_BUTTON = ("Arial", 11, "bold")
FONT_SMALL = ("Arial", 9)

# Messages
MSG_LOGIN_SUCCESS = "Đăng nhập thành công"
MSG_WRONG_USER = "Tài khoản hoặc mật khẩu không chính xác"
MSG_DUPLICATE_LOGIN = "Tài khoản đã đăng nhập ở nơi khác"
MSG_BANNED_USER = "Tài khoản đã bị cấm"
MSG_DUPLICATE_USERNAME = "Tên tài khoản đã tồn tại"
MSG_ROOM_FULLY = "Phòng chơi đã đủ 2 người"
MSG_ROOM_NOT_FOUND = "Không tìm thấy phòng"
MSG_ROOM_WRONG_PASSWORD = "Mật khẩu phòng sai"
MSG_CONNECTION_ERROR = "Lỗi kết nối đến server"
MSG_LEFT_ROOM = "Đối thủ đã rời khỏi phòng"

# Protocol Messages
PROTOCOL_LOGIN = "login"
PROTOCOL_SERVER_SEND_ID = "server-send-id"
PROTOCOL_LOGIN_SUCCESS = "login-success"
PROTOCOL_WRONG_USER = "wrong-user"
PROTOCOL_DUPLICATE_LOGIN = "dupplicate-login"
PROTOCOL_BANNED_USER = "banned-user"
PROTOCOL_REGISTER = "register"
PROTOCOL_DUPLICATE_USERNAME = "duplicate-username"
PROTOCOL_CLIENT_VERIFY = "client-verify"
PROTOCOL_OFFLINE = "offline"
PROTOCOL_CHAT_SERVER = "chat-server"
PROTOCOL_CHAT = "chat"
PROTOCOL_VIEW_FRIEND_LIST = "view-friend-list"
PROTOCOL_RETURN_FRIEND_LIST = "return-friend-list"
PROTOCOL_VIEW_ROOM_LIST = "view-room-list"
PROTOCOL_ROOM_LIST = "room-list"
PROTOCOL_CREATE_ROOM = "create-room"
PROTOCOL_CREATE_ROOM_PASSWORD = "create-room-password"
PROTOCOL_YOUR_CREATED_ROOM = "your-created-room"
PROTOCOL_QUICK_ROOM = "quick-room"
PROTOCOL_GO_TO_ROOM = "go-to-room"
PROTOCOL_JOIN_ROOM = "join-room"
PROTOCOL_CANCEL_ROOM = "cancel-room"
PROTOCOL_ROOM_FULLY = "room-fully"
PROTOCOL_ROOM_NOT_FOUND = "room-not-found"
PROTOCOL_ROOM_WRONG_PASSWORD = "room-wrong-password"
PROTOCOL_GET_RANK_CHARTS = "get-rank-charts"
PROTOCOL_RETURN_GET_RANK_CHARTS = "return-get-rank-charts"
PROTOCOL_CHECK_FRIEND = "check-friend"
PROTOCOL_CHECK_FRIEND_RESPONSE = "check-friend-response"
PROTOCOL_MAKE_FRIEND = "make-friend"
PROTOCOL_MAKE_FRIEND_REQUEST = "make-friend-request"
PROTOCOL_MAKE_FRIEND_CONFIRM = "make-friend-confirm"
PROTOCOL_DUEL_REQUEST = "duel-request"
PROTOCOL_DUEL_NOTICE = "duel-notice"
PROTOCOL_AGREE_DUEL = "agree-duel"
PROTOCOL_DISAGREE_DUEL = "disagree-duel"
PROTOCOL_CARO = "caro"
PROTOCOL_WIN = "win"
PROTOCOL_LOSE = "lose"
PROTOCOL_DRAW_REQUEST = "draw-request"
PROTOCOL_DRAW_CONFIRM = "draw-confirm"
PROTOCOL_DRAW_REFUSE = "draw-refuse"
PROTOCOL_DRAW_GAME = "draw-game"
PROTOCOL_NEW_GAME = "new-game"
PROTOCOL_VOICE_MESSAGE = "voice-message"
PROTOCOL_LEFT_ROOM = "left-room"
PROTOCOL_COMPETITOR_TIME_OUT = "competitor-time-out"
PROTOCOL_BANNED_NOTICE = "banned-notice"
PROTOCOL_WARNING_NOTICE = "warning-notice"
PROTOCOL_ADMIN_BROADCAST = "admin-broadcast"

# Voice Messages
VOICE_CLOSE_MIC = "close-mic"
VOICE_OPEN_MIC = "open-mic"
VOICE_CLOSE_SPEAKER = "close-speaker"
VOICE_OPEN_SPEAKER = "open-speaker"
