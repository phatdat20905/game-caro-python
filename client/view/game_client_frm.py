"""
Game Client Form - Complete game implementation
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from client.controller.client import Client
from shared.utils import create_message, log
from shared.constants import *
from shared.game_logic import GameLogic, SimpleAI
from shared.point import Point
import time
import threading

class GameClientFrm:
    """Main game client form with board, timer, and chat"""
    
    def __init__(self, competitor, room_id, is_start=False, competitor_ip=""):
        master = Client.root if hasattr(Client, 'root') and Client.root else None
        self.window = tk.Toplevel(master)
        self.window.title(f"Game Caro - Phòng {room_id}")
        # Optimized size: board 450px + panels 300px + margins = 770x580
        self.window.geometry("770x580")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Game state
        self.competitor = competitor
        self.room_id = room_id
        self.is_start = is_start  # 0 or 1 from server
        self.competitor_ip = competitor_ip
        
        # CRITICAL: numberOfMatch determines who uses X or O
        # Java logic: numberOfMatch % 2 == 0 → current player uses X
        #            numberOfMatch % 2 == 1 → current player uses O
        self.number_of_match = is_start  # Initialize from server
        
        # Determine my turn and symbols based on numberOfMatch
        # If numberOfMatch is even (0, 2, 4...) → I go first, I use X
        # If numberOfMatch is odd (1, 3, 5...) → Opponent goes first, I use O
        self.my_turn = (self.number_of_match % 2 == 0)
        
        self.game_started = True
        self.game_ended = False
        
        # Board state
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Timer - CRITICAL FIX: Track timer_id to prevent double-running
        self.time_left = TURN_TIME_LIMIT
        self.timer_running = False
        self.timer_id = None  # NEW: Track after() callback ID
        
        # AI mode
        self.is_ai_mode = (competitor.get_nickname() == "AI")
        
        self.setup_ui()
        self.center_window()
        
        # DON'T start timer in __init__ - wait for show() or explicit call
        # This prevents double-start issue
    
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
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Reduced from 10
        
        # Left panel (game board) with smaller spacing
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, padx=(0, 5))  # Reduced from 10
        
        # Title - smaller font
        tk.Label(
            left_panel,
            text=f"PHÒNG {self.room_id}",
            font=("Arial", 14, "bold"),  # Reduced from 16
            fg=COLOR_PRIMARY
        ).pack(pady=(0, 5))  # Reduced padding
        
        # Game board
        self.board_frame = tk.Frame(left_panel, bg="black", padx=2, pady=2)
        self.board_frame.pack()
        
        self.create_board()
        
        # Timer and status
        status_frame = tk.Frame(left_panel)
        status_frame.pack(pady=5)  # Reduced from 10
        
        self.status_label = tk.Label(
            status_frame,
            text="Đang chờ đối thủ...",
            font=("Arial", 9),  # Smaller font
            fg=COLOR_INFO
        )
        self.status_label.pack()
        
        self.timer_label = tk.Label(
            status_frame,
            text=f"⏱ {self.time_left}s",
            font=("Arial", 12, "bold"),  # Reduced from 14
            fg=COLOR_DANGER
        )
        self.timer_label.pack(pady=3)  # Reduced from 5
        
        # Control buttons - smaller size
        control_frame = tk.Frame(left_panel)
        control_frame.pack(pady=5)  # Reduced from 10
        
        self.draw_button = tk.Button(
            control_frame,
            text="Yêu cầu hòa",
            font=("Arial", 9),  # Smaller font
            bg=COLOR_WARNING,
            fg="white",
            cursor="hand2",
            command=self.request_draw,
            state=tk.DISABLED,
            width=10  # Reduced from 12
        )
        self.draw_button.pack(side=tk.LEFT, padx=3)  # Reduced padding
        
        tk.Button(
            control_frame,
            text="Rời phòng",
            font=("Arial", 9),  # Smaller font
            bg=COLOR_DANGER,
            fg="white",
            cursor="hand2",
            command=self.leave_room,
            width=10  # Reduced from 12
        ).pack(side=tk.LEFT, padx=3)  # Reduced padding
        
        # Right panel (competitor info and chat)
        # Reduced width from 300 to 260 for better balance
        right_panel = tk.Frame(main_container, width=260)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_panel.pack_propagate(False)
        
        # Competitor info - more compact
        info_frame = tk.LabelFrame(right_panel, text="Đối thủ", font=("Arial", 9, "bold"), padx=8, pady=8)
        info_frame.pack(fill=tk.X, pady=(0, 8))  # Reduced padding
        
        # Avatar placeholder - smaller size
        avatar_label = tk.Label(info_frame, text="👤", font=("Arial", 32))
        avatar_label.pack()
        
        tk.Label(
            info_frame,
            text=self.competitor.get_nickname(),
            font=("Arial", 12, "bold")  # Smaller
        ).pack()
        
        stats_text = f"Thắng: {self.competitor.get_number_of_win()} | " \
                    f"Hòa: {self.competitor.get_number_of_draw()} | " \
                    f"Thua: {self.competitor.get_number_of_game() - self.competitor.get_number_of_win() - self.competitor.get_number_of_draw()}"
        
        tk.Label(
            info_frame,
            text=stats_text,
            font=("Arial", 8),  # Smaller
            fg="gray"
        ).pack()
        
        # Chat box - more compact
        chat_frame = tk.LabelFrame(right_panel, text="Chat", font=("Arial", 9, "bold"), padx=8, pady=8)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chat display - smaller height
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=28,  # Reduced from 30
            height=12,  # Reduced from 15
            font=FONT_SMALL,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chat input - smaller components
        chat_input_frame = tk.Frame(chat_frame)
        chat_input_frame.pack(fill=tk.X)
        
        self.chat_entry = tk.Entry(chat_input_frame, font=("Arial", 9))
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        self.chat_entry.bind('<Return>', lambda e: self.send_chat())
        
        tk.Button(
            chat_input_frame,
            text="Gửi",
            font=("Arial", 9),
            bg=COLOR_PRIMARY,
            fg="white",
            cursor="hand2",
            command=self.send_chat,
            width=6  # Reduced from 8
        ).pack(side=tk.RIGHT)
    
    def create_board(self):
        """Create 15x15 game board with optimal size"""
        # Button size: 28x28 pixels (smaller than before for better fit)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                button = tk.Button(
                    self.board_frame,
                    text="",
                    width=2,  # Reduced from 3
                    height=1,
                    font=("Arial", 8, "bold"),  # Smaller font
                    bg="white",
                    relief=tk.RAISED,
                    borderwidth=1,
                    command=lambda r=row, c=col: self.on_cell_click(r, c)
                )
                button.grid(row=row, column=col, padx=0, pady=0, sticky="nsew")
                self.buttons[row][col] = button
    
    def on_cell_click(self, row, col):
        """Handle cell click"""
        # Check if game has started
        if not self.game_started:
            messagebox.showwarning("Cảnh báo", "Trò chơi chưa bắt đầu!")
            return
        
        # Check if game has ended
        if self.game_ended:
            return
        
        # Check if it's player's turn
        if not self.my_turn:
            messagebox.showwarning("Cảnh báo", "Chưa đến lượt của bạn!")
            return
        
        # Check if cell is empty
        if self.board[row][col] != 0:
            messagebox.showwarning("Cảnh báo", "Ô này đã được đánh!")
            return
        
        # Make move
        self.make_move(row, col, 1)  # 1 = my piece
        
        # Disable all buttons while waiting for opponent
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:  # Only disable empty cells
                    self.buttons[i][j].config(state=tk.DISABLED)
        
        # Stop my timer
        self.stop_timer()
        
        # Update status
        self.update_status("Lượt đối thủ...")
        self.my_turn = False
        
        # Send move to server (if not AI mode)
        if not self.is_ai_mode and Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_CARO, row, col))
        
        # Check win
        if GameLogic.check_win(self.board, row, col, 1):
            self.on_game_win()
            return
        
        # Check draw
        if GameLogic.is_board_full(self.board):
            self.on_game_draw()
            return
        
        # AI's turn (if AI mode)
        if self.is_ai_mode:
            self.window.after(500, self.ai_make_move)
            return
        
        # Switch turn
        self.my_turn = False
        self.stop_timer()
        self.update_status("Lượt đối thủ...")
        
        # Disable draw button when it's not my turn (Java logic)
        self.draw_button.config(state=tk.DISABLED)
        
        # AI's turn
        if self.is_ai_mode:
            self.window.after(500, self.ai_make_move)
    
    def make_move(self, row, col, player):
        """
        Make a move on the board
        
        Args:
            row, col: Position
            player: 1 for me, 2 for opponent
        """
        self.board[row][col] = player
        
        # Determine symbol based on numberOfMatch and player
        # Java logic:
        # - Current player uses: numberOfMatch % 2 == 0 ? "X" : "O"
        # - Opponent uses: not(numberOfMatch % 2) == 0 ? "X" : "O"
        
        if player == 1:  # My move
            # If numberOfMatch is even, I use X; if odd, I use O
            symbol = "X" if (self.number_of_match % 2 == 0) else "O"
            color = COLOR_PRIMARY if symbol == "X" else COLOR_DANGER
        else:  # Opponent's move
            # Opponent uses opposite symbol
            symbol = "O" if (self.number_of_match % 2 == 0) else "X"
            color = COLOR_DANGER if symbol == "O" else COLOR_PRIMARY
        
        # Update button - keep size fixed
        button = self.buttons[row][col]
        button.config(
            text=symbol,
            fg=color,
            font=("Arial", 8, "bold"),  # Keep same small font as board creation
            state=tk.DISABLED,
            relief=tk.FLAT,  # Flat instead of SUNKEN to keep size
            disabledforeground=color  # Show color even when disabled
        )
    
    def ai_make_move(self):
        """AI makes a move"""
        if self.game_ended:
            return
        
        # Get AI's best move
        move = SimpleAI.get_best_move(self.board, 2, 1)
        
        if move:
            row, col = move.get_x(), move.get_y()
            self.make_move(row, col, 2)
            
            # Check win
            if GameLogic.check_win(self.board, row, col, 2):
                self.on_game_loss()
                return
            
            # Check draw
            if GameLogic.is_board_full(self.board):
                self.on_game_draw()
                return
            
            # Switch turn back to player
            self.my_turn = True
            self.start_timer()
            self.update_status("Lượt của bạn!")
    
    def receive_move(self, row, col):
        """
        Receive opponent's move from server
        
        Args:
            row, col: Position of opponent's move
        """
        if self.game_ended:
            return
        
        self.make_move(row, col, 2)
        
        # Check win
        if GameLogic.check_win(self.board, row, col, 2):
            self.on_game_loss()
            return
        
        # Check draw
        if GameLogic.is_board_full(self.board):
            self.on_game_draw()
            return
        
        # Switch turn to me
        self.my_turn = True
        self.start_timer()
        self.update_status("Lượt của bạn!")
    
    def add_competitor_move(self, row, col):
        """
        Add competitor's move and switch turn to current player
        This is called when receiving PROTOCOL_CARO from server
        Matches Java's addCompetitorMove() method
        
        Args:
            row, col: Position of competitor's move
        """
        # Mark opponent's move on board
        self.make_move(row, col, 2)  # 2 = opponent
        
        # Check if opponent won
        if GameLogic.check_win(self.board, row, col, 2):
            self.on_game_loss()
            return
        
        # Check for draw
        if GameLogic.is_board_full(self.board):
            self.on_game_draw()
            return
        
        # Enable my turn - THIS IS THE KEY FIX!
        self.my_turn = True
        self.update_status("Lượt của bạn!")
        self.start_timer()
        
        # Enable draw button when it's my turn (Java displayUserTurn logic)
        self.draw_button.config(state=tk.NORMAL)
        
        # Enable all empty buttons for clicking
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:  # Empty cell
                    self.buttons[i][j].config(state=tk.NORMAL)
    
    def start_game(self):
        """Start the game"""
        self.game_started = True
        self.game_ended = False
        self.draw_button.config(state=tk.NORMAL)
        
        if self.my_turn:
            self.start_timer()
            self.update_status("Lượt của bạn!")
        else:
            self.update_status("Lượt đối thủ...")
    
    def start_timer(self):
        """Start turn timer - CRITICAL FIX for double-start prevention"""
        # STEP 1: Cancel any existing timer callback first
        if self.timer_id is not None:
            try:
                self.window.after_cancel(self.timer_id)
                log(f"[TIMER] Cancelled existing timer callback ID={self.timer_id}", "DEBUG")
            except:
                pass
            self.timer_id = None
        
        # STEP 2: Check if timer already running (防止 double start)
        if self.timer_running:
            log(f"[TIMER] WARNING: Timer already running! Ignoring start request.", "WARNING")
            return
        
        # STEP 3: Initialize new timer
        self.time_left = TURN_TIME_LIMIT
        self.timer_running = True
        log(f"[TIMER] Starting NEW timer with {self.time_left}s", "DEBUG")
        
        # STEP 4: Start timer loop
        self.update_timer()
    
    def stop_timer(self):
        """Stop timer - CRITICAL FIX"""
        if self.timer_running:
            log(f"[TIMER] Stopping timer at {self.time_left}s", "DEBUG")
        
        # Cancel pending callback
        if self.timer_id is not None:
            try:
                self.window.after_cancel(self.timer_id)
                log(f"[TIMER] Cancelled timer callback ID={self.timer_id}", "DEBUG")
            except:
                pass
            self.timer_id = None
        
        self.timer_running = False
        self.time_left = TURN_TIME_LIMIT
    
    def update_timer(self):
        """Update timer display - called every 1 second - CRITICAL FIX"""
        # Check if timer should stop
        if not self.timer_running:
            log(f"[TIMER] Timer stopped, exiting update loop", "DEBUG")
            self.timer_id = None
            return
        
        # Update display
        self.timer_label.config(text=f"⏱ {self.time_left}s")
        log(f"[TIMER] Tick: {self.time_left}s remaining", "DEBUG")
        
        # Check timeout
        if self.time_left <= 0:
            log(f"[TIMER] Timeout!", "DEBUG")
            self.timer_running = False
            self.timer_id = None
            self.on_timeout()
            return  # CRITICAL: Don't schedule next callback
        
        # Decrement time
        self.time_left -= 1
        
        # Schedule next update - CRITICAL: Save callback ID
        self.timer_id = self.window.after(1000, self.update_timer)
    
    def on_timeout(self):
        """Handle timeout"""
        self.stop_timer()
        
        if self.is_ai_mode:
            messagebox.showwarning("Hết giờ", "Bạn đã hết thời gian!")
            self.on_game_loss()
        else:
            # Send timeout to server
            if Client.socket_handle:
                Client.socket_handle.write(create_message(PROTOCOL_LOSE))
    
    def update_status(self, status):
        """Update status label"""
        self.status_label.config(text=status)
    
    def on_game_win(self):
        """Handle game win"""
        self.game_ended = True
        self.stop_timer()
        self.draw_button.config(state=tk.DISABLED)
        
        messagebox.showinfo("Chiến thắng!", "🎉 Chúc mừng! Bạn đã thắng!")
        
        # Send win to server (if not AI mode)
        if not self.is_ai_mode and Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_WIN))
    
    def on_game_loss(self):
        """Handle game loss"""
        self.game_ended = True
        self.stop_timer()
        self.draw_button.config(state=tk.DISABLED)
        
        messagebox.showinfo("Thua cuộc", "😢 Bạn đã thua!")
    
    def on_game_draw(self):
        """Handle game draw"""
        self.game_ended = True
        self.stop_timer()
        self.draw_button.config(state=tk.DISABLED)
        
        messagebox.showinfo("Hòa", "🤝 Trò chơi hòa!")
    
    def new_game(self):
        """
        Start a new game (called by server after game ends)
        Matches Java's newgame() method
        """
        # Increment numberOfMatch for next round
        # This determines who goes first and what symbols to use
        self.number_of_match += 1
        
        # Reset game state
        self.game_ended = False
        self.game_started = True
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Determine turn based on new numberOfMatch
        # Java: if (numberOfMatch % 2 == 0) → current player goes first
        self.my_turn = (self.number_of_match % 2 == 0)
        
        # Reset UI
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].config(
                    text="",
                    bg="white",
                    state=tk.NORMAL if self.my_turn else tk.DISABLED,
                    relief=tk.RAISED,
                    fg="black"
                )
        
        # Re-enable draw button
        self.draw_button.config(state=tk.NORMAL)
        
        # Show message and start timer if it's my turn
        if self.my_turn:
            messagebox.showinfo("Ván mới", "Đến lượt bạn đi trước!")
            self.update_status("Lượt của bạn!")
            self.start_timer()
        else:
            messagebox.showinfo("Ván mới", "Đối thủ đi trước!")
            self.update_status("Lượt đối thủ...")
    
    def request_draw(self):
        """Request draw with opponent - IMPROVED UX"""
        # Validation
        if not self.my_turn:
            messagebox.showwarning("Cảnh báo", "Chưa đến lượt của bạn!")
            return
        
        if self.game_ended:
            messagebox.showwarning("Cảnh báo", "Game đã kết thúc!")
            return
        
        # Handle AI mode
        if self.is_ai_mode:
            if messagebox.askyesno("Hòa?", "Bạn muốn hòa với AI?"):
                self.on_game_draw()
            return
        
        # Confirm with user
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn yêu cầu hòa?"):
            return
        
        # Send request to server
        if Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_DRAW_REQUEST))
            messagebox.showinfo("Yêu cầu hòa", "Đã gửi yêu cầu hòa đến đối thủ!\nChờ phản hồi...")
            
            # Disable button temporarily to prevent spam
            self.draw_button.config(state=tk.DISABLED)
            
            log(f"[DRAW] Sent draw request", "INFO")
    
    def receive_draw_request(self):
        """Receive draw request from opponent - matches Java showDrawRequest()"""
        result = messagebox.askyesno(
            "Yêu cầu hòa", 
            f"{self.competitor.get_nickname()} muốn hòa.\n\nBạn đồng ý không?"
        )
        
        if result:
            # Accept draw
            log(f"[DRAW] Accepted draw request", "INFO")
            if Client.socket_handle:
                Client.socket_handle.write(create_message(PROTOCOL_DRAW_CONFIRM))
            messagebox.showinfo("Chấp nhận", "Bạn đã chấp nhận hòa!")
        else:
            # Reject draw
            log(f"[DRAW] Refused draw request", "INFO")
            if Client.socket_handle:
                Client.socket_handle.write(create_message(PROTOCOL_DRAW_REFUSE))
            messagebox.showinfo("Từ chối", "Bạn đã từ chối yêu cầu hòa!")
    
    # Alias for Client callback compatibility
    def show_draw_request(self):
        """Alias for receive_draw_request"""
        self.receive_draw_request()
    
    def show_draw_refuse(self):
        """Handle draw request refused by opponent"""
        messagebox.showinfo("Từ chối hòa", f"{self.competitor.get_nickname()} đã từ chối yêu cầu hòa!")
        
        # Re-enable draw button when my turn comes back
        if self.my_turn and not self.game_ended:
            self.draw_button.config(state=tk.NORMAL)
        
        log(f"[DRAW] Draw request refused by opponent", "INFO")
    
    def handle_draw_game(self):
        """Handle draw game from server"""
        self.on_game_draw()
    
    def receive_draw_response(self, accepted):
        """
        Receive draw response from opponent
        
        Args:
            accepted: True if opponent accepted, False otherwise
        """
        if accepted:
            messagebox.showinfo("Hòa", "Đối thủ đã chấp nhận hòa!")
            self.on_game_draw()
        else:
            messagebox.showinfo("Từ chối", "Đối thủ đã từ chối yêu cầu hòa!")
    
    def send_chat(self):
        """Send chat message"""
        message = self.chat_entry.get().strip()
        if not message:
            return
        
        # Display own message
        self.add_chat_message("Bạn", message)
        
        # Send to server (if not AI mode)
        if not self.is_ai_mode and Client.socket_handle:
            Client.socket_handle.write(create_message(PROTOCOL_CHAT, message))
        
        # Clear input
        self.chat_entry.delete(0, tk.END)
        
        # AI auto-reply
        if self.is_ai_mode:
            self.window.after(1000, lambda: self.add_chat_message("AI", "Tôi là AI, tôi không trò chuyện được 🤖"))
    
    def add_chat_message(self, sender, message):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def receive_chat(self, message):
        """Receive chat from opponent"""
        log(f"[GAME CHAT] Received message: {message} from {self.competitor.get_nickname()}", "DEBUG")
        self.add_chat_message(self.competitor.get_nickname(), message)
    
    def leave_room(self):
        """Leave the game room - Java pattern: close all views, open new homepage"""
        # Ask for confirmation only if game is in progress
        if not self.game_ended and self.game_started:
            if not messagebox.askyesno("Xác nhận", "Rời phòng sẽ tính là thua. Bạn có chắc?"):
                return
        
        # Stop timer first
        self.stop_timer()
        
        # Send leave message to server (if not AI mode)
        if not self.is_ai_mode and Client.socket_handle:
            try:
                Client.socket_handle.write(create_message(PROTOCOL_LEFT_ROOM))
            except:
                pass
        
        # Close all views (including homepage if it exists) - Java pattern
        Client.close_all_views()
        
        # Open new homepage - Java pattern
        Client.open_homepage()
    
    def on_closing(self):
        """Handle window close button"""
        self.leave_room()
    
    def show(self):
        """Show window"""
        self.window.deiconify()
        # Update status when game starts
        if self.game_started:
            if self.my_turn:
                self.update_status("Lượt của bạn!")
                self.start_timer()
            else:
                self.update_status("Lượt đối thủ...")
    
    def close(self):
        """Close window"""
        self.stop_timer()
        try:
            # Disable chat scrollbar to prevent TclError
            if hasattr(self, 'chat_display'):
                try:
                    self.chat_display.config(state=tk.DISABLED)
                except:
                    pass
            # Destroy window
            self.window.destroy()
        except Exception as e:
            log(f"Error closing game window: {e}", "ERROR")
