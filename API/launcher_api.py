import logging
import requests
import os
from pydantic_core import ValidationError
from utils import ConfigProvider
from data.profile_data import IMPORT_PROFILE_DATA
from models import launcher
from API.shared_vars import SharedVars

logger = logging.getLogger('my_logger')
config = ConfigProvider()


class Launcher(SharedVars):
    """Launcher API endpoints

    Args:
        SharedVars (class): shared states
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.HEADERS = config.get_headers(super().get_var('access_token'))
        self.export_id = None

    def start_profile(self, folder_id: str, profile_id: str) -> launcher.Response:
        """Start profile

        Args:
            folder_id (str): folider ID
            profile_id (str): profile ID

        Returns:
            Response: profile start response
        """

        URL = self.url + f"/profile/f/{folder_id}/p/{profile_id}/start"
        try:
            data = requests.get(url=URL, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.start_profile.__name__}: {data.json()}"
            )
            parsed = launcher.Response(**data.json())
            return parsed

        except ValidationError as e:
            logger.error("ValidationError occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def start_quick_profile(self, profile_param) -> launcher.Response:
        URL = self.url + '/profile/quick'
        body = launcher.QuickProfile(**profile_param)
        try:
            data = requests.post(
                url=URL, headers=self.HEADERS, data=body.to_json()
            )
            logger.info(
                f"Receiving response from {self.start_quick_profile.__name__}: {data.json()}"
            )
            parsed = launcher.Response(**data.json())
            return parsed

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
            parsed = launcher.VersionResponse(**data.json())
            return parsed

        except ValidationError as e:
            logger.error("ValidationError occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def stop_profile(self, profile_id: str) -> launcher.Response:
        """Stop profile

        Args:
            profile_id (str): profile ID

        Returns:
            Response: stop profile reponse
        """
        URL = self.url + f"/profile/stop/p/{profile_id}"
        try:
            data = requests.get(url=URL, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.stop_profile.__name__}: {data.json()}"
            )
            parsed = launcher.Response(**data.json())
            return parsed

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def stop_all_profiles(self) -> launcher.Response:
        """Stop all profiles

        Returns:
            Response: stop profile reponse
        """
        URL = self.url + '/profile/stop_all'
        params = {'type': 'all'}
        try:
            data = requests.get(url=URL, headers=self.HEADERS, params=params)
            logger.info(
                f"Receiving response from {self.stop_all_profiles.__name__}: {data.json()}"
            )
            parsed = launcher.Response(**data.json())
            return parsed

        except ValidationError as e:
            logger.error("ValidationError occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def retrieve_profile_status(self) -> launcher.ProfileStatusesResponse:
        """Retrieve profile status

        Returns:
            ProfileStatusesResponse: get status response
        """
        URL = self.url + '/profile/statuses'
        try:
            data = requests.get(url=URL, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.retrieve_profile_status.__name__}: {data.json()}"
            )
            parsed = launcher.ProfileStatusesResponse(**data.json())
            return parsed

        except ValidationError as e:
            logger.error("ValidationError occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def import_cookies(
        self, cookies: str, xpass_load: bool = False
    ) -> launcher.Response:
        """_summary_

        Args:
            cookies (str): cookies as JSON string
            xpass_load (bool, optional): XPASS flag. Defaults to False.

        Returns:
            dict: import cookies response
        """
        URL = self.url + "/cookie_import"
        try:
            body = launcher.CookieImport(
                profile_id=self.profile_id,
                folder_id=self.folder_id,
                cookies=cookies,
                import_advanced_cookies=xpass_load,
            )
            data = requests.post(url=URL, data=body.to_json(), headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.import_cookies.__name__}: {data.json()}"
            )
            return launcher.Response(**data.json())

        except ValidationError as e:
            logger.error("ValidationError occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def export_profile(self, profile_id) -> launcher.ProfileExportStatusResponse:
        """Export profile

        Returns:
            ProfileExportStatusResponse: export profile response
        """
        URL = self.url + f"/profile/{profile_id}/export"
        try:
            data = requests.post(url=URL, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.export_profile.__name__}: {data.json()}"
            )
            response = launcher.ProfileExportStatusResponse(**data.json())
            self.export_id = response.data.export_id
            return response

        except ValidationError as e:
            logger.error("Validation error occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def import_profile(self, export_id) -> launcher.ProfileImportStatusResponse:
        """Import profile

        Returns:
            ProfileImportStatusResponse: import profile response
        """
        URL = self.url + '/profile/import'
        try:
            import_data = IMPORT_PROFILE_DATA
            file_path = import_data['import_path'] / f"{export_id}.zip"

            if not file_path.exists():
                raise FileNotFoundError

            import_data['import_path'] = str(file_path)
            body = launcher.ImportProfileRequest(**import_data)
            data = requests.post(url=URL, headers=self.HEADERS, data=body.to_json())
            logger.info(
                f"Receiving response from {self.import_profile.__name__}: {data.json()}"
            )
            return launcher.ProfileImportStatusResponse(**data.json())

        except FileNotFoundError:
            logger.error(f"File {export_id}.zip not found")
            raise

        except ValidationError as e:
            logger.error('Validation error occurred: %s', e)
            raise

        except Exception as e:
            logger.error('Unexpected error occurred: %s', e)
            raise

    def get_profile_import_status(self, import_id: str) -> launcher.ProfileImportStatusResponse:
        """Import profile status

        Args:
            import_id (str): import_id

        Returns:
            launcher.ProfileImportStatusResponse: _description_
        """

        URL = self.url + f"/profile/imports/{import_id}/status"

        try:
            data = requests.get(url=URL, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.get_profile_import_status.__name__}: {data.json()}"
            )
            response = launcher.ProfileImportStatusResponse(**data.json())
            return response

        except ValidationError as e:
            logger.error('Validation error occurred: %s', e)
            raise

        except Exception as e:
            logger.error('Unexpected error occurred: %s', e)
            raise

    def get_profile_export_status(self, export_id: str) -> launcher.ProfileExportStatusResponse:
        """Export profile status

            Args:
                Export_id (str): Export_id

            Returns:
                launcher.ProfileExportStatusResponse: Export status response
            """

        URL = self.url + f"/profile/exports/{export_id}/status"

        try:
            data = requests.get(url=URL, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.get_profile_export_status.__name__}: {data.json()}"
            )
            response = launcher.ProfileExportStatusResponse(**data.json())
            return response

        except ValidationError as e:
            logger.error("Validation error occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise
