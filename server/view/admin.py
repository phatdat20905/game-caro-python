"""
Admin panel GUI for server management
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from shared.utils import get_timestamp
from server.dao.user_dao import UserDAO

class Admin:
    """Admin GUI for server management"""
    
    def __init__(self, root, server):
        """
        Initialize admin panel
        
        Args:
            root: Tkinter root window
            server: Server instance
        """
        self.root = root
        self.server = server
        self.user_dao = UserDAO()
        
        self.root.title("Caro Game - Admin Panel")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="CARO GAME SERVER - ADMIN PANEL",
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main content
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Server info
        info_frame = tk.LabelFrame(main_frame, text="Server Information", font=("Arial", 10, "bold"), padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(info_frame, text="Status: Running", font=("Arial", 10))
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.connections_label = tk.Label(info_frame, text="Active Connections: 0", font=("Arial", 10))
        self.connections_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.address_label = tk.Label(
            info_frame,
            text=f"Address: {self.server.host}:{self.server.port}",
            font=("Arial", 10)
        )
        self.address_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Logs tab
        logs_frame = tk.Frame(notebook)
        notebook.add(logs_frame, text="Server Logs")
        
        self.log_text = scrolledtext.ScrolledText(
            logs_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#263238",
            fg="#00FF00"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Broadcast tab
        broadcast_frame = tk.Frame(notebook)
        notebook.add(broadcast_frame, text="Broadcast Message")
        
        # Instructions
        tk.Label(
            broadcast_frame,
            text="Gửi tin nhắn tới tất cả người chơi đang online:",
            font=("Arial", 10, "bold"),
            fg="#2196F3"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Message input
        message_frame = tk.Frame(broadcast_frame, padx=10, pady=5)
        message_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            message_frame,
            text="Nội dung tin nhắn:",
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.broadcast_text = scrolledtext.ScrolledText(
            message_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            height=8
        )
        self.broadcast_text.pack(fill=tk.BOTH, expand=True)
        
        # Broadcast buttons
        btn_broadcast_frame = tk.Frame(broadcast_frame, padx=10, pady=10)
        btn_broadcast_frame.pack(fill=tk.X)
        
        tk.Button(
            btn_broadcast_frame,
            text="📢 GỬI TIN NHẮN",
            command=self.send_broadcast,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_broadcast_frame,
            text="Xóa nội dung",
            command=lambda: self.broadcast_text.delete(1.0, tk.END),
            bg="#FF9800",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        # Broadcast history
        tk.Label(
            broadcast_frame,
            text="Lịch sử broadcast:",
            font=("Arial", 9)
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.broadcast_history = scrolledtext.ScrolledText(
            broadcast_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            height=8,
            bg="#F5F5F5",
            state=tk.DISABLED
        )
        self.broadcast_history.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Users tab
        users_frame = tk.Frame(notebook)
        notebook.add(users_frame, text="User Management")
        
        # User list
        self.user_tree = ttk.Treeview(
            users_frame,
            columns=("ID", "Username", "Nickname", "Online", "Playing"),
            show="headings",
            height=15
        )
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Nickname", text="Nickname")
        self.user_tree.heading("Online", text="Online")
        self.user_tree.heading("Playing", text="Playing")
        
        self.user_tree.column("ID", width=50)
        self.user_tree.column("Username", width=150)
        self.user_tree.column("Nickname", width=150)
        self.user_tree.column("Online", width=80)
        self.user_tree.column("Playing", width=80)
        
        self.user_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # User management buttons
        user_btn_frame = tk.Frame(users_frame)
        user_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(
            user_btn_frame,
            text="Refresh Users",
            command=self.refresh_users,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            user_btn_frame,
            text="Reset All to Offline",
            command=self.reset_all_users,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            user_btn_frame,
            text="Ban User",
            command=self.ban_user,
            bg="#F44336",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            user_btn_frame,
            text="Unban User",
            command=self.unban_user,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=2)
        
        # Control buttons
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            btn_frame,
            text="Clear Logs",
            command=self.clear_logs,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Disconnect All Clients",
            command=self.disconnect_all_clients,
            bg="#FF5722",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Stop Server",
            command=self.stop_server,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(side=tk.RIGHT, padx=5)
        
        # Auto-update connection count
        self.update_connection_count()
        
        # Initial user load
        self.refresh_users()
    
    def add_message(self, message):
        """Add message to log"""
        timestamp = get_timestamp()
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    def clear_logs(self):
        """Clear log text"""
        self.log_text.delete(1.0, tk.END)
        self.add_message("Logs cleared")
    
    def send_broadcast(self):
        """Send broadcast message to all online users"""
        from shared.constants import PROTOCOL_ADMIN_BROADCAST
        from shared.utils import create_message, get_timestamp
        
        message = self.broadcast_text.get(1.0, tk.END).strip()
        
        if not message:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung tin nhắn!")
            return
        
        # Send to all connected clients
        count = 0
        if hasattr(self.server, 'server_thread_bus'):
            for thread in self.server.server_thread_bus.get_list_server_threads():
                try:
                    thread.write(create_message(PROTOCOL_ADMIN_BROADCAST, message))
                    count += 1
                except:
                    pass
        
        # Add to history
        timestamp = get_timestamp()
        history_entry = f"[{timestamp}] Sent to {count} users: {message}\n"
        
        self.broadcast_history.config(state=tk.NORMAL)
        self.broadcast_history.insert(1.0, history_entry)
        self.broadcast_history.config(state=tk.DISABLED)
        
        # Clear input
        self.broadcast_text.delete(1.0, tk.END)
        
        # Log
        self.add_message(f"Broadcast sent to {count} users: {message}")
        
        messagebox.showinfo("Thành công", f"Đã gửi tin nhắn tới {count} người chơi!")
    
    def update_connection_count(self):
        """Update connection count display"""
        if hasattr(self.server, 'get_active_connections'):
            count = self.server.get_active_connections()
            self.connections_label.config(text=f"Active Connections: {count}")
        
        # Schedule next update
        self.root.after(2000, self.update_connection_count)
    
    def refresh_users(self):
        """Refresh user list"""
        # Clear current items
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # Get all users
        users = self.user_dao.get_all_users()
        
        for user in users:
            self.user_tree.insert(
                "",
                tk.END,
                values=(
                    user.get_id(),
                    user.get_username(),
                    user.get_nickname(),
                    "Yes" if user.get_is_online() else "No",
                    "Yes" if user.get_is_playing() else "No"
                )
            )
    
    def reset_all_users(self):
        """Reset all users to offline and not playing"""
        if messagebox.askyesno("Xác nhận", "Reset tất cả người dùng về trạng thái offline?\n\nĐiều này sẽ đặt lại tất cả người dùng về offline và không chơi."):
            try:
                self.user_dao.reset_all_users_status()
                self.add_message("All users reset to offline status")
                self.refresh_users()
                messagebox.showinfo("Thành công", "Đã reset tất cả người dùng về offline!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể reset users: {e}")
                self.add_message(f"Error resetting users: {e}")
    
    def disconnect_all_clients(self):
        """Disconnect all connected clients"""
        if messagebox.askyesno("Xác nhận", "Ngắt kết nối tất cả client đang kết nối?\n\nTất cả người chơi sẽ bị ngắt kết nối khỏi server."):
            count = 0
            if hasattr(self.server, 'server_thread_bus'):
                threads = list(self.server.server_thread_bus.get_list_server_threads())
                for thread in threads:
                    try:
                        thread.cleanup()
                        count += 1
                    except Exception as e:
                        self.add_message(f"Error disconnecting client: {e}")
                
                # Clear thread bus
                self.server.server_thread_bus.get_list_server_threads().clear()
            
            self.add_message(f"Disconnected {count} clients")
            self.refresh_users()
            messagebox.showinfo("Thành công", f"Đã ngắt kết nối {count} client!")
    
    def ban_user(self):
        """Ban selected user"""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to ban")
            return
        
        item = self.user_tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        if messagebox.askyesno("Confirm Ban", f"Ban user '{username}' (ID: {user_id})?"):
            self.user_dao.update_banned_status(user_id, True, "Banned by admin")
            self.add_message(f"User {username} (ID: {user_id}) has been banned")
            self.refresh_users()
            messagebox.showinfo("Success", f"User '{username}' has been banned")
    
    def unban_user(self):
        """Unban selected user"""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to unban")
            return
        
        item = self.user_tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        if messagebox.askyesno("Confirm Unban", f"Unban user '{username}' (ID: {user_id})?"):
            self.user_dao.update_banned_status(user_id, False)
            self.add_message(f"User {username} (ID: {user_id}) has been unbanned")
            self.refresh_users()
            messagebox.showinfo("Success", f"User '{username}' has been unbanned")
    
    def stop_server(self):
        """Stop server"""
        if messagebox.askyesno("Confirm", "Are you sure you want to stop the server?"):
            self.add_message("Stopping server...")
            if hasattr(self.server, 'stop'):
                self.server.stop()
            self.root.quit()
    
    def run(self):
        """Run admin GUI"""
        self.root.mainloop()


if __name__ == "__main__":
    # For testing admin panel standalone
    root = tk.Tk()
    admin = Admin(root, None)
    admin.run()
