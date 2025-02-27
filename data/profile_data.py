import faker
from pathlib import Path
fake = faker.Faker()

PROFILE_GENERIC = {
    'browser_type': 'mimic',
    'folder_id': '',
    'name': f'{fake.name()}',
    'os_type': 'windows',
    'parameters': {
        'fingerprint': {},
        'flags': {
            'audio_masking': 'mask',
            'fonts_masking': 'mask',
            'geolocation_masking': 'mask',
            'geolocation_popup': 'prompt',
            'graphics_masking': 'mask',
            'graphics_noise': 'mask',
            'localization_masking': 'mask',
            'media_devices_masking': 'mask',
            'navigator_masking': 'mask',
            'ports_masking': 'mask',
            'proxy_masking': 'disabled',
            'quic_mode': 'natural',
            'screen_masking': 'mask',
            'timezone_masking': 'mask',
            'webrtc_masking': 'disabled',
            'startup_behavior': 'recover',
        },
        'storage': {'is_local': False, 'save_service_worker': False},
    },
    'times': 1,
}

PROFILE_PROXY_CUSTOM = {
    'browser_type': 'mimic',
    'folder_id': '',
    'name': f'{fake.name()}',
    'os_type': 'windows',
    'parameters': {
        "proxy": {
            "type": "http",
            "host": "rotating.proxyempire.io",
            "port": 9000,
            "username": "yzBYkTa4iCrZYvmn",
            "password": "wifi;vn;;hanoi;cau+giay",
            "save_traffic": False
        },
        'fingerprint': {},
        'flags': {
            'audio_masking': 'mask',
            'fonts_masking': 'mask',
            'geolocation_masking': 'mask',
            'geolocation_popup': 'prompt',
            'graphics_masking': 'mask',
            'graphics_noise': 'mask',
            'localization_masking': 'mask',
            'media_devices_masking': 'mask',
            'navigator_masking': 'mask',
            'ports_masking': 'mask',
            'proxy_masking': 'custom',
            'quic_mode': 'natural',
            'screen_masking': 'mask',
            'timezone_masking': 'mask',
            'webrtc_masking': 'disabled',
            'startup_behavior': 'recover',
        },
        'storage': {'is_local': False, 'save_service_worker': False},
    },
    'times': 1,
}


QUICK_PROFILE_SELENIUM = {
    'browser_type': 'mimic',
    'os_type': 'windows',
    'automation': 'selenium',
    'parameters': {
        'fingerprint': {},
        'flags': {
            'proxy_masking': 'disabled',
            'audio_masking': 'mask',
            'fonts_masking': 'mask',
            'geolocation_masking': 'mask',
            'geolocation_popup': 'prompt',
            'graphics_masking': 'mask',
            'graphics_noise': 'mask',
            'localization_masking': 'mask',
            'media_devices_masking': 'mask',
            'navigator_masking': 'mask',
            'ports_masking': 'mask',
            'screen_masking': 'mask',
            'timezone_masking': 'mask',
            'webrtc_masking': 'mask',
            'startup_behavior': 'recover'
        }
    }
}

HOME = Path.home()

IMPORT_PROFILE_DATA = {
    'import_path': HOME / 'mlx' / 'exports',
    'is_local': False
}

IMPORT_PROFILE_DATA_IS_LOCAL_TRUE = {
    'import_path': HOME / 'mlx' / 'exports',
    'is_local': True
}