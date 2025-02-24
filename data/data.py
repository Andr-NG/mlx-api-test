# flake8: noqa

import faker


RESTRICTIONS = {
    'workspace_id': '',
    'restrictions': {
        'plan_name': 'Team Monthly',
        'cloud_profiles_count': 1000,
        'allowed_browser_types': ['mimic', 'stealthfox', 'android'],
        'folders_count': 100000,
        'local_profiles_count': 1000,
        'team_members_count': 100,
        'active_profiles_count': 0,
        'automation_available': True,
        'ratelimit': [{'limit_size': 50, 'operation': 'all', 'window_size': '1m'}],
    },
}

PROFILE_SEARCH = {
    'offset': 0,
    'limit': 100,
    'search_text': '',
    'storage_type': 'all',
    'browser_type': None,
    'os_type': None,
    'core_version': None,
    'is_removed': False,
    'folder_id': None,
    'order_by':'updated_at',
    'sort': 'desc',
}
