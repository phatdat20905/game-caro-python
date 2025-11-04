"""
Register Form
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from client.controller.client import Client
from shared.utils import create_message, get_asset_path
from shared.constants import *

class RegisterFrm:
    """Register form GUI"""
    
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
        
        self.window.title("Đăng ký - Caro Game")
        self.window.geometry("450x600")  # Optimized from 500x650
        self.window.resizable(False, False)
        self.selected_avatar = "0"
        self.avatar_images = []  # Keep references to prevent garbage collection
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
        # Main frame with scrolling capability
        main_frame = tk.Frame(self.window, bg=COLOR_BACKGROUND)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="ĐĂNG KÝ TÀI KHOẢN",
            font=("Arial", 18, "bold"),
            bg=COLOR_BACKGROUND,
            fg=COLOR_PRIMARY
        )
        title_label.pack(pady=(0, 15))
        
        # Form fields frame
        form_frame = tk.Frame(main_frame, bg=COLOR_BACKGROUND)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        tk.Label(form_frame, text="Tài khoản:", font=FONT_NORMAL, bg=COLOR_BACKGROUND).pack(anchor=tk.W)
        self.username_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=40)
        self.username_entry.pack(pady=(3, 10), ipady=4)
        
        # Password
        tk.Label(form_frame, text="Mật khẩu:", font=FONT_NORMAL, bg=COLOR_BACKGROUND).pack(anchor=tk.W)
        self.password_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=40, show="●")
        self.password_entry.pack(pady=(3, 10), ipady=4)
        
        # Confirm Password
        tk.Label(form_frame, text="Xác nhận mật khẩu:", font=FONT_NORMAL, bg=COLOR_BACKGROUND).pack(anchor=tk.W)
        self.confirm_password_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=40, show="●")
        self.confirm_password_entry.pack(pady=(3, 10), ipady=4)
        
        # Nickname
        tk.Label(form_frame, text="Tên hiển thị:", font=FONT_NORMAL, bg=COLOR_BACKGROUND).pack(anchor=tk.W)
        self.nickname_entry = tk.Entry(form_frame, font=FONT_NORMAL, width=40)
        self.nickname_entry.pack(pady=(3, 10), ipady=4)
        
        # Avatar selection with combobox
        avatar_label = tk.Label(
            form_frame, 
            text="Chọn avatar:", 
            font=FONT_NORMAL, 
            bg=COLOR_BACKGROUND
        )
        avatar_label.pack(anchor=tk.W, pady=(5, 3))
        
        from tkinter import ttk
        avatar_options = [f"Avatar {i}" for i in range(6)]
        self.avatar_combo = ttk.Combobox(
            form_frame,
            values=avatar_options,
            state="readonly",
            font=FONT_NORMAL,
            width=20
        )
        self.avatar_combo.current(0)  # Default to Avatar 0
        self.avatar_combo.pack(anchor=tk.W, pady=(0, 5))
        
        # Avatar preview
        self.avatar_preview_frame = tk.Frame(
            form_frame, 
            bg=COLOR_LIGHT, 
            padx=2, 
            pady=2
        )
        self.avatar_preview_frame.pack(pady=(5, 10))
        
        self.avatar_preview_label = tk.Label(
            self.avatar_preview_frame,
            text="",
            bg=COLOR_BACKGROUND
        )
        self.avatar_preview_label.pack()
        
        # Load and show default avatar
        self.load_avatar_preview(0)
        
        # Bind combobox selection
        self.avatar_combo.bind('<<ComboboxSelected>>', self.on_avatar_change)
        
        # Register button
        register_btn = tk.Button(
            main_frame,
            text="ĐĂNG KÝ",
            font=("Arial", 12, "bold"),
            bg=COLOR_SUCCESS,
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            cursor="hand2",
            command=self.register,
            width=25,
            height=2
        )
        register_btn.pack(pady=(15, 10))
        
        # Login link
        login_frame = tk.Frame(main_frame, bg=COLOR_BACKGROUND)
        login_frame.pack(pady=(5, 0))
        
        tk.Label(
            login_frame,
            text="Đã có tài khoản?",
            font=FONT_NORMAL,
            bg=COLOR_BACKGROUND
        ).pack(side=tk.LEFT)
        
        login_link = tk.Label(
            login_frame,
            text="Đăng nhập ngay",
            font=FONT_NORMAL,
            bg=COLOR_BACKGROUND,
            fg=COLOR_PRIMARY,
            cursor="hand2"
        )
        login_link.pack(side=tk.LEFT, padx=(5, 0))
        login_link.bind('<Button-1>', lambda e: self.back_to_login())
        
        # Underline on hover
        login_link.bind('<Enter>', lambda e: login_link.config(font=("Arial", 10, "underline")))
        login_link.bind('<Leave>', lambda e: login_link.config(font=FONT_NORMAL))
    
    def load_avatar_preview(self, avatar_id):
        """Load and display avatar preview"""
        try:
            avatar_path = get_asset_path('avatar', f'{avatar_id}.jpg')
            if os.path.exists(avatar_path):
                img = Image.open(avatar_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)  # Smaller preview
                photo = ImageTk.PhotoImage(img)
                # Keep reference
                self.avatar_preview_photo = photo
                self.avatar_preview_label.config(image=photo)
            else:
                self.avatar_preview_label.config(
                    text=f"Avatar {avatar_id}",
                    font=("Arial", 10),
                    width=10,
                    height=5
                )
        except:
            self.avatar_preview_label.config(
                text=f"Avatar {avatar_id}",
                font=("Arial", 10),
                width=10,
                height=5
            )
    
    def on_avatar_change(self, event=None):
        """Handle avatar selection change"""
        selected = self.avatar_combo.current()
        self.selected_avatar = str(selected)
        self.load_avatar_preview(selected)
    
    def select_avatar(self, avatar_id):
        """Select avatar (legacy method for compatibility)"""
        self.selected_avatar = str(avatar_id)
    
    def register(self):
        """Handle register button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        nickname = self.nickname_entry.get().strip()
        
        # Validation
        if not username or not password or not nickname:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if len(username) < 3:
            messagebox.showwarning("Cảnh báo", "Tài khoản phải có ít nhất 3 ký tự!")
            return
        
        if len(password) < 3:
            messagebox.showwarning("Cảnh báo", "Mật khẩu phải có ít nhất 3 ký tự!")
            return
        
        if password != confirm_password:
            messagebox.showwarning("Cảnh báo", "Mật khẩu xác nhận không khớp!")
            return
        
        if len(nickname) < 2:
            messagebox.showwarning("Cảnh báo", "Tên hiển thị phải có ít nhất 2 ký tự!")
            return
        
        # Send register request
        if Client.socket_handle:
            Client.socket_handle.write(create_message(
                PROTOCOL_REGISTER,
                username,
                password,
                nickname,
                self.selected_avatar
            ))
    
    def back_to_login(self):
        """Go back to login"""
        self.close()
        Client.open_login()
    
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
