"""
Client view package
"""

from .login_frm import LoginFrm
from .register_frm import RegisterFrm
from .homepage_frm import HomePageFrm
from .waiting_room_frm import WaitingRoomFrm
from .room_list_frm import RoomListFrm
from .friend_list_frm import FriendListFrm
from .rank_frm import RankFrm
from .game_client_frm import GameClientFrm
from .create_room_password_frm import CreateRoomPasswordFrm
from .find_room_frm import FindRoomFrm
from .competitor_info_frm import CompetitorInfoFrm

__all__ = [
    'LoginFrm',
    'RegisterFrm',
    'HomePageFrm',
    'WaitingRoomFrm',
    'RoomListFrm',
    'FriendListFrm',
    'RankFrm',
    'GameClientFrm',
    'CreateRoomPasswordFrm',
    'FindRoomFrm',
    'CompetitorInfoFrm'
]
