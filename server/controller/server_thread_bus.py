"""
Server thread bus - manages all server threads
"""

from threading import Lock
from shared.utils import log

class ServerThreadBus:
    """Manages all active server threads"""
    
    def __init__(self):
        self.list_server_threads = []
        self.lock = Lock()
    
    def add(self, server_thread):
        """Add server thread to bus"""
        with self.lock:
            self.list_server_threads.append(server_thread)
            log(f"Added thread {server_thread.get_client_number()}, total: {len(self.list_server_threads)}")
    
    def remove(self, client_number):
        """Remove server thread by client number"""
        with self.lock:
            self.list_server_threads = [
                t for t in self.list_server_threads 
                if t.get_client_number() != client_number
            ]
            log(f"Removed thread {client_number}, remaining: {len(self.list_server_threads)}")
    
    def get_length(self):
        """Get number of active threads"""
        with self.lock:
            return len(self.list_server_threads)
    
    def get_list_server_threads(self):
        """Get copy of server thread list"""
        with self.lock:
            return self.list_server_threads.copy()
    
    def broadcast(self, client_number, message):
        """
        Broadcast message to all clients except sender
        
        Args:
            client_number: Sender's client number (to exclude)
            message: Message to broadcast
        """
        with self.lock:
            for thread in self.list_server_threads:
                if thread.get_client_number() != client_number:
                    try:
                        thread.write(message)
                    except Exception as e:
                        log(f"Broadcast error to client {thread.get_client_number()}: {e}", "ERROR")
    
    def get_server_thread_by_user_id(self, user_id):
        """Get server thread by user ID"""
        with self.lock:
            for thread in self.list_server_threads:
                if thread.get_user() and thread.get_user().get_id() == user_id:
                    return thread
        return None
    
    def send_message_to_user_id(self, user_id, message):
        """Send message to specific user by ID"""
        thread = self.get_server_thread_by_user_id(user_id)
        if thread:
            try:
                thread.write(message)
                return True
            except Exception as e:
                log(f"Send message error to user {user_id}: {e}", "ERROR")
        return False
