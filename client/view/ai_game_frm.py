"""
AI Game Form - Play against AI
"""

import tkinter as tk
from tkinter import messagebox
from client.controller.client import Client
from shared.user import User
from shared.constants import *
from shared.game_logic import GameLogic, SimpleAI
from shared.point import Point
import threading
import time

class AIGameFrm:
    """AI game form for single-player practice"""
    
    def __init__(self):
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title("Chơi với AI - Caro Game")
        self.window.geometry("770x580")  # Optimized from 1000x700
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Game state
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.my_turn = True  # Player starts first
        self.game_started = True
        self.game_ended = False
        self.player_marker = 1  # Player is X
        self.ai_marker = 2  # AI is O
        
        # Timer
        self.time_left = TURN_TIME_LIMIT
        self.timer_running = False
        
        # Stats
        self.moves_count = 0
        
        self.setup_ui()
        self.center_window()
        self.start_timer()
    
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
        # Main container with smaller padding
        main_container = tk.Frame(self.window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel (game board)
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, padx=(0, 5))
        
        # Title - smaller
        tk.Label(
            left_panel,
            text="CHƠI VỚI AI",
            font=("Arial", 14, "bold"),
            fg=COLOR_PRIMARY
        ).pack(pady=(0, 5))
        
        # Game board
        self.board_frame = tk.Frame(left_panel, bg="black", padx=2, pady=2)
        self.board_frame.pack()
        
        self.create_board()
        
        # Timer and status - smaller
        status_frame = tk.Frame(left_panel)
        status_frame.pack(pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Lượt của bạn",
            font=("Arial", 9),
            fg=COLOR_SUCCESS
        )
        self.status_label.pack()
        
        self.timer_label = tk.Label(
            status_frame,
            text=f"⏱ {self.time_left}s",
            font=("Arial", 12, "bold"),
            fg=COLOR_DANGER
        )
        self.timer_label.pack(pady=3)
        
        # Control buttons
        # Control buttons - smaller
        button_frame = tk.Frame(left_panel)
        button_frame.pack(pady=5)
        
        tk.Button(
            button_frame,
            text="Chơi lại",
            font=("Arial", 9),
            bg=COLOR_SUCCESS,
            fg="white",
            cursor="hand2",
            command=self.restart_game,
            width=10
        ).pack(side=tk.LEFT, padx=3)
        
        tk.Button(
            button_frame,
            text="Thoát",
            font=("Arial", 9),
            bg=COLOR_DANGER,
            fg="white",
            cursor="hand2",
            command=self.on_closing,
            width=10
        ).pack(side=tk.LEFT, padx=3)
        
        # Right panel (info) - smaller
        right_panel = tk.Frame(main_container, width=260)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        # Player info
        self.create_player_info(right_panel)
        
        # Game info
        self.create_game_info(right_panel)
    
    def create_board(self):
        """Create game board with buttons"""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 8, "bold"),  # Smaller font
                    width=2,
                    height=1,
                    bg="white",
                    borderwidth=1,
                    command=lambda x=i, y=j: self.make_move(x, y)
                )
                btn.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
                self.buttons[i][j] = btn
    
    def create_player_info(self, parent):
        """Create player information panel"""
        info_frame = tk.LabelFrame(
            parent,
            text="Thông tin người chơi",
            font=("Arial", 9, "bold"),  # Smaller
            bg=COLOR_LIGHT,
            padx=8,
            pady=8
        )
        info_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Player (You)
        tk.Label(
            info_frame,
            text="Bạn (X)",
            font=("Arial", 10, "bold"),  # Smaller
            bg=COLOR_LIGHT
        ).pack(anchor=tk.W)
        
        player_name = Client.user.get_nickname() if Client.user else "Player"
        tk.Label(
            info_frame,
            text=player_name,
            font=("Arial", 9),  # Smaller
            bg=COLOR_LIGHT,
            fg=COLOR_PRIMARY
        ).pack(anchor=tk.W, pady=(0, 8))
        
        # AI - smaller
        tk.Label(
            info_frame,
            text="AI (O)",
            font=("Arial", 10, "bold"),
            bg=COLOR_LIGHT
        ).pack(anchor=tk.W)
        
        tk.Label(
            info_frame,
            text="Máy tính",
            font=("Arial", 9),
            bg=COLOR_LIGHT,
            fg=COLOR_DANGER
        ).pack(anchor=tk.W)
    
    def create_game_info(self, parent):
        """Create game info panel"""
        info_frame = tk.LabelFrame(
            parent,
            text="Thông tin trò chơi",
            font=("Arial", 9, "bold"),
            bg=COLOR_LIGHT,
            padx=8,
            pady=8
        )
        info_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.moves_label = tk.Label(
            info_frame,
            text="Số nước đã đi: 0",
            font=("Arial", 9),
            bg=COLOR_LIGHT
        )
        self.moves_label.pack(anchor=tk.W, pady=3)
        
        # Instructions - smaller
        instructions = tk.LabelFrame(
            parent,
            text="Hướng dẫn",
            font=("Arial", 9, "bold"),
            bg=COLOR_LIGHT,
            padx=8,
            pady=8
        )
        instructions.pack(fill=tk.BOTH, expand=True)
        
        guide_text = """• Click vào ô trống để đánh

• Tạo 5 quân X liên tiếp

• Mỗi nước có 30 giây

• AI tự động đánh sau bạn"""
        
        tk.Label(
            instructions,
            text=guide_text,
            font=("Arial", 8),
            bg=COLOR_LIGHT,
            justify=tk.LEFT
        ).pack()
    
    def make_move(self, x, y):
        """Handle player move"""
        if self.game_ended:
            return
        
        if not self.my_turn:
            messagebox.showwarning("Cảnh báo", "Chưa đến lượt của bạn!")
            return
        
        if self.board[x][y] != 0:
            messagebox.showwarning("Cảnh báo", "Ô này đã được đánh!")
            return
        
        # Make move
        self.board[x][y] = self.player_marker
        self.buttons[x][y].config(
            text="X",
            fg=COLOR_PRIMARY,
            bg=COLOR_LIGHT,
            state=tk.DISABLED
        )
        self.moves_count += 1
        self.moves_label.config(text=f"Số nước đã đi: {self.moves_count}")
        
        # Check win
        if GameLogic.check_win(self.board, x, y, self.player_marker):
            self.handle_win(True)
            return
        
        # Check draw
        if GameLogic.is_board_full(self.board):
            self.handle_draw()
            return
        
        # Switch turn to AI
        self.my_turn = False
        self.status_label.config(text="Lượt của AI", fg=COLOR_DANGER)
        self.stop_timer()
        
        # AI makes move after delay
        threading.Thread(target=self.ai_move, daemon=True).start()
    
    def ai_move(self):
        """AI makes a move"""
        time.sleep(0.5)  # Small delay for better UX
        
        # Get best move from AI
        move = SimpleAI.get_best_move(self.board, self.ai_marker, self.player_marker)
        
        if move:
            x, y = move.x, move.y
            
            # Make move on main thread
            self.window.after(0, lambda: self.apply_ai_move(x, y))
    
    def apply_ai_move(self, x, y):
        """Apply AI move to board (called on main thread)"""
        if self.game_ended:
            return
        
        self.board[x][y] = self.ai_marker
        self.buttons[x][y].config(
            text="O",
            fg=COLOR_DANGER,
            bg=COLOR_LIGHT,
            state=tk.DISABLED
        )
        self.moves_count += 1
        self.moves_label.config(text=f"Số nước đã đi: {self.moves_count}")
        
        # Check win
        if GameLogic.check_win(self.board, x, y, self.ai_marker):
            self.handle_win(False)
            return
        
        # Check draw
        if GameLogic.is_board_full(self.board):
            self.handle_draw()
            return
        
        # Switch turn back to player
        self.my_turn = True
        self.status_label.config(text="Lượt của bạn", fg=COLOR_SUCCESS)
        self.start_timer()
    
    def handle_win(self, player_won):
        """Handle game win"""
        self.game_ended = True
        self.stop_timer()
        
        if player_won:
            self.status_label.config(text="🎉 Bạn thắng!", fg=COLOR_SUCCESS)
            messagebox.showinfo("Chiến thắng!", "Chúc mừng! Bạn đã thắng AI!")
        else:
            self.status_label.config(text="😢 AI thắng!", fg=COLOR_DANGER)
            messagebox.showinfo("Thua cuộc", "AI đã thắng! Cố gắng lần sau nhé!")
    
    def handle_draw(self):
        """Handle draw game"""
        self.game_ended = True
        self.stop_timer()
        self.status_label.config(text="Hòa!", fg=COLOR_WARNING)
        messagebox.showinfo("Hòa", "Trò chơi hòa!")
    
    def start_timer(self):
        """Start turn timer"""
        self.time_left = TURN_TIME_LIMIT
        self.timer_running = True
        self.update_timer()
    
    def stop_timer(self):
        """Stop turn timer"""
        self.timer_running = False
    
    def update_timer(self):
        """Update timer display"""
        if not self.timer_running:
            return
        
        self.timer_label.config(text=f"⏱ {self.time_left}s")
        
        if self.time_left <= 0:
            self.handle_timeout()
            return
        
        self.time_left -= 1
        self.window.after(1000, self.update_timer)
    
    def handle_timeout(self):
        """Handle timer timeout"""
        self.stop_timer()
        if not self.game_ended:
            messagebox.showwarning("Hết giờ", "Bạn đã hết thời gian!")
            self.handle_win(False)
    
    def restart_game(self):
        """Restart game"""
        if not self.game_ended:
            if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn chơi lại? Trò chơi hiện tại sẽ bị hủy."):
                return
        
        # Reset game state
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.my_turn = True
        self.game_started = True
        self.game_ended = False
        self.moves_count = 0
        
        # Reset UI
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].config(
                    text="",
                    bg="white",
                    state=tk.NORMAL
                )
        
        self.status_label.config(text="Lượt của bạn", fg=COLOR_SUCCESS)
        self.moves_label.config(text="Số nước đã đi: 0")
        self.start_timer()
    
    def on_closing(self):
        """Handle window close"""
        if not self.game_ended:
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
                self.stop_timer()
                self.window.destroy()
        else:
            self.stop_timer()
            self.window.destroy()
