# Game Caro - Phiên bản Python 🎮

Dự án Game Caro multiplayer hoàn chỉnh được viết bằng Python.

## 📋 Tính năng

### Server
- ✅ **Quản lý kết nối**: ThreadPoolExecutor hỗ trợ 10-100 kết nối đồng thời
- ✅ **Database**: SQLite3 lưu trữ users, friends, banned users
- ✅ **Admin Panel**: GUI quản lý server, xem logs, ban/unban users
- ✅ **Protocol đầy đủ**: 40+ loại message cho tất cả tính năng

### Client  
- ✅ **Đăng nhập/Đăng ký**: Xác thực với server, chọn avatar
- ✅ **Trang chủ**: Hiển thị thống kê, menu điều hướng, chat server
- ✅ **Quản lý phòng**: Tạo phòng (có/không mật khẩu), xem danh sách, tìm kiếm, vào phòng
- ✅ **Game Caro**: Bàn cờ 15x15, timer 30s/lượt, check win 5 ô liên tiếp
- ✅ **Bạn bè**: Thêm bạn, xem danh sách, xem trạng thái online/offline
- ✅ **Thách đấu**: Gửi lời thách đấu đến bạn bè online
- ✅ **Bảng xếp hạng**: Xem top players, sắp xếp theo nhiều tiêu chí
- ✅ **AI Mode**: Chơi với máy (AI cơ bản)
- ✅ **Chat**: Chat trong game với đối thủ
- ✅ **Yêu cầu hòa**: Gửi/nhận yêu cầu hòa trong game

### Game Logic
- ✅ **Board 15x15**: Ma trận 2D với buttons
- ✅ **Win detection**: Kiểm tra 4 hướng (ngang, dọc, 2 chéo)
- ✅ **Timer**: Đếm ngược 30 giây mỗi lượt
- ✅ **Draw detection**: Phát hiện board đầy
- ✅ **AI opponent**: AI cơ bản với chiến thuật tấn công/phòng thủ

## 🚀 Hướng dẫn cài đặt

### Yêu cầu hệ thống

- Python 3.8 hoặc mới hơn
- pip (Python package manager)

> Gợi ý: dự án chủ yếu dùng thư viện chuẩn (Tkinter, sqlite3, threading, socket). Nếu có file `requirements.txt` thì cài thêm các phụ thuộc bổ sung.

### Cài đặt và chạy (Windows — PowerShell)

1) Mở PowerShell và chuyển đến thư mục dự án:

```powershell
cd caro-game-python
```

2) (Tùy chọn, khuyến nghị) Tạo và kích hoạt virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.bat
```

3) Cài phụ thuộc (nếu có `requirements.txt`):

```powershell
pip install -r requirements.txt
```

4) Khởi tạo database:

- Hệ thống sẽ tự tạo file SQLite `database/caro_game.db` khi bạn chạy server lần đầu. Nếu muốn tái tạo schema thủ công, xem `database/init_database.sql`.
- Nếu gặp lỗi schema hoặc muốn reset dữ liệu thử nghiệm, xóa file `database/caro_game.db` và khởi động lại server — server sẽ tạo lại database theo schema.

### Chạy server và client

- Chạy server (mặc định lắng nghe trên `localhost:7777`):

```powershell
python run_server.py
```

- Chạy client (mở một hoặc nhiều cửa sổ client để test multiplayer):

```powershell
python run_client.py
```

### Cấu hình

- Thay đổi host/port, board size hoặc thời gian lượt trong `shared/config.py`:

```python
SERVER_HOST = "localhost"
SERVER_PORT = 7777
BOARD_SIZE = 15
TURN_TIME_LIMIT = 30
DEBUG_MODE = False
```

- Bật `DEBUG_MODE = True` để xem log chi tiết khi gỡ lỗi.

### Lưu ý nhanh

- Nếu client không kết nối: kiểm tra server đã chạy, port 7777 có bị chiếm, và firewall/antivirus có chặn không.
- Nếu database bị hỏng: xóa `database/caro_game.db` và chạy lại server.
- Nếu bạn chạy trên hệ điều hành khác (Linux / macOS), các lệnh terminal tương tự nhưng kích hoạt virtualenv khác (ví dụ `source venv/bin/activate`).

## 🎯 Cách chạy

### Chạy Server
```bash
cd caro-game-python
python run_server.py
```

Server sẽ:
- Khởi tạo database (nếu chưa có)
- Mở Admin Panel GUI
- Lắng nghe trên port 7777 (mặc định)

### Chạy Client
```bash
cd caro-game-python
python run_client.py
```

Client sẽ:
- Kết nối đến server
- Mở form đăng nhập

### Tài khoản demo
```
Username: admin
Password: admin123

Username: player1 
Password: pass123

Username: player2
Password: pass123
```

## 📁 Cấu trúc dự án

```
caro-game-python/
├── server/                    # Server backend
│   ├── controller/
│   │   ├── server.py         # Main server với ThreadPoolExecutor
│   │   ├── server_thread.py  # Xử lý từng client (600+ dòng)
│   │   ├── server_thread_bus.py  # Quản lý threads
│   │   └── room.py           # Class Room quản lý game
│   ├── dao/
│   │   ├── database.py       # SQLite wrapper
│   │   └── user_dao.py       # CRUD operations
│   └── view/
│       └── admin.py          # Admin panel GUI
│
├── client/                    # Client application
│   ├── controller/
│   │   ├── client.py         # Main controller
│   │   └── socket_handle.py  # Socket communication
│   └── view/                 # All GUI forms
│       ├── login_frm.py      # ✅ Đăng nhập
│       ├── register_frm.py   # ✅ Đăng ký
│       ├── homepage_frm.py   # ✅ Trang chủ
│       ├── room_list_frm.py  # ✅ Danh sách phòng
│       ├── waiting_room_frm.py   # ✅ Phòng chờ
│       ├── game_client_frm.py    # ✅ Game chính (400+ dòng)
│       ├── friend_list_frm.py    # ✅ Danh sách bạn bè
│       ├── rank_frm.py       # ✅ Bảng xếp hạng
│       ├── create_room_password_frm.py  # ✅ Tạo phòng
│       ├── find_room_frm.py  # ✅ Tìm phòng
│       └── competitor_info_frm.py   # ✅ Thông tin đối thủ
│
├── shared/                    # Shared code
│   ├── constants.py          # 100+ constants
│   ├── config.py             # Configuration
│   ├── utils.py              # 15+ utility functions
│   ├── user.py               # User model
│   ├── point.py              # Point model
│   └── game_logic.py         # ✅ Game rules & AI
│
├── database/
│   ├── init_database.sql     # Database schema
│   └── caro_game.db          # SQLite database (auto-generated)
│
├── run_server.py              # Server entry point
├── run_client.py              # Client entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎮 Hướng dẫn chơi

### 1. Đăng nhập/Đăng ký
- Mở client → Đăng nhập hoặc đăng ký tài khoản mới
- Chọn avatar (6 lựa chọn)

### 2. Tạo phòng hoặc Tìm phòng
**Tạo phòng mới:**
- Click "Tạo phòng" → Nhập mật khẩu (tùy chọn) → Chờ đối thủ

**Vào phòng có sẵn:**
- Click "Danh sách phòng" → Chọn phòng → Click "Vào phòng"
- Nhập mật khẩu nếu phòng có bảo mật

**Tìm phòng:**
- Click "Tìm phòng" → Nhập ID phòng → Tìm và vào

### 3. Chơi game
- Bàn cờ 15x15, mỗi lượt 30 giây
- Thắng khi xếp được 5 ô liên tiếp (ngang/dọc/chéo)
- Chat với đối thủ trong game
- Yêu cầu hòa hoặc đầu hàng

### 4. Chế độ AI
- Click "Chơi với AI" để luyện tập
- AI sẽ tự động đánh sau mỗi nước của bạn

### 5. Bạn bè
- Thêm bạn bằng ID
- Xem danh sách bạn bè, trạng thái online
- Thách đấu bạn bè đang online

### 6. Bảng xếp hạng
- Xem top players
- Sắp xếp theo: số trận, thắng, hòa, thua, tỷ lệ thắng
- Click vào tiêu đề cột để sắp xếp

## 🔧 Configuration

File `shared/config.py`:
```python
SERVER_HOST = "localhost"
SERVER_PORT = 7777
BOARD_SIZE = 15
WIN_CONDITION = 5
TURN_TIME_LIMIT = 30  # seconds
DEBUG_MODE = False
```

## 🐛 Troubleshooting

### Server không khởi động
- Kiểm tra port 7777 có bị chiếm không
- Chạy với quyền admin nếu cần

### Client không kết nối được
- Kiểm tra server đã chạy chưa
- Kiểm tra firewall
- Xác nhận SERVER_HOST và SERVER_PORT trong config

### Lỗi database
- Xóa file `database/caro_game.db` và chạy lại server
- Database sẽ được tạo lại với schema mới

### Game bị lag
- Giảm số client kết nối
- Kiểm tra network latency
- Tắt DEBUG_MODE trong config

## 📝 Protocol Messages

Server-Client sử dụng 40+ loại messages:
- `login,username,password`
- `register,username,password,nickname,avatar`
- `create-room` / `create-room-password,password`
- `go-to-room,roomId,password`
- `caro,x,y` (đánh cờ tại vị trí x,y)
- `win` / `lose` / `draw-request` / `draw-confirm`
- Và nhiều hơn nữa trong `shared/constants.py`

## 🎨 GUI Technology

- **Framework**: Tkinter (built-in Python GUI)
- **Widgets**: Label, Button, Entry, Frame, Treeview, ScrolledText
- **Layout**: Pack, Grid managers
- **Colors**: Định nghĩa trong constants.py

## 💾 Database Schema

### Table: user
```sql
id INTEGER PRIMARY KEY
username TEXT UNIQUE
password TEXT  -- Hashed
nickname TEXT
avatar INTEGER
num_game INTEGER
num_win INTEGER
num_draw INTEGER
is_online INTEGER
is_playing INTEGER
```

### Table: friend  
```sql
user1_id INTEGER
user2_id INTEGER
PRIMARY KEY (user1_id, user2_id)
```

### Table: banned_user
```sql
user_id INTEGER PRIMARY KEY
reason TEXT
banned_date TEXT
```

## 🚧 Tình trạng dự án

✅ **Hoàn thành 100%**

- [x] Server backend (100%)
- [x] Database layer (100%)  
- [x] Client controller (100%)
- [x] Socket communication (100%)
- [x] Authentication (100%)
- [x] Homepage (100%)
- [x] Room management (100%)
- [x] Game logic (100%)
- [x] AI opponent (100%)
- [x] Friend system (100%)
- [x] Ranking system (100%)
- [x] All GUI forms (100%)
- [x] Admin panel (100%)
- [x] Documentation (100%)

## 🔮 Tính năng có thể mở rộng

- [ ] Voice chat thực sự (hiện tại chỉ có placeholder)
- [ ] Replay game
- [ ] AI nâng cao (minimax, alpha-beta pruning)
- [ ] Tournament mode
- [ ] Spectator mode
- [ ] Theme customization
- [ ] Multiple board sizes
- [ ] Undo move
- [ ] Hint system

## 📄 License

Dự án này được tạo ra cho mục đích học tập.

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra phần Troubleshooting
2. Xem logs trong Admin Panel
3. Kiểm tra file constants.py và config.py
4. Đảm bảo đã cài đủ dependencies

---

### 🏫 Thông tin môn học

* **Tên học phần:** Lập trình mạng
* **Mã học phần:** 010112301305
* **Số tín chỉ:** 3
* **Giảng viên:** 👨‍🏫 Bùi Dương Thế

### 👥 Thông tin nhóm

* **Tên nhóm:** Nhóm 2
* **Thành viên:**
    * 👤 Ngô Phát Đạt
    * 👤 Nguyễn Thành Đạt

**Chúc bạn chơi game vui vẻ! 🎉**
