import logging
import data
import os
import requests
import utils
from typing import List
from pydantic_core import ValidationError
from dotenv import load_dotenv
from models import MLX as mlx_models
from API.shared_vars import SharedVars

load_dotenv()
logger = logging.getLogger('my_logger')
config = utils.ConfigProvider()


class MLX(SharedVars):
    """All the MLX endpoints from PAM and PM."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.HEADERS = None

    def sign_in(self, login: str, password: str) -> mlx_models.SigninResponse:
        """Sign in

        Args:
            login (str): email
            password (str): password

        Returns:
            mlx_models.SigninResponse: sign in response
        """
        URL = self.url + '/user/signin'
        try:
            # Calling the endpoint to retrieve data.
            credentials = mlx_models.UserCreds(email=login, password=password)
            data = requests.post(url=URL, data=credentials.to_json())
            logger.info(
                f"Receiving response from {self.sign_in.__name__}: {data.json()}"
            )

            # Parsing the retrieved data and updating the values.
            parsed_data = mlx_models.SigninResponse(**data.json())
            token = parsed_data.data.token
            refresh_token = parsed_data.data.refresh_token
            SharedVars.update_token(access_token=token)
            self.HEADERS = config.get_headers(SharedVars.get_var(variable='access_token'))
            SharedVars.update_refresh_token(refresh_token=refresh_token)
            return parsed_data

        except ValidationError as e:
            logger.error("Validation error occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def refresh_token(self) -> mlx_models.SigninResponse:
        """Refresh token

        Returns:
            SigninResponse: sign in response
        """
        URL = self.url + "/user/refresh_token"

        # Calling the endpoint to retrieve data.
        body = mlx_models.RefreshToken(
            email=os.getenv("EMAIL"),
            refresh_token=self.get_var('refresh_token'),
            workspace_id=self.get_var('workspace_id'),
        )
        data = requests.post(url=URL, data=body.to_json())

        # Parsing the retrieved data and updating the values
        parsed = mlx_models.SigninResponse(**data.json())
        token = parsed.data.token
        refresh_token = parsed.data.refresh_token
        SharedVars.update_token(access_token=token)
        self.HEADERS = config.get_headers(super().get_var(variable='access_token'))
        SharedVars.update_refresh_token(refresh_token=refresh_token)
        return parsed

    def get_folder_id(self, folder_name='Default folder') -> mlx_models.UserFolderArrayResponse:
        """Get the folder id

        Args:
            token (str): Bearer token

        Returns:
            UserFolderArrayResponse: list of available folders
        """
        URL = self.url + '/workspace/folders'
        try:
            # Calling the endpoint to retrieve data.
            data = requests.get(url=URL, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.get_folder_id.__name__}: {data.json()}"
            )

            # Extracting the default folder_id and updating the value.
            parsed = mlx_models.UserFolderArrayResponse(**data.json())
            for folder in parsed.data.folders:
                if folder.name == folder_name:
                    SharedVars.update_folder_id(folder_id=folder.folder_id)

            return parsed

        except ValidationError as e:
            logger.error("Validation error occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def get_workspace_id(self) -> mlx_models.UserWorkspaceArrayResponse:
        """Get the workspace id

        Args:
            token (str): Bearer token

        Returns:
            UserWorkspaceArrayResponse: list of available workspaces
        """
        URL = self.url + '/user/workspaces'
        try:
            # Calling the endpoint to retrieve data.
            data = requests.get(url=URL, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.get_workspace_id.__name__}: {data.json()}"
            )

            # Extracting the owner workspace_id and updating the value.
            parsed = mlx_models.UserWorkspaceArrayResponse(**data)
            SharedVars.update_workspace_id(workspace_id=parsed.data.workspaces[0].workspace_id)
            return parsed

        except ValidationError as e:
            logger.error("Validation error occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def create_profile(self, profile_params: dict) -> mlx_models.ArrayOfIDsResponse:
        """Create a profile

        Args:
            profile_params (dict): profile data

        Returns:
            ArrayOfIDsResponse: create profile response
        """
        URL = self.url + '/profile/create'
        try:
            # Calling the endpoint to retrieve data.
            body = mlx_models.CreateProfile.from_dict(profile_params)
            data = requests.post(url=URL, data=body.to_json(), headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.create_profile.__name__}: {data.json()}"
            )

            # Extracting the profile_id from the returned list and updating the value.
            parsed = mlx_models.ArrayOfIDsResponse(**data.json())
            profile_list: List[str] = parsed.data.ids
            SharedVars.update_profile_id(profile_id=profile_list[0])
            return parsed

        except ValidationError as e:
            logger.error("Validation error occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def delete_profile(self, profile_ids: list, permanently=True) -> mlx_models.MLXResponse:
        """Delete profiles

        Args:
            token (str): Bearer token
            profile_ids (list): list of profiles to delete

        Returns:
            MLXResponse: delete profile response
        """
        URL = self.url + "/profile/remove"
        try:
            # Calling the endpoint to delete profiles.
            body = mlx_models.RemoveProfiles(ids=profile_ids, permanently=permanently)
            data = requests.post(url=URL, data=body.to_json(), headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.delete_profile.__name__}: {data.json()}"
            )
            parsed = mlx_models.MLXResponse(**data.json())
            return parsed

        except ValidationError as e:
            logger.error("Validation error occurred: %s", e)
            raise

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def get_baked_meta(self) -> dict:
        """Get baked profile metadata

        Args:
            token (str): Bearer token
            profile_id (str): profile ID

        Returns:
            dict: get baked meta response
        """
        URL = self.url + '/profile/baked'
        try:
            params = {'meta_id': self.get_var('profile_id')}
            data = requests.get(url=URL, params=params, headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.get_baked_meta.__name__}: {data.json()}"
            )
            return data.json()

        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise

    def search_profile(self) -> dict:
        """Search profile

        Args:
            search_params (dict): search params

        Returns:
            dict: Search profile response
        """
        URL = self.url + '/profile/search'
        try:
            body = mlx_models.ProfileSearchCriteria(**data.PROFILE_SEARCH)
            raw_data = requests.post(url=URL, data=body.to_json(), headers=self.HEADERS)
            logger.info(
                f"Receiving response from {self.search_profile.__name__}: {raw_data.json()}"
            )
            return raw_data.json()

        except ValidationError as e:
            logger.error('ValidationError occurred: %s', e)
            raise

        except Exception as e:
            logger.error('Unexpected error occurred: %s', e)
            raise
