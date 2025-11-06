"""
Rank Form - Complete implementation with sorting
"""

import tkinter as tk
from tkinter import ttk
from client.controller.client import Client
from shared.utils import create_message, calculate_win_ratio
from shared.constants import *

class RankFrm:
    """Rank form with sortable table"""
    
    def __init__(self):
        # Use Client.root as master to avoid "main thread not in main loop" error
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title("Bảng xếp hạng")
        self.window.geometry("800x550")
        self.window.resizable(False, False)
        
        self.ranks_data = []  # Store rank data
        self.sort_column = None
        self.sort_reverse = False
        
        self.setup_ui()
        self.center_window()
        
        # Request rank list from server
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_GET_RANK_CHARTS))
    
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
            text="🏆 BẢNG XẾP HẠNG 🏆",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARY,
            fg="white"
        ).pack(pady=15)
        
        # Main content
        content_frame = tk.Frame(self.window, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info label
        tk.Label(
            content_frame,
            text="Nhấn vào tiêu đề cột để sắp xếp",
            font=FONT_NORMAL,
            fg="gray"
        ).pack(pady=(0, 10))
        
        # Table frame
        table_frame = tk.Frame(content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.rank_table = ttk.Treeview(
            table_frame,
            columns=("Rank", "ID", "Nickname", "Games", "Wins", "Draws", "Losses", "Ratio"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=14
        )
        
        # Configure columns
        columns = [
            ("Rank", "Hạng", 60),
            ("ID", "ID", 60),
            ("Nickname", "Tên người chơi", 180),
            ("Games", "Số trận", 80),
            ("Wins", "Thắng", 70),
            ("Draws", "Hòa", 70),
            ("Losses", "Thua", 70),
            ("Ratio", "Tỷ lệ", 80),
        ]
        
        for col_id, col_text, col_width in columns:
            self.rank_table.heading(
                col_id,
                text=col_text,
                command=lambda c=col_id: self.sort_by_column(c)
            )
            self.rank_table.column(col_id, width=col_width, anchor=tk.CENTER)
        
        self.rank_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.rank_table.yview)
        
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
            command=self.refresh_ranks,
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
        
        # Legend
        legend_frame = tk.Frame(content_frame)
        legend_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(legend_frame, text="🥇 Top 1", font=FONT_SMALL, fg="gold").pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🥈 Top 2", font=FONT_SMALL, fg="silver").pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🥉 Top 3", font=FONT_SMALL, fg="#CD7F32").pack(side=tk.LEFT, padx=10)
    
    def update_rank_list(self, users):
        """
        Update rank list display
        
        Args:
            users: List of User objects sorted by rank
        """
        # Clear current items
        for item in self.rank_table.get_children():
            self.rank_table.delete(item)
        
        # Store data
        self.ranks_data = []
        
        # Add users to table
        if not users or len(users) == 0:
            self.rank_table.insert(
                "",
                tk.END,
                values=("-", "-", "Chưa có dữ liệu", "-", "-", "-", "-", "-")
            )
        else:
            for rank, user in enumerate(users, start=1):
                # Calculate stats
                num_game = user.get_number_of_game()
                num_win = user.get_number_of_win()
                num_draw = user.get_number_of_draw()
                num_loss = num_game - num_win - num_draw
                win_ratio = calculate_win_ratio(num_win, num_game)
                
                # Determine medal/rank display
                if rank == 1:
                    rank_display = "🥇"
                    tag = "gold"
                elif rank == 2:
                    rank_display = "🥈"
                    tag = "silver"
                elif rank == 3:
                    rank_display = "🥉"
                    tag = "bronze"
                else:
                    rank_display = str(rank)
                    tag = "normal"
                
                # Store data for sorting
                self.ranks_data.append({
                    "rank": rank,
                    "id": user.get_id(),
                    "nickname": user.get_nickname(),
                    "games": num_game,
                    "wins": num_win,
                    "draws": num_draw,
                    "losses": num_loss,
                    "ratio": win_ratio
                })
                
                # Insert into table
                self.rank_table.insert(
                    "",
                    tk.END,
                    values=(
                        rank_display,
                        user.get_id(),
                        user.get_nickname(),
                        num_game,
                        num_win,
                        num_draw,
                        num_loss,
                        f"{win_ratio}%"
                    ),
                    tags=(tag,)
                )
        
        # Configure tags for colors
        self.rank_table.tag_configure("gold", background="#FFD700", foreground="black")
        self.rank_table.tag_configure("silver", background="#C0C0C0", foreground="black")
        self.rank_table.tag_configure("bronze", background="#CD7F32", foreground="white")
        self.rank_table.tag_configure("normal", background="white")
    
    def sort_by_column(self, column):
        """
        Sort table by column
        
        Args:
            column: Column ID to sort by
        """
        # Toggle sort direction if same column
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        # Map column to data key
        column_map = {
            "Rank": "rank",
            "ID": "id",
            "Nickname": "nickname",
            "Games": "games",
            "Wins": "wins",
            "Draws": "draws",
            "Losses": "losses",
            "Ratio": "ratio"
        }
        
        sort_key = column_map.get(column)
        if not sort_key or not self.ranks_data:
            return
        
        # Sort data
        sorted_data = sorted(
            self.ranks_data,
            key=lambda x: x[sort_key],
            reverse=self.sort_reverse
        )
        
        # Clear table
        for item in self.rank_table.get_children():
            self.rank_table.delete(item)
        
        # Re-insert sorted data
        for data in sorted_data:
            # Determine rank display
            rank = data["rank"]
            if rank == 1:
                rank_display = "🥇"
                tag = "gold"
            elif rank == 2:
                rank_display = "🥈"
                tag = "silver"
            elif rank == 3:
                rank_display = "🥉"
                tag = "bronze"
            else:
                rank_display = str(rank)
                tag = "normal"
            
            self.rank_table.insert(
                "",
                tk.END,
                values=(
                    rank_display,
                    data["id"],
                    data["nickname"],
                    data["games"],
                    data["wins"],
                    data["draws"],
                    data["losses"],
                    f"{data['ratio']}%"
                ),
                tags=(tag,)
            )
        
        # Reapply tag colors
        self.rank_table.tag_configure("gold", background="#FFD700", foreground="black")
        self.rank_table.tag_configure("silver", background="#C0C0C0", foreground="black")
        self.rank_table.tag_configure("bronze", background="#CD7F32", foreground="white")
        self.rank_table.tag_configure("normal", background="white")
    
    def refresh_ranks(self):
        """Refresh rank list"""
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_GET_RANK_CHARTS))
    
    def back(self):
        """Go back to homepage"""
        self.close()
        Client.open_homepage()
    
    def show(self):
        """Show window"""
        self.window.deiconify()
    
    def close(self):
        """Close window - Java pattern: ONLY dispose, caller decides what to open next"""
        try:
            self.window.destroy()
        except:
            pass
