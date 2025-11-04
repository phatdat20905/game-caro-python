"""
Create Room Password Form - Set password when creating a room
"""

import tkinter as tk
from tkinter import messagebox
from client.controller.client import Client
from shared.utils import create_message
from shared.constants import *

class CreateRoomPasswordFrm:
    """Form for setting password when creating a room"""
    
    def __init__(self):
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title("Tạo phòng")
        self.window.geometry("400x250")
        self.window.resizable(False, False)
        self.window.grab_set()  # Modal
        
        self.password = None
        
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
        # Title
        title_frame = tk.Frame(self.window, bg=COLOR_PRIMARY, height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="TẠO PHÒNG MỚI",
            font=("Arial", 16, "bold"),
            bg=COLOR_PRIMARY,
            fg="white"
        ).pack(pady=15)
        
        # Content
        content_frame = tk.Frame(self.window, padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info
        tk.Label(
            content_frame,
            text="Bạn có muốn đặt mật khẩu cho phòng?",
            font=FONT_NORMAL
        ).pack(pady=(0, 15))
        
        # Password input
        password_frame = tk.Frame(content_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            password_frame,
            text="Mật khẩu:",
            font=FONT_NORMAL,
            width=10,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=FONT_NORMAL,
            show="●",
            width=20
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.password_entry.focus()
        
        # Note
        tk.Label(
            content_frame,
            text="(Để trống nếu không cần mật khẩu)",
            font=FONT_SMALL,
            fg="gray"
        ).pack()
        
        # Buttons
        btn_frame = tk.Frame(content_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Tạo phòng",
            font=FONT_BUTTON,
            bg=COLOR_SUCCESS,
            fg="white",
            cursor="hand2",
            command=self.create_room,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Hủy",
            font=FONT_BUTTON,
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            cursor="hand2",
            command=self.close,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.create_room())
    
    def create_room(self):
        """Create room with password"""
        password = self.password_entry.get().strip()
        
        # Send create room request
        if Client.socket_handle:
            if password:
                # Create room with password
                Client.socket_handle.write(create_message(PROTOCOL_CREATE_ROOM_PASSWORD, password))
            else:
                # Create room without password
                Client.socket_handle.write(create_message(PROTOCOL_CREATE_ROOM))
        
        self.close()
    
    def show(self):
        """Show window"""
        self.window.deiconify()
        self.window.wait_window()
    
    def close(self):
        """Close window"""
        try:
            self.window.destroy()
        except:
            pass
