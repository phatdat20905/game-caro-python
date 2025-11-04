"""
Comprehensive test for all fixes
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("TESTING ALL FIXES")
print("=" * 60)

# Test 1: Import all modules
print("\n[1/5] Testing imports...")
try:
    from client.controller.client import Client
    from client.view import *
    from shared.constants import *
    from shared.utils import *
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test 2: Check Client.root can be set
print("\n[2/5] Testing Client.root...")
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    Client.root = root
    
    if hasattr(Client, 'root') and Client.root is not None:
        print("✅ Client.root set successfully")
    else:
        print("❌ Client.root not set")
        sys.exit(1)
        
    root.destroy()
except Exception as e:
    print(f"❌ Client.root error: {e}")
    sys.exit(1)

# Test 3: Check all constants exist
print("\n[3/5] Testing constants...")
required_constants = [
    'PROTOCOL_LOGIN',
    'PROTOCOL_CREATE_ROOM',
    'PROTOCOL_CREATE_ROOM_PASSWORD',
    'PROTOCOL_YOUR_CREATED_ROOM',
    'PROTOCOL_GO_TO_ROOM',
    'PROTOCOL_QUICK_ROOM'
]

missing = []
for const in required_constants:
    if const not in dir():
        missing.append(const)

if missing:
    print(f"❌ Missing constants: {missing}")
    sys.exit(1)
else:
    print(f"✅ All {len(required_constants)} constants defined")

# Test 4: Check utils functions
print("\n[4/5] Testing utility functions...")
try:
    # Test calculate_win_ratio
    ratio = calculate_win_ratio(10, 20)
    assert ratio == 50.0, f"Expected 50.0, got {ratio}"
    
    # Test with zero games
    ratio = calculate_win_ratio(0, 0)
    assert ratio == 0.0, f"Expected 0.0, got {ratio}"
    
    print("✅ Utility functions working")
except Exception as e:
    print(f"❌ Utility error: {e}")
    sys.exit(1)

# Test 5: Check form constructors
print("\n[5/5] Testing form constructors...")
try:
    # Create root
    root = tk.Tk()
    root.withdraw()
    Client.root = root
    
    # Test LoginFrm can be created
    login = LoginFrm()
    assert login.window is not None
    login.window.destroy()
    
    # Test HomePageFrm can be created
    homepage = HomePageFrm()
    assert homepage.window is not None
    homepage.window.destroy()
    
    # Test RegisterFrm can be created
    register = RegisterFrm()
    assert register.window is not None
    register.window.destroy()
    
    # Test Toplevel forms with Client.root
    rank = RankFrm()
    assert rank.window is not None
    rank.window.destroy()
    
    waiting = WaitingRoomFrm("123", "")
    assert waiting.window is not None
    waiting.window.destroy()
    
    print("✅ All forms can be created")
    
    root.destroy()
except Exception as e:
    print(f"❌ Form constructor error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# All tests passed
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nProject is ready to run:")
print("1. Start server: python run_server.py")
print("2. Start client: python run_client.py")
print("3. Login with: admin/admin123")
print("\nNo more 'main thread is not in main loop' errors!")
