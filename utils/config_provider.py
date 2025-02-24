from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()


class ConfigProvider:

    BACKEND_URLS = {
        'QA': 'https://api-qa.mlx.yt',
        'DEV': 'https://api-dev.mlx.yt',
        'STAGING-EU': 'https://api-staging-eu.mlx.yt',
        'Multilogin EU': 'https://api.multilogin.com',
        'INDIGO_PROD': 'https://api.indigobrowser.com',
        'INDIGO_DEV': 'https://api-indigo-test.mlx.yt',
        'MLX_LT': 'https://api-lt.mlx.yt',
    }
    LAUNCHER_URLS = {
        'v1': 'https://launcher.mlx.yt:45001/api/v1',
        'v2': 'https://launcher.mlx.yt:45001/api/v2',
        'v3': 'https://launcher.mlx.yt:45001/api/v3',
    }
    BASE_DIR = Path(__file__).parent.parent
    session_env = os.getenv('ENV')
    launcher_val = os.getenv('LAUNCHER_VER')

    def get_url(self) -> str:
        if self.session_env not in self.BACKEND_URLS.keys():
            raise ValueError(
                f"Wrong env value: {self.session_env}. Supported envs are: {', '.join(self.BACKEND_URLS.keys())}"  # noqa: E501
            )
        else:
            return self.BACKEND_URLS[self.session_env]

    def get_launcher_url(self) -> str:
        if self.launcher_val.lower() not in self.LAUNCHER_URLS.keys():
            raise ValueError(
                f"Wrong env value: {self.launcher_val}. Supported envs are: {', '.join(self.LAUNCHER_URLS.keys())}"  # noqa: E501
            )
        else:
            return self.LAUNCHER_URLS[self.launcher_val.lower()]

    def get_headers(self, token: str) -> dict[str, str]:
        """Composing headers for a request

        Args:
            token (str): token

        Returns:
            dict[str, str]: headers with Bearer Token
        """
        headers = {"Accept": "application/json"}
        headers.setdefault("Authorization", f"Bearer {token}")
        return headers
