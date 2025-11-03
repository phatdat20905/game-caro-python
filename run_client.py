"""
Main entry point for Caro Game Client
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.controller.client import Client
from shared.config import Config


def main():
    """Main function"""
    # Create hidden root window for Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Store root in Client for all forms to access
    Client.root = root
    
    # Connect to server
    print(f"Connecting to server at {Config.SERVER_HOST}:{Config.SERVER_PORT}...")
    
    if not Client.init_connection():
        messagebox.showerror(
            "Lỗi kết nối",
            f"Không thể kết nối đến server!\n"
            f"Địa chỉ: {Config.SERVER_HOST}:{Config.SERVER_PORT}\n\n"
            f"Vui lòng kiểm tra:\n"
            f"1. Server đã được khởi động chưa?\n"
            f"2. Địa chỉ server có đúng không?"
        )
        root.destroy()
        sys.exit(1)
    
    print("Connected to server successfully!")
    
    # Open login form (will use Client.root)
    Client.open_login()
    
    # Start Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
