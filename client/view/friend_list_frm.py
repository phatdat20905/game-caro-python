"""
Friend List Form - Complete implementation
"""

import tkinter as tk
from tkinter import ttk, messagebox
from client.controller.client import Client
from shared.utils import create_message
from shared.constants import *

class FriendListFrm:
    """Friend list form with management features"""
    
    def __init__(self):
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title("Danh sách bạn bè")
        self.window.geometry("620x500")  # Optimized from 700x550
        self.window.resizable(False, False)
        
        self.friends_data = []  # Store friend data
        
        self.setup_ui()
        self.center_window()
        
        # Request friend list from server
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_VIEW_FRIEND_LIST))
    
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
            text="DANH SÁCH BẠN BÈ",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARY,
            fg="white"
        ).pack(pady=15)
        
        # Main content
        content_frame = tk.Frame(self.window, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add friend section
        add_frame = tk.LabelFrame(content_frame, text="Thêm bạn bè", font=FONT_BUTTON, padx=10, pady=10)
        add_frame.pack(fill=tk.X, pady=(0, 15))
        
        input_frame = tk.Frame(add_frame)
        input_frame.pack()
        
        tk.Label(input_frame, text="ID người chơi:", font=FONT_NORMAL).pack(side=tk.LEFT, padx=5)
        
        self.friend_id_entry = tk.Entry(input_frame, font=FONT_NORMAL, width=15)
        self.friend_id_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            input_frame,
            text="Gửi lời mời",
            font=FONT_BUTTON,
            bg=COLOR_SUCCESS,
            fg="white",
            cursor="hand2",
            command=self.send_friend_request,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Friend list table
        table_frame = tk.Frame(content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.friend_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Nickname", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12
        )
        
        # Configure columns
        self.friend_table.heading("ID", text="ID")
        self.friend_table.heading("Nickname", text="Tên")
        self.friend_table.heading("Status", text="Trạng thái")
        
        self.friend_table.column("ID", width=80, anchor=tk.CENTER)
        self.friend_table.column("Nickname", width=250, anchor=tk.W)
        self.friend_table.column("Status", width=150, anchor=tk.CENTER)
        
        self.friend_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.friend_table.yview)
        
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
            command=self.refresh_friends,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Thách đấu",
            font=FONT_BUTTON,
            bg=COLOR_WARNING,
            fg="white",
            cursor="hand2",
            command=self.challenge_friend,
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
    
    def update_friend_list(self, friends):
        """
        Update friend list display
        
        Args:
            friends: List of User objects
        """
        # Clear current items
        for item in self.friend_table.get_children():
            self.friend_table.delete(item)
        
        # Store data
        self.friends_data = friends
        
        # Add friends to table
        if not friends or len(friends) == 0:
            self.friend_table.insert(
                "",
                tk.END,
                values=("-", "Chưa có bạn bè", "-")
            )
        else:
            for friend in friends:
                # Determine status
                if friend.get_is_playing():
                    status = "🎮 Đang chơi"
                    tag = "playing"
                elif friend.get_is_online():
                    status = "🟢 Online"
                    tag = "online"
                else:
                    status = "⚫ Offline"
                    tag = "offline"
                
                # Insert into table
                item = self.friend_table.insert(
                    "",
                    tk.END,
                    values=(friend.get_id(), friend.get_nickname(), status),
                    tags=(tag,)
                )
        
        # Configure tags for colors
        self.friend_table.tag_configure("online", foreground=COLOR_SUCCESS)
        self.friend_table.tag_configure("playing", foreground=COLOR_WARNING)
        self.friend_table.tag_configure("offline", foreground="gray")
    
    def send_friend_request(self):
        """Send friend request"""
        friend_id = self.friend_id_entry.get().strip()
        
        if not friend_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID người chơi!")
            return
        
        try:
            friend_id = int(friend_id)
            
            # Check if it's yourself
            if Client.user and friend_id == Client.user.get_id():
                messagebox.showwarning("Cảnh báo", "Bạn không thể kết bạn với chính mình!")
                return
            
            # Send friend request
            if Client.socket_handle:
                Client.socket_handle.write(create_message(PROTOCOL_MAKE_FRIEND, friend_id))
                self.friend_id_entry.delete(0, tk.END)
                messagebox.showinfo("Thành công", "Đã gửi lời mời kết bạn!")
        
        except ValueError:
            messagebox.showerror("Lỗi", "ID không hợp lệ!")
    
    def challenge_friend(self):
        """Challenge selected friend to a duel"""
        selected = self.friend_table.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bạn bè!")
            return
        
        # Get selected index
        selected_item = self.friend_table.selection()[0]
        index = self.friend_table.index(selected_item)
        
        if index >= len(self.friends_data):
            messagebox.showwarning("Cảnh báo", "Không thể thách đấu người này!")
            return
        
        friend = self.friends_data[index]
        
        # Check if friend is online and not playing
        if not friend.get_is_online():
            messagebox.showwarning("Cảnh báo", "Bạn bè đang offline!")
            return
        
        if friend.get_is_playing():
            messagebox.showwarning("Cảnh báo", "Bạn bè đang trong trận đấu!")
            return
        
        # Confirm challenge
        if messagebox.askyesno(
            "Xác nhận",
            f"Bạn muốn thách đấu {friend.get_nickname()}?"
        ):
            # Send duel request
            if Client.socket_handle:
                Client.socket_handle.write(create_message(
                    PROTOCOL_DUEL_REQUEST,
                    friend.get_id()
                ))
                messagebox.showinfo("Thông báo", "Đã gửi lời thách đấu! Đang chờ phản hồi...")
    
    def refresh_friends(self):
        """Refresh friend list"""
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_VIEW_FRIEND_LIST))
    
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
