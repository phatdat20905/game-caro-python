"""
Find Room Form - Search for specific room by ID
"""

import tkinter as tk
from tkinter import messagebox
from client.controller.client import Client
from shared.utils import create_message
from shared.constants import *

class FindRoomFrm:
    """Form for finding a specific room by ID"""
    
    def __init__(self):
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title("Tìm phòng")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        self.window.grab_set()  # Modal
        
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
            text="TÌM PHÒNG",
            font=("Arial", 16, "bold"),
            bg=COLOR_PRIMARY,
            fg="white"
        ).pack(pady=15)
        
        # Content
        content_frame = tk.Frame(self.window, padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Room ID input
        id_frame = tk.Frame(content_frame)
        id_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            id_frame,
            text="Mã phòng:",
            font=FONT_NORMAL,
            width=10,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.room_id_entry = tk.Entry(
            id_frame,
            font=FONT_NORMAL,
            width=15
        )
        self.room_id_entry.pack(side=tk.LEFT)
        self.room_id_entry.focus()
        
        # Buttons
        btn_frame = tk.Frame(content_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Tìm và vào",
            font=FONT_BUTTON,
            bg=COLOR_PRIMARY,
            fg="white",
            cursor="hand2",
            command=self.find_and_join,
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
        self.room_id_entry.bind('<Return>', lambda e: self.find_and_join())
    
    def find_and_join(self):
        """Find and join room"""
        room_id = self.room_id_entry.get().strip()
        
        if not room_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phòng!")
            return
        
        try:
            room_id = int(room_id)
            
            # Send find room request (same as go to room without password)
            if Client.socket_handle:
                Client.socket_handle.write(create_message(PROTOCOL_GO_TO_ROOM, room_id, ""))
            
            self.close()
        
        except ValueError:
            messagebox.showerror("Lỗi", "Mã phòng không hợp lệ!")
    
    def show(self):
        """Show window"""
        self.window.deiconify()
        self.window.wait_window()
    
    def close(self):
        """Close window - Java pattern: ONLY dispose, caller decides what to open next"""
        try:
            self.window.destroy()
        except:
            pass
