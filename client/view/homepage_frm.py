"""
Homepage Form - Main menu after login
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from client.controller.client import Client
from shared.utils import create_message, format_win_ratio, calculate_mark
from shared.constants import *

class HomePageFrm:
    """Homepage form - main menu"""
    
    def __init__(self):
        # Always use Toplevel, never reassign Client.root
        if hasattr(Client, 'root') and Client.root:
            self.window = tk.Toplevel(Client.root)
            self.is_main_window = False
        else:
            # Fallback: create new Tk (shouldn't happen in normal flow)
            self.window = tk.Tk()
            self.is_main_window = True
            # DON'T reassign Client.root - let run_client.py handle it
        
        self.window.title("Trang chủ - Caro Game")
        self.window.geometry("720x550")  # Optimized from 800x600
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup UI components"""
        # Title bar
        title_frame = tk.Frame(self.window, bg=COLOR_PRIMARY, height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="CARO GAME - TRANG CHỦ",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARY,
            fg="white"
        ).pack(pady=15)
        
        # Main content
        content_frame = tk.Frame(self.window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - User info
        left_panel = tk.Frame(content_frame, bg=COLOR_LIGHT, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.setup_user_info(left_panel)
        
        # Right panel - Menu and chat
        right_panel = tk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Menu buttons
        menu_frame = tk.LabelFrame(right_panel, text="Menu", font=FONT_BUTTON, padx=10, pady=10)
        menu_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.setup_menu_buttons(menu_frame)
        
        # Chat
        chat_frame = tk.LabelFrame(right_panel, text="Chat Server", font=FONT_BUTTON, padx=10, pady=10)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_chat(chat_frame)
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_user_info(self, parent):
        """Setup user information panel"""
        tk.Label(
            parent,
            text="THÔNG TIN",
            font=FONT_BUTTON,
            bg=COLOR_LIGHT
        ).pack(pady=(10, 20))
        
        # Avatar display
        avatar_frame = tk.Frame(parent, bg=COLOR_LIGHT, width=100, height=100)
        avatar_frame.pack(pady=10)
        avatar_frame.pack_propagate(False)
        
        # Try to load avatar image
        if Client.user and hasattr(Client.user, 'get_avatar'):
            try:
                from PIL import Image, ImageTk
                from shared.utils import get_asset_path
                import os
                
                avatar_id = Client.user.get_avatar()
                avatar_path = get_asset_path('avatar', f'{avatar_id}.jpg')
                
                if os.path.exists(avatar_path):
                    img = Image.open(avatar_path)
                    img = img.resize((100, 100), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    avatar_label = tk.Label(avatar_frame, image=photo, bg=COLOR_LIGHT)
                    avatar_label.image = photo  # Keep reference!
                    avatar_label.pack()
                else:
                    tk.Label(avatar_frame, text="Avatar", bg="gray", fg="white").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            except Exception as e:
                tk.Label(avatar_frame, text="Avatar", bg="gray", fg="white").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            tk.Label(avatar_frame, text="Avatar", bg="gray", fg="white").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # User stats
        if Client.user:
            self.nickname_label = tk.Label(
                parent,
                text=Client.user.get_nickname(),
                font=("Arial", 14, "bold"),
                bg=COLOR_LIGHT
            )
            self.nickname_label.pack(pady=5)
            
            stats_frame = tk.Frame(parent, bg=COLOR_LIGHT)
            stats_frame.pack(fill=tk.X, padx=20, pady=10)
            
            # Stats labels
            user = Client.user
            stats = [
                ("Số ván:", user.get_number_of_game()),
                ("Thắng:", user.get_number_of_win()),
                ("Hòa:", user.get_number_of_draw()),
                ("Tỷ lệ thắng:", format_win_ratio(user.get_number_of_win(), user.get_number_of_game())),
                ("Điểm:", calculate_mark(user.get_number_of_game(), user.get_number_of_win())),
                ("Hạng:", user.get_rank())
            ]
            
            for label, value in stats:
                row = tk.Frame(stats_frame, bg=COLOR_LIGHT)
                row.pack(fill=tk.X, pady=2)
                tk.Label(row, text=label, font=FONT_SMALL, bg=COLOR_LIGHT).pack(side=tk.LEFT)
                tk.Label(row, text=str(value), font=FONT_SMALL, bg=COLOR_LIGHT, fg=COLOR_PRIMARY).pack(side=tk.RIGHT)
    
    def setup_menu_buttons(self, parent):
        """Setup menu buttons"""
        buttons = [
            ("🎮 Tìm phòng nhanh", self.quick_match, COLOR_SUCCESS),
            ("➕ Tạo phòng", self.create_room, COLOR_PRIMARY),
            ("🔍 Danh sách phòng", self.room_list, COLOR_INFO),
            ("👥 Bạn bè", self.friend_list, COLOR_WARNING),
            ("🏆 Bảng xếp hạng", self.rank_board, "#9C27B0"),
            ("🤖 Chơi với AI", self.play_ai, "#607D8B"),
            ("🚪 Đăng xuất", self.logout, COLOR_DANGER),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                parent,
                text=text,
                font=FONT_BUTTON,
                bg=color,
                fg="white",
                activebackground=color,
                cursor="hand2",
                command=command,
                width=25,
                height=2
            )
            btn.pack(pady=5, padx=10)
    
    def setup_chat(self, parent):
        """Setup chat area"""
        # Chat display
        self.chat_text = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=FONT_SMALL,
            height=12,
            state=tk.DISABLED
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chat input
        input_frame = tk.Frame(parent)
        input_frame.pack(fill=tk.X)
        
        self.chat_input = tk.Entry(input_frame, font=FONT_NORMAL)
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.chat_input.bind('<Return>', lambda e: self.send_message())
        
        send_btn = tk.Button(
            input_frame,
            text="Gửi",
            font=FONT_BUTTON,
            bg=COLOR_PRIMARY,
            fg="white",
            cursor="hand2",
            command=self.send_message,
            width=8
        )
        send_btn.pack(side=tk.RIGHT)
    
    def add_message(self, message):
        """Add message to chat"""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
    
    def send_message(self):
        """Send chat message"""
        message = self.chat_input.get().strip()
        if message and Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_CHAT_SERVER, message))
            self.chat_input.delete(0, tk.END)
    
    # Button handlers
    def quick_match(self):
        """Quick match"""
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_QUICK_ROOM))
            # Don't open waiting room immediately
            # Wait for server response (PROTOCOL_GO_TO_ROOM or PROTOCOL_YOUR_CREATED_ROOM)
            # Server will send room_id in response
            self.close()
    
    def create_room(self):
        """Create room - Java pattern: ask for password, then close homepage"""
        # Ask if user wants to set password
        result = messagebox.askyesno(
            "Tạo phòng",
            "Bạn có muốn đặt mật khẩu cho phòng không?"
        )
        
        if result:  # YES - wants password
            self.close()
            Client.open_create_room_password()
        else:  # NO - public room
            try:
                Client.socket_handle.write(create_message(PROTOCOL_CREATE_ROOM))
                self.close()  # Close homepage, waiting room will open when server responds
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo phòng: {str(e)}")
    
    def room_list(self):
        """Show room list - Java pattern: close homepage, open room list, send protocol"""
        try:
            self.close()
            Client.open_room_list()
            Client.socket_handle.write(create_message(PROTOCOL_VIEW_ROOM_LIST))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xem danh sách phòng: {str(e)}")
    
    def friend_list(self):
        """Show friend list"""
        self.close()
        Client.open_friend_list()
    
    def rank_board(self):
        """Show rank board"""
        Client.open_rank()
    
    def play_ai(self):
        """Play with AI"""
        Client.open_ai_game()
    
    def logout(self):
        """Logout"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            if Client.socket_handle and Client.user:
                Client.socket_handle.write(create_message(PROTOCOL_OFFLINE, Client.user.get_id()))
            self.close()
            Client.open_login()
    
    def on_closing(self):
        """Handle window closing - CRITICAL FIX"""
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn đăng xuất và thoát?"):
            # Logout first
            try:
                if Client.socket_handle:
                    Client.socket_handle.write("logout,")
                    Client.socket_handle.close()
            except:
                pass
            
            # Destroy all windows
            try:
                if hasattr(Client, 'root') and Client.root:
                    Client.root.destroy()
            except:
                pass
            
            # Force exit
            import sys
            sys.exit(0)
    
    def show(self):
        """Show window"""
        self.window.deiconify()
        # Don't call mainloop here - it's called in run_client.py
    
    def close(self):
        """Close window"""
        try:
            self.window.destroy()
        except:
            pass
