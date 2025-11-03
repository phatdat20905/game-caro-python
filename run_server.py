"""
Main entry point for Caro Game Server
"""

import sys
import os
import tkinter as tk
import threading

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.controller.server import Server
from server.view.admin import Admin


def main():
    """Main function"""
    print("=" * 60)
    print("CARO GAME SERVER")
    print("=" * 60)
    
    # Create root window
    root = tk.Tk()
    
    # Create server
    server = Server()
    
    # Create admin panel
    admin = Admin(root, server)
    
    # Set admin reference in server
    server.set_admin(admin)
    
    # Start server in background thread
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    print(f"Server started on {server.host}:{server.port}")
    print("Admin panel opened. Close the window to stop server.")
    
    # Run GUI
    root.mainloop()


if __name__ == "__main__":
    main()
