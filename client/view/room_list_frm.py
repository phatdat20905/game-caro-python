"""
Room List Form - Complete implementation
"""

import tkinter as tk
from tkinter import ttk, messagebox
from client.controller.client import Client
from shared.utils import create_message
from shared.constants import *

class RoomListFrm:
    """Room list form with complete table view"""
    
    def __init__(self):
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title("Danh sách phòng")
        self.window.geometry("620x460")  # Optimized from 700x500
        self.window.resizable(False, False)
        
        self.rooms_data = []  # Store room data
        
        self.setup_ui()
        self.center_window()
        
        # Request room list from server
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_VIEW_ROOM_LIST))
    
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
            text="DANH SÁCH PHÒNG",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARY,
            fg="white"
        ).pack(pady=15)
        
        # Main content
        content_frame = tk.Frame(self.window, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        tk.Label(
            content_frame,
            text="Chọn phòng và nhấn 'Vào phòng' để tham gia",
            font=FONT_NORMAL
        ).pack(pady=(0, 10))
        
        # Table frame
        table_frame = tk.Frame(content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (table)
        self.room_table = ttk.Treeview(
            table_frame,
            columns=("Room", "Status", "Password"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12
        )
        
        # Configure columns
        self.room_table.heading("Room", text="Tên phòng")
        self.room_table.heading("Status", text="Trạng thái")
        self.room_table.heading("Password", text="Bảo mật")
        
        self.room_table.column("Room", width=200, anchor=tk.W)
        self.room_table.column("Status", width=150, anchor=tk.CENTER)
        self.room_table.column("Password", width=120, anchor=tk.CENTER)
        
        self.room_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.room_table.yview)
        
        # Buttons frame
        btn_frame = tk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(
            btn_frame,
            text="Làm mới",
            font=FONT_BUTTON,
            bg=COLOR_INFO,
            fg="white",
            cursor="hand2",
            command=self.refresh_rooms,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Vào phòng",
            font=FONT_BUTTON,
            bg=COLOR_SUCCESS,
            fg="white",
            cursor="hand2",
            command=self.join_room,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Quay lại",
            font=FONT_BUTTON,
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            cursor="hand2",
            command=self.back,
            width=12
        ).pack(side=tk.RIGHT, padx=5)
    
    def update_room_list(self, rooms, passwords):
        """
        Update room list display
        
        Args:
            rooms: List of room names (e.g., ["Phòng 100", "Phòng 101"])
            passwords: List of passwords (e.g., [" ", "123"])
        """
        # Clear current items
        for item in self.room_table.get_children():
            self.room_table.delete(item)
        
        # Store data
        self.rooms_data = []
        
        # Add rooms to table
        if not rooms or len(rooms) == 0:
            # No rooms available
            self.room_table.insert(
                "",
                tk.END,
                values=("Không có phòng nào", "-", "-")
            )
        else:
            for i, room_name in enumerate(rooms):
                # Extract room ID from name (e.g., "Phòng 100" -> "100")
                room_id = room_name.replace("Phòng ", "")
                
                # Get password status
                password = passwords[i] if i < len(passwords) else " "
                has_password = password != " "
                password_status = "Có mật khẩu" if has_password else "Công khai"
                
                # Insert into table
                self.room_table.insert(
                    "",
                    tk.END,
                    values=(room_name, "Đang chờ (1/2)", password_status)
                )
                
                # Store data for joining
                self.rooms_data.append({
                    "id": room_id,
                    "name": room_name,
                    "password": password,
                    "has_password": has_password
                })
    
    def join_room(self):
        """Join selected room"""
        selected = self.room_table.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return
        
        # Get selected index
        selected_item = self.room_table.selection()[0]
        index = self.room_table.index(selected_item)
        
        if index >= len(self.rooms_data):
            messagebox.showwarning("Cảnh báo", "Không thể vào phòng này!")
            return
        
        room_data = self.rooms_data[index]
        room_id = room_data["id"]
        
        # Check if room requires password
        if room_data["has_password"]:
            # Ask for password
            password = self.ask_password(room_data["name"])
            if password is None:
                return  # User cancelled
            
            # Send join request with password
            if Client.socket_handle:
                Client.socket_handle.write(create_message(
                    PROTOCOL_GO_TO_ROOM,
                    room_id,
                    password
                ))
        else:
            # Send join request without password
            if Client.socket_handle:
                Client.socket_handle.write(create_message(
                    PROTOCOL_GO_TO_ROOM,
                    room_id,
                    ""
                ))
    
    def ask_password(self, room_name):
        """
        Ask user for room password
        
        Args:
            room_name: Name of the room
        
        Returns:
            Password string or None if cancelled
        """
        # Create password dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Nhập mật khẩu")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        result = {"password": None}
        
        # Content
        tk.Label(
            dialog,
            text=f"Nhập mật khẩu cho {room_name}:",
            font=FONT_NORMAL
        ).pack(pady=(20, 10))
        
        password_entry = tk.Entry(dialog, font=FONT_NORMAL, show="●", width=25)
        password_entry.pack(pady=10)
        password_entry.focus()
        
        # Buttons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def ok():
            result["password"] = password_entry.get()
            dialog.destroy()
        
        def cancel():
            result["password"] = None
            dialog.destroy()
        
        tk.Button(
            btn_frame,
            text="OK",
            command=ok,
            bg=COLOR_PRIMARY,
            fg="white",
            font=FONT_BUTTON,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Hủy",
            command=cancel,
            bg=COLOR_LIGHT,
            font=FONT_BUTTON,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        password_entry.bind('<Return>', lambda e: ok())
        
        dialog.wait_window()
        return result["password"]
    
    def refresh_rooms(self):
        """Refresh room list"""
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_VIEW_ROOM_LIST))
    
    def back(self):
        """Go back to homepage"""
        self.close()
        Client.open_homepage()
    
    def show(self):
        """Show window"""
        self.window.deiconify()
    
    def close(self):
        """Close window"""
        try:
            self.window.destroy()
        except:
            pass
