"""
Login Form
"""

import tkinter as tk
from tkinter import messagebox
from client.controller.client import Client
from shared.utils import create_message
from shared.constants import *

class LoginFrm:
    """Login form GUI"""
    
    def __init__(self):
        # Use Client.root if available, otherwise create new Tk
        if hasattr(Client, 'root') and Client.root:
            # Hide root and use Toplevel
            Client.root.withdraw()
            self.window = tk.Toplevel(Client.root)
        else:
            # Fallback: create new Tk (shouldn't happen in normal flow)
            self.window = tk.Tk()
            # DON'T reassign Client.root - let run_client.py handle it
        
        self.window.title("Đăng nhập - Caro Game")
        self.window.geometry("400x420")
        self.window.resizable(False, False)
        
        # CRITICAL FIX: Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()
        
        # Center window
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
            text="CARO GAME",
            font=("Arial", 24, "bold"),
            bg=COLOR_BACKGROUND,
            fg=COLOR_PRIMARY
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Đăng nhập để bắt đầu",
            font=FONT_NORMAL,
            bg=COLOR_BACKGROUND,
            fg=COLOR_DARK
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username
        username_label = tk.Label(
            main_frame,
            text="Tài khoản:",
            font=FONT_NORMAL,
            bg=COLOR_BACKGROUND
        )
        username_label.pack(anchor=tk.W)
        
        self.username_entry = tk.Entry(
            main_frame,
            font=FONT_NORMAL,
            width=30
        )
        self.username_entry.pack(pady=(5, 15), ipady=5)
        
        # Password
        password_label = tk.Label(
            main_frame,
            text="Mật khẩu:",
            font=FONT_NORMAL,
            bg=COLOR_BACKGROUND
        )
        password_label.pack(anchor=tk.W)
        
        self.password_entry = tk.Entry(
            main_frame,
            font=FONT_NORMAL,
            width=30,
            show="●"
        )
        self.password_entry.pack(pady=(5, 25), ipady=5)
        
        # Login button
        login_btn = tk.Button(
            main_frame,
            text="ĐĂNG NHẬP",
            font=FONT_BUTTON,
            bg=COLOR_PRIMARY,
            fg="white",
            activebackground=COLOR_INFO,
            activeforeground="white",
            cursor="hand2",
            command=self.login,
            width=25,
            height=2
        )
        login_btn.pack(pady=(0, 15))
        
        # Register link
        register_frame = tk.Frame(main_frame, bg=COLOR_BACKGROUND)
        register_frame.pack()
        
        tk.Label(
            register_frame,
            text="Chưa có tài khoản?",
            font=FONT_NORMAL,
            bg=COLOR_BACKGROUND
        ).pack(side=tk.LEFT)
        
        register_link = tk.Label(
            register_frame,
            text="Đăng ký ngay",
            font=FONT_NORMAL,
            bg=COLOR_BACKGROUND,
            fg=COLOR_PRIMARY,
            cursor="hand2"
        )
        register_link.pack(side=tk.LEFT, padx=(5, 0))
        register_link.bind('<Button-1>', lambda e: self.open_register())
        
        # Underline on hover
        register_link.bind('<Enter>', lambda e: register_link.config(font=("Arial", 10, "underline")))
        register_link.bind('<Leave>', lambda e: register_link.config(font=FONT_NORMAL))
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus on username
        self.username_entry.focus()
    
    def login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Send login request to server
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_CLIENT_VERIFY, username, password))
    
    def open_register(self):
        """Open register form"""
        self.close()
        Client.open_register()
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Lỗi đăng nhập", message)
    
    def on_closing(self):
        """Handle window close (X button) - CRITICAL FIX"""
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn thoát ứng dụng?"):
            # Close socket first
            try:
                if Client.socket_handle:
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
