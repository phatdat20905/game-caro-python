"""
Competitor Info Form - Show opponent information in a popup
"""

import tkinter as tk
from client.controller.client import Client
from shared.constants import *

class CompetitorInfoFrm:
    """Form for displaying competitor information"""
    
    def __init__(self, competitor):
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title("Thông tin đối thủ")
        self.window.geometry("350x400")
        self.window.resizable(False, False)
        self.window.grab_set()  # Modal
        
        self.competitor = competitor
        
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
            text="THÔNG TIN ĐỐI THỦ",
            font=("Arial", 16, "bold"),
            bg=COLOR_PRIMARY,
            fg="white"
        ).pack(pady=15)
        
        # Content
        content_frame = tk.Frame(self.window, padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Avatar
        avatar_label = tk.Label(content_frame, text="👤", font=("Arial", 60))
        avatar_label.pack(pady=10)
        
        # User info
        info_items = [
            ("ID:", str(self.competitor.get_id())),
            ("Tên:", self.competitor.get_nickname()),
            ("Tổng số trận:", str(self.competitor.get_number_of_game())),
            ("Thắng:", str(self.competitor.get_number_of_win())),
            ("Hòa:", str(self.competitor.get_number_of_draw())),
            ("Thua:", str(self.competitor.get_number_of_game() - self.competitor.get_number_of_win() - self.competitor.get_number_of_draw())),
        ]
        
        for label, value in info_items:
            item_frame = tk.Frame(content_frame)
            item_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                item_frame,
                text=label,
                font=FONT_NORMAL,
                width=12,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            tk.Label(
                item_frame,
                text=value,
                font=("Arial", 11, "bold"),
                fg=COLOR_PRIMARY
            ).pack(side=tk.LEFT)
        
        # Status
        status_frame = tk.Frame(content_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            status_frame,
            text="Trạng thái:",
            font=FONT_NORMAL,
            width=12,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        if self.competitor.get_is_playing():
            status_text = "🎮 Đang chơi"
            status_color = COLOR_WARNING
        elif self.competitor.get_is_online():
            status_text = "🟢 Online"
            status_color = COLOR_SUCCESS
        else:
            status_text = "⚫ Offline"
            status_color = "gray"
        
        tk.Label(
            status_frame,
            text=status_text,
            font=FONT_NORMAL,
            fg=status_color
        ).pack(side=tk.LEFT)
        
        # Close button
        tk.Button(
            content_frame,
            text="Đóng",
            font=FONT_BUTTON,
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            cursor="hand2",
            command=self.close,
            width=15
        ).pack(pady=20)
    
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
