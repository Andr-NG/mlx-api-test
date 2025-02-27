import logging
import data
import os
import requests
import utils
from pydantic_core import ValidationError
from dotenv import load_dotenv
from models import MLX as mlx_models

load_dotenv()
logger = logging.getLogger('my_logger')
config = utils.ConfigProvider()


class MLX:
    """All the MLX endpoints from PAM and PM."""

    def __init__(self, url: str) -> None:
        self.url = url

    def sign_in(self, login: str, password: str) -> dict:
        """Sign in

        Args:
            login (str): email
            password (str): password

        Returns:
            dict: sign in response
        """
        URL = self.url + '/user/signin'
        try:
            # Calling the endpoint to retrieve data.
            credentials = mlx_models.UserCreds(email=login, password=password)
            data = requests.post(url=URL, data=credentials.to_json())
            logger.info(
                f"Receiving response from {self.sign_in.__name__}: {data.json()['status']}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def refresh_token(self, workspace_id: str, refresh_token: str, token: str) -> dict:
        """Update token

        Args:
            workspace_id (str): Workspace ID
            refresh_token (str): Refresh token
            token (str): Bearer token

        Returns:
            dict: Refresh token response
        """
        URL = self.url + "/user/refresh_token"
        HEADERS = config.get_headers(token=token)

        # Calling the endpoint to retrieve data.
        body = mlx_models.RefreshToken(
            email=os.getenv("EMAIL"),
            refresh_token=refresh_token,
            workspace_id=workspace_id,
        )
        try:
            data = requests.post(url=URL, data=body.to_json(), headers=HEADERS)

            # Parsing the retrieved data and updating the values
            logger.info(
                    f"Receiving response from {self.refresh_token.__name__}: {data.json()}"
                )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def get_folder_id(self, token: str) -> dict:
        """Get the folder id

        Args:
            token (str): Bearer token

        Returns:
            dict: Get folder id response (Default folder)
        """
        URL = self.url + '/workspace/folders'
        try:
            # Calling the endpoint to retrieve data.
            data = requests.get(url=URL, headers=config.get_headers(token=token))
            logger.info(
                f"Receiving response from {self.get_folder_id.__name__}: {data.json()}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def get_workspace_id(self, token: str) -> dict:
        """Get the workspace id

        Args:
            token (str): Bearer token

        Returns:
            dict: Get workspace response
        """
        URL = self.url + '/user/workspaces'
        try:
            # Calling the endpoint to retrieve data.
            data = requests.get(url=URL, headers=config.get_headers(token=token))
            logger.info(
                f"Receiving response from {self.get_workspace_id.__name__}: {data.json()}"
            )

            # parsed = mlx_models.UserWorkspaceArrayResponse(**data)
            # SharedVars.update_workspace_id(workspace_id=parsed.data.workspaces[0].workspace_id)
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def create_profile(self, profile_params: dict, token: str) -> dict:
        """Create a profile

        Args:
            profile_params (dict): profile data
            token (str): Bearer token

        Returns:
            dict: create profile response
        """
        URL = self.url + '/profile/create'
        try:
            # Calling the endpoint to retrieve data.
            body = mlx_models.CreateProfile.from_dict(profile_params)
            data = requests.post(
                url=URL, data=body.to_json(), headers=config.get_headers(token=token)
            )
            logger.info(
                f"Receiving response from {self.create_profile.__name__}: {data.json()}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def delete_profile(self, profile_ids: list, token: str, permanently=True) -> dict:
        """Delete profiles

        Args:
            token (str): Bearer token
            profile_ids (list): List of profiles to delete
            permanently (boolean): Permanent delete

        Returns:
            dict: delete profile response
        """
        URL = self.url + "/profile/remove"
        try:
            # Calling the endpoint to delete profiles.
            body = mlx_models.RemoveProfiles(ids=profile_ids, permanently=permanently)
            data = requests.post(
                url=URL, data=body.to_json(), headers=config.get_headers(token=token)
            )
            logger.info(
                f"Receiving response from {self.delete_profile.__name__}: {data.json()}"
            )

            return data.json()

        except ValidationError as e:
            logger.error('ValidationError occurred: %s', e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def get_baked_meta(self, profile_id: str, token: str) -> dict:
        """Get baked profile metadata

        Args:
            token (str): Bearer token
            profile_id (str): profile ID

        Returns:
            dict: get baked meta response
        """
        URL = self.url + '/profile/baked'
        try:
            params = {'meta_id': profile_id}
            data = requests.get(
                url=URL, params=params, headers=config.get_headers(token=token)
            )
            logger.info(
                f"Receiving response from {self.get_baked_meta.__name__}: {data.json()}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def search_profile(self, token: str) -> dict:
        """Search profile

        Args:
            search_params (dict): search params

        Returns:
            dict: Search profile response
        """
        URL = self.url + '/profile/search'
        try:
            body = mlx_models.ProfileSearchCriteria(**data.PROFILE_SEARCH)
            raw_data = requests.post(
                url=URL, data=body.to_json(), headers=config.get_headers(token=token)
            )
            logger.info(
                f"Receiving response from {self.search_profile.__name__}: {raw_data.status_code}"
            )
            return raw_data.json()

        except ValidationError as e:
            logger.error('ValidationError occurred: %s', e)
            raise

        except Exception as e:
            logger.error('Unexpected error occurred: %s', e)
            raise
