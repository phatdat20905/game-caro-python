"""
Create Roo        self.window = tk.Toplevel(master)
        self.window.title("Tạo phòng mới")
        self.window.geometry("400x450")  # Optimized from 450x500
        self.window.resizable(False, False)rm - Choose public/private room
"""

import tkinter as tk
from tkinter import messagebox
from client.controller.client import Client
from shared.utils import create_message
from shared.constants import *

class CreateRoomFrm:
    """Create room form with public/private option"""
    
    def __init__(self):
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title("Tạo phòng chơi")
        self.window.geometry("450x500")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        # Room type: 0 = public, 1 = private
        self.room_type = tk.IntVar(value=0)
        
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
        # Main frame
        main_frame = tk.Frame(self.window, bg=COLOR_BACKGROUND, padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="TẠO PHÒNG CHƠI",
            font=FONT_TITLE,
            bg=COLOR_BACKGROUND,
            fg=COLOR_PRIMARY
        )
        title_label.pack(pady=(0, 20))
        
        # Instructions
        tk.Label(
            main_frame,
            text="Chọn loại phòng bạn muốn tạo:",
            font=FONT_NORMAL,
            bg=COLOR_BACKGROUND
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Room type selection
        room_type_frame = tk.Frame(main_frame, bg=COLOR_BACKGROUND)
        room_type_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Public room option
        public_frame = tk.Frame(room_type_frame, bg=COLOR_LIGHT, padx=15, pady=15)
        public_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Radiobutton(
            public_frame,
            text="🌐 Phòng Công Khai",
            variable=self.room_type,
            value=0,
            font=FONT_BUTTON,
            bg=COLOR_LIGHT,
            activebackground=COLOR_LIGHT,
            command=self.on_room_type_change
        ).pack(anchor=tk.W)
        
        tk.Label(
            public_frame,
            text="• Mọi người đều có thể vào\n• Không cần mật khẩu\n• Hiển thị trong danh sách phòng",
            font=FONT_SMALL,
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=(25, 0), pady=(5, 0))
        
        # Private room option
        private_frame = tk.Frame(main_frame, bg=COLOR_LIGHT, padx=15, pady=15)
        private_frame.pack(fill=tk.X)
        
        tk.Radiobutton(
            private_frame,
            text="🔒 Phòng Riêng Tư",
            variable=self.room_type,
            value=1,
            font=FONT_BUTTON,
            bg=COLOR_LIGHT,
            activebackground=COLOR_LIGHT,
            command=self.on_room_type_change
        ).pack(anchor=tk.W)
        
        tk.Label(
            private_frame,
            text="• Chỉ người có mật khẩu mới vào được\n• Bảo mật cao\n• Chơi với bạn bè",
            font=FONT_SMALL,
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=(25, 0), pady=(5, 0))
        
        # Password frame (only show for private)
        self.password_frame = tk.Frame(private_frame, bg=COLOR_LIGHT)
        self.password_frame.pack(fill=tk.X, padx=(25, 0), pady=(10, 0))
        
        tk.Label(
            self.password_frame,
            text="Mật khẩu phòng:",
            font=FONT_NORMAL,
            bg=COLOR_LIGHT
        ).pack(anchor=tk.W)
        
        self.password_entry = tk.Entry(
            self.password_frame,
            font=FONT_NORMAL,
            width=20,
            show="●"
        )
        self.password_entry.pack(anchor=tk.W, pady=(5, 0))
        
        # Hide password frame initially
        self.password_frame.pack_forget()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=COLOR_BACKGROUND)
        button_frame.pack(pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="TẠO PHÒNG",
            font=FONT_BUTTON,
            bg=COLOR_PRIMARY,
            fg="white",
            activebackground=COLOR_INFO,
            activeforeground="white",
            cursor="hand2",
            command=self.create_room,
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="HỦY",
            font=FONT_BUTTON,
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            activebackground=COLOR_BACKGROUND,
            cursor="hand2",
            command=self.close,
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=5)
    
    def on_room_type_change(self):
        """Handle room type selection change"""
        if self.room_type.get() == 1:  # Private
            self.password_frame.pack(fill=tk.X, padx=(25, 0), pady=(10, 0))
            self.password_entry.focus()
        else:  # Public
            self.password_frame.pack_forget()
    
    def create_room(self):
        """Create room based on selection"""
        if self.room_type.get() == 1:  # Private
            password = self.password_entry.get().strip()
            if not password:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập mật khẩu phòng!")
                self.password_entry.focus()
                return
            if len(password) < 3:
                messagebox.showwarning("Cảnh báo", "Mật khẩu phải có ít nhất 3 ký tự!")
                self.password_entry.focus()
                return
        else:  # Public
            password = ""
        
        # Send create room request
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_CREATE_ROOM, password))
            self.close()
        else:
            messagebox.showerror("Lỗi", "Chưa kết nối đến server!")
    
    def show(self):
        """Show window"""
        self.window.deiconify()
    
    def close(self):
        """Close window"""
        try:
            self.window.destroy()
        except:
            pass
