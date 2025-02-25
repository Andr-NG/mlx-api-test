import logging
import requests
from pydantic_core import ValidationError
from utils import ConfigProvider
from data.profile_data import IMPORT_PROFILE_DATA
from models import launcher

logger = logging.getLogger('my_logger')
config = ConfigProvider()


class Launcher:
    """Launcher API endpoints

    Args:
        SharedVars (class): shared states
    """

    def __init__(self, url: str) -> None:
        self.url = url

    def start_profile(self, folder_id: str, profile_id: str, token: str) -> dict:
        """Start profile

        Args:
            folder_id (str): folider ID
            profile_id (str): profile ID

        Returns:
            dict: profile start response
        """

        URL = self.url + f"/profile/f/{folder_id}/p/{profile_id}/start"
        try:
            data = requests.get(url=URL, headers=config.get_headers(token=token))
            logger.info(
                f"Receiving response from {self.start_profile.__name__}: {data.json()}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def start_quick_profile(self, profile_param: dict, token: str) -> dict:
        URL = self.url + '/profile/quick'
        body = launcher.QuickProfile(**profile_param)
        try:
            data = requests.post(
                url=URL, headers=config.get_headers(token=token), data=body.to_json()
            )
            logger.info(
                f"Receiving response from {self.start_quick_profile.__name__}: {data.json()}"
            )
            return data.json()

        except ValidationError as e:
            logger.error("ValidationError occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def get_launcher_version(self) -> launcher.VersionResponse:
        URL = self.url + '/version'
        try:
            data = requests.get(url=URL)
            logger.info(
                f"Receiving response from {self.get_launcher_version.__name__}: {data.json()}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def stop_profile(self, profile_id: str, token: str) -> launcher.Response:
        """Stop profile

        Args:
            profile_id (str): profile ID
            token (str): Bearer token

        Returns:
            Response: stop profile reponse
        """
        URL = self.url + f"/profile/stop/p/{profile_id}"
        try:
            data = requests.get(url=URL, headers=config.get_headers(token=token))
            logger.info(
                f"Receiving response from {self.stop_profile.__name__}: {data.json()}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def stop_all_profiles(self, token: str) -> dict:
        """Stop all profiles

        Args:
            token (str): Bearer token

        Returns:
            dict: stop profile reponse
        """
        URL = self.url + '/profile/stop_all'
        params = {'type': 'all'}
        try:
            data = requests.get(
                url=URL, headers=config.get_headers(token=token), params=params
            )
            logger.info(
                f"Receiving response from {self.stop_all_profiles.__name__}: {data.json()}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def retrieve_profile_status(self, token: str) -> dict:
        """Retrieve profile status

        Args:
            token (str): Bearer token

        Returns:
            ProfileStatusesResponse: get status response
        """
        URL = self.url + '/profile/statuses'
        try:
            data = requests.get(url=URL, headers=config.get_headers(token=token))
            logger.info(
                f"Receiving response from {self.retrieve_profile_status.__name__}: {data.json()}"
            )

            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def import_cookies(
        self, profile_id: str, folder_id: str, cookies: str, token: str, xpass_load: bool = False
    ) -> dict:
        """_summary_

        Args:
            token (str): Bearer token
            folder_id (str): Folder ID
            profile_id (str): Profile ID
            cookies (str): cookies as JSON string
            xpass_load (bool, optional): XPASS flag. Defaults to False.

        Returns:
            dict: import cookies response
        """
        URL = self.url + "/cookie_import"
        try:
            body = launcher.CookieImport(
                profile_id=profile_id,
                folder_id=folder_id,
                cookies=cookies,
                import_advanced_cookies=xpass_load,
            )
            data = requests.post(
                url=URL, data=body.to_json(), headers=config.get_headers(token=token)
            )
            logger.info(
                f"Receiving response from {self.import_cookies.__name__}: {data.json()}"
            )
            return data.json()

        except ValidationError as e:
            logger.error("ValidationError occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def export_profile(self, profile_id: str, token: str) -> dict:
        """Export profile

        Args:
            profile_id (str): Profile ID
            token (str): Bearer token

        Returns:
            dict: Export profile response
        """
        URL = self.url + f"/profile/{profile_id}/export"
        try:
            data = requests.post(url=URL, headers=config.get_headers(token=token))
            logger.info(
                f"Receiving response from {self.export_profile.__name__}: {data.json()}"
            )
            return data.json()

        except ValidationError as e:
            logger.error("Validation error occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def import_profile(self, token: str, export_id: str, import_data: dict) -> dict:
        """Import profile

        Args:
            token (str): Bearer token
            export_id (str): Export ID
            import_data (dict): Import data

        Returns:
            dict: Import profile response
        """

        URL = self.url + '/profile/import'
        try:

            body = launcher.ImportProfileRequest(**import_data)
            data = requests.post(
                url=URL, headers=config.get_headers(token=token), data=body.to_json()
            )
            logger.info(
                f"Receiving response from {self.import_profile.__name__}: {data.json()}"
            )
            # launcher.ProfileImportStatusResponse(**data.json())
            return data.json()

        except FileNotFoundError:
            logger.error(f"File {export_id}.zip not found")
            raise

        except ValidationError as e:
            logger.error('Validation error occurred: %s', e)
            raise

        except Exception as e:
            logger.error('Unexpected error occurred: %s', e)
            raise

    def get_profile_import_status(self, import_id: str, token: str) -> dict:
        """Import profile status

        Args:
            import_id (str): Import ID
            token (str): Bearer token

        Returns:
            dict: Import profile status
        """

        URL = self.url + f"/profile/imports/{import_id}/status"

        try:
            data = requests.get(
                url=URL, headers=config.get_headers(token=token)
            )
            logger.info(
                f"Receiving response from {self.get_profile_import_status.__name__}: {data.json()}"
            )

            return data.json()

        except Exception as e:
            logger.error('Unexpected error occurred: %s', e)
            raise

    def get_profile_export_status(self, export_id: str, token: str) -> dict:
        """Export profile status

            Args:
                export_id (str): Export ID
                token (str): Bearer token

            Returns:
                token: Export status response
            """

        URL = self.url + f"/profile/exports/{export_id}/status"

        try:
            data = requests.get(url=URL, headers=config.get_headers(token=token))
            logger.info(
                f"Receiving response from {self.get_profile_export_status.__name__}: {data.json()}"
            )
            # response = launcher.ProfileExportStatusResponse(**data.json())
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise
