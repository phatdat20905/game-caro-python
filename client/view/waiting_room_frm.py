"""
Waiting Roo        self.window = tk.Toplevel(master)
        self.window.title(f"Phòng {self.room_id}")
        self.window.geometry("450x360")  # Optimized from 500x400
        self.window.resizable(False, False)rm - Room waiting for second player
"""

import tkinter as tk
from tkinter import messagebox
from client.controller.client import Client
from shared.utils import create_message
from shared.constants import *

class WaitingRoomFrm:
    """Waiting room form when creating/joining a room"""
    
    def __init__(self, room_id, password=""):
        # Use Client.root as master to avoid "main thread not in main loop" error
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title(f"Phòng chờ - {room_id}")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.room_id = room_id
        self.password = password
        
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
        title_frame = tk.Frame(self.window, bg=COLOR_PRIMARY, height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="PHÒNG CHỜ",
            font=("Arial", 20, "bold"),
            bg=COLOR_PRIMARY,
            fg="white"
        ).pack(pady=25)
        
        # Content
        content_frame = tk.Frame(self.window, padx=40, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Room info
        info_frame = tk.LabelFrame(content_frame, text="Thông tin phòng", font=FONT_BUTTON, padx=20, pady=20)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Room ID
        id_frame = tk.Frame(info_frame)
        id_frame.pack(fill=tk.X, pady=5)
        tk.Label(id_frame, text="Mã phòng:", font=FONT_NORMAL, width=12, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(id_frame, text=self.room_id, font=("Arial", 12, "bold"), fg=COLOR_PRIMARY).pack(side=tk.LEFT)
        
        # Password status
        password_frame = tk.Frame(info_frame)
        password_frame.pack(fill=tk.X, pady=5)
        tk.Label(password_frame, text="Bảo mật:", font=FONT_NORMAL, width=12, anchor=tk.W).pack(side=tk.LEFT)
        
        if self.password and self.password != " ":
            tk.Label(password_frame, text="🔒 Có mật khẩu", font=FONT_NORMAL, fg=COLOR_WARNING).pack(side=tk.LEFT)
        else:
            tk.Label(password_frame, text="🔓 Công khai", font=FONT_NORMAL, fg=COLOR_SUCCESS).pack(side=tk.LEFT)
        
        # Status
        status_frame = tk.Frame(info_frame)
        status_frame.pack(fill=tk.X, pady=5)
        tk.Label(status_frame, text="Trạng thái:", font=FONT_NORMAL, width=12, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(status_frame, text="Đang chờ đối thủ (1/2)", font=FONT_NORMAL, fg=COLOR_INFO).pack(side=tk.LEFT)
        
        # Waiting animation
        self.waiting_label = tk.Label(
            content_frame,
            text="⏳ Đang chờ người chơi thứ hai...",
            font=("Arial", 12),
            fg=COLOR_INFO
        )
        self.waiting_label.pack(pady=20)
        
        # Buttons
        btn_frame = tk.Frame(content_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Hủy phòng",
            font=FONT_BUTTON,
            bg=COLOR_DANGER,
            fg="white",
            cursor="hand2",
            command=self.cancel_room,
            width=15
        ).pack()
    
    def cancel_room(self):
        """Cancel the room"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy phòng?"):
            # Send cancel message to server
            if Client.socket_handle:
                Client.socket_handle.write(create_message(PROTOCOL_CANCEL_ROOM))
            
            self.close()
            Client.open_homepage()
    
    def on_closing(self):
        """Handle window close button"""
        self.cancel_room()
    
    def show(self):
        """Show window"""
        self.window.deiconify()
    
    def close(self):
        """Close window"""
        try:
            self.window.destroy()
        except:
            pass
