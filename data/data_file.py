# flake8: noqa
from data.profile_data import IMPORT_PROFILE_DATA, IMPORT_PROFILE_DATA_IS_LOCAL_TRUE, PROFILE_PROXY_CUSTOM


RESTRICTIONS = {
    "workspace_id": "",
    "restrictions": {
        "plan_name": "Team Monthly",
        "cloud_profiles_count": 1000,
        "allowed_browser_types": ["mimic", "stealthfox", "android"],
        "folders_count": 100000,
        "local_profiles_count": 1000,
        "team_members_count": 100,
        "active_profiles_count": 0,
        "automation_available": True,
        "ratelimit": [{"limit_size": 50, "operation": "all", "window_size": "1m"}],
    },
}

PROFILE_SEARCH = {
    "offset": 0,
    "limit": 100,
    "search_text": "",
    "storage_type": "all",
    "browser_type": None,
    "os_type": None,
    "core_version": None,
    "is_removed": False,
    "folder_id": None,
    "order_by": "updated_at",
    "sort": "desc",
}

UNAUTH_ARGS = "token, error_code, http_code, msg"
UNAUTH_VALS = [
    (None, "UNAUTHORIZED_REQUEST", 401, "Authorization error"),  # Missing token
    ("QWERTY1234", "UNAUTHORIZED_REQUEST", 401, "Authorization error"),  # Invalid token
    (
        "eyJhbGciOiJIUzUxMiJ9.eyJicGRzLmJ1Y2tldCI6Im1seC1icGRzLXN0YWdpbmctMSIsIm1hY2hpbmVJRCI6IiIsInByb2R1Y3RJRCI6InN0YWdpbmctZXUiLCJ3b3Jrc3BhY2VSb2xlIjoib3duZXIiLCJ2ZXJpZmllZCI6dHJ1ZSwicGxhbk5hbWUiOiJUZWFtIChNb250aGx5KSIsInNoYXJkSUQiOiJjYmUxMzgwMC1iYmFmLTRjOGYtODBiMy0xOTdmODk2Mzk0ZjIiLCJ1c2VySUQiOiJlYTEzYzUyNy02NTA4LTQ1YTEtODVhNC1jYWY4NDg2YTNhZWIiLCJlbWFpbCI6ImxhdW5jaGVyX3JlZ3Jlc3Npb25AbXVsdGlsb2dpbi5jb20iLCJpc0F1dG9tYXRpb24iOmZhbHNlLCJ3b3Jrc3BhY2VJRCI6IjE3OWMwZTE4LWEwYzUtNDcyNy1iNmNlLWI0NTYwNzM3ZDgwMiIsImp0aSI6IjBmNTNmOGRhLTVhMjctNGQ5ZS04OGYzLWIxYjk2MTgxMzBhZiIsInN1YiI6Ik1MWCIsImlzcyI6ImVhMTNjNTI3LTY1MDgtNDVhMS04NWE0LWNhZjg0ODZhM2FlYiIsImlhdCI6MTc0MDU0NTkzMiwiZXhwIjoxNzQwNTQ5NTMyfQ.e3WJVBlcH2dZWaGPBeNPEWdj2lQ1vAiFIrC99jXIBswwwmQyWfDaZ-wzHslI3xpLA-gL1nF_ZY6nW-xllg-EiQ",
        "EXPIRED_JWT_TOKEN",
        401,
        "Authorization error",
    ),  # Expired token
]
UNAUTH_IDS = ['Missing token', 'Invalid token', 'Expired token']

PROFILE_IMPORT_ARGS = 'imported_data'
PROFILE_IMPORT_VALS = [(IMPORT_PROFILE_DATA), (IMPORT_PROFILE_DATA_IS_LOCAL_TRUE)]
PROFILE_IMPORT_IDS = ['Imported profile is cloud', 'Imported profile is local']

PROFILE_EXPORT_INVALID_ID_ARGS = 'profile_id , http_code, error_code, msg'
PROFILE_EXPORT_INVALID_ID_VALS = [
    (
        "e51f7908-441c-4c2c-8405-ae2ff2842e9a",
        400,
        "BAD_REQUEST_BODY",
        "profile not found",
    ),  # Non-existent profile
    (
        "7343b3b4-0e54-455e-b02e-65d8cf1ea42e",
        403,
        "PERMISSIONS_NOT_OK",
        "restricted permission",  # Existing profile created by another user
    ),
    (
        "e51f7908-441c-4c2c-8405",
        500,
        "INTERNAL_SERVER_ERROR",
        "internal server error",
    ),  # Invalid profile_id
]
PROFILE_EXPORT_INVALID_ID_IDS = [
    'Non-existent profile',
    "Existing profile created by another user",
    "Invalid ID",
]

HTTP_PROXY_SAVER_FALSE = {
            "type": "http",
            "host": "rotating.proxyempire.io",
            "port": 9000,
            "username": "yzBYkTa4iCrZYvmn",
            "password": "wifi;vn;;hanoi;cau+giay",
            "save_traffic": False
        }
SOCKS_PROXY_SAVER_TRUE = {
            'type': 'socks5',
            'host': 'rotating.proxyempire.io',
            'port': 9000,
            'username': 'yzBYkTa4iCrZYvmn',
            'password': 'wifi;vn;;hanoi;cau+giay',
            'save_traffic': True
        }
PROXY_ARGS = 'proxy'
PROXY_VALS = [(HTTP_PROXY_SAVER_FALSE), (SOCKS_PROXY_SAVER_TRUE)]
PROXY_IDS = ['http, save_traffic is False', 'socks5, save_traffic is True']
