# flake8: noqa
from data.profile_data import IMPORT_PROFILE_DATA, IMPORT_PROFILE_DATA_IS_LOCAL_TRUE


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
    ("QWERTY1234", "UNAUTHORIZED_REQUEST", 401, "Authorization error"),
    (None, "UNAUTHORIZED_REQUEST", 401, "Authorization error")
]
UNAUTH_IDS = ['Missing token', 'Invalid token']

PROFILE_IMPORT_ARGS = 'imported_data'
PROFILE_IMPORT_VALS = [
    (IMPORT_PROFILE_DATA),
    (IMPORT_PROFILE_DATA_IS_LOCAL_TRUE)
]
PROFILE_IMPORT_IDS = ['Imported profile is cloud', 'Imported profile is local']

PROFILE_EXPORT_INVALID_ID_ARGS = 'profile_id , http_code, error_code, msg'
PROFILE_EXPORT_INVALID_ID_VALS = [
    ('e51f7908-441c-4c2c-8405-ae2ff2842e9a',
     403,
     'PERMISSIONS_NOT_OK',
     'restricted permission'), # Proile created by another user
    ('e51f7908-441c-4c2c-8405',
     500,
     'INTERNAL_SERVER_ERROR',
     'internal server error') # Invalid profile_id
]
PROFILE_EXPORT_INVALID_ID_IDS = ['Profile created by another user', 'Invalid ID']
