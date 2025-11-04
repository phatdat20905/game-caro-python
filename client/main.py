"""
Client main entry point
"""

import tkinter as tk
from client.controller.client import Client
from shared.config import Config

def main():
    """Main client entry point"""
    # Initialize connection
    if not Client.init_connection():
        print("Cannot connect to server!")
        print(f"Please make sure server is running on {Config.SERVER_HOST}:{Config.SERVER_PORT}")
        return
    
    # Open login form
    Client.open_login()
    
    # Start Tkinter main loop
    tk.mainloop()


if __name__ == "__main__":
    main()
