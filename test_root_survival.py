"""
Simple test to check if Client.root survives
"""

import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.controller.client import Client

# Create root
root = tk.Tk()
root.withdraw()
Client.root = root

print("Client.root created:", Client.root)
print("Client.root winfo_exists():", Client.root.winfo_exists())

# Create a Toplevel
window1 = tk.Toplevel(Client.root)
window1.title("Window 1")
print("\nCreated Window 1")
print("Client.root still exists:", Client.root.winfo_exists())

# Destroy window1
window1.destroy()
print("\nDestroyed Window 1")
print("Client.root still exists:", Client.root.winfo_exists())

# Try to create another Toplevel
try:
    window2 = tk.Toplevel(Client.root)
    window2.title("Window 2")
    print("\n✅ Created Window 2 successfully")
    print("Client.root still exists:", Client.root.winfo_exists())
    window2.destroy()
except Exception as e:
    print(f"\n❌ Error creating Window 2: {e}")

# Clean up
root.destroy()
print("\n✅ Test complete")
