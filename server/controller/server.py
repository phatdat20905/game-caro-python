"""
Main server
"""

import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from server.controller.server_thread import ServerThread
from server.controller.server_thread_bus import ServerThreadBus
from server.dao.database import get_database
from server.dao.user_dao import UserDAO
from shared.config import Config
from shared.constants import *
from shared.utils import log

class Server:
    """Main game server"""
    
    def __init__(self, host=None, port=None):
        """
        Initialize server
        
        Args:
            host: Server host address
            port: Server port
        """
        self.host = host or Config.SERVER_HOST
        self.port = port or Config.SERVER_PORT
        self.server_socket = None
        self.server_thread_bus = ServerThreadBus()
        self.client_counter = 0
        self.running = False
        self.admin = None
        
        # Initialize database
        db = get_database()
        if not db.init_database():
            log("Failed to initialize database", "ERROR")
        
        # Reset all users to offline status on server start
        user_dao = UserDAO()
        user_dao.reset_all_users_status()
        log("Reset all users to offline status")
    
    def set_admin(self, admin):
        """Set admin panel reference"""
        self.admin = admin
    
    def start(self):
        """Start server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(100)
            
            self.running = True
            log(f"Server started on {self.host}:{self.port}")
            log("Waiting for connections...")
            
            # Thread pool for handling clients
            executor = ThreadPoolExecutor(
                max_workers=MAX_THREADS,
                thread_name_prefix="ClientHandler"
            )
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    log(f"New connection from {client_address}")
                    
                    # Create server thread
                    server_thread = ServerThread(
                        client_socket,
                        self.client_counter,
                        self.server_thread_bus,
                        self.admin
                    )
                    
                    self.server_thread_bus.add(server_thread)
                    self.client_counter += 1
                    
                    # Execute in thread pool
                    executor.submit(server_thread.run)
                    
                    log(f"Active threads: {self.server_thread_bus.get_length()}")
                
                except Exception as e:
                    if self.running:
                        log(f"Accept connection error: {e}", "ERROR")
        
        except Exception as e:
            log(f"Server error: {e}", "ERROR")
        
        finally:
            self.stop()
    
    def stop(self):
        """Stop server"""
        self.running = False
        
        # Close all client connections
        for thread in self.server_thread_bus.get_list_server_threads():
            try:
                thread.cleanup()
            except Exception as e:
                log(f"Error closing thread: {e}", "ERROR")
        
        # Clear thread bus
        self.server_thread_bus = ServerThreadBus()
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        log("Server stopped")
    
    def get_active_connections(self):
        """Get number of active connections"""
        return self.server_thread_bus.get_length()


def main():
    """Main server entry point"""
    from server.view.admin import Admin
    import tkinter as tk
    
    # Create and run server in separate thread
    server = Server()
    
    # Create admin GUI
    root = tk.Tk()
    admin = Admin(root, server)
    server.set_admin(admin)
    
    # Start server in background thread
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    # Run admin GUI
    root.mainloop()


if __name__ == "__main__":
    main()
