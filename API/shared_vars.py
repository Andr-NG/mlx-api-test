from typing import Literal


class SharedVars:

    _access_token = None
    _refresh_token = None
    workspace_id = None
    folder_id = None
    profile_id = None

    @classmethod
    def get_var(
        cls,
        variable: Literal[
            'access_token', 'refresh_token', 'workspace_id', 'folder_id', 'profile_id'
        ],
    ) -> str:
        """Retrieving a variable for the test run

        Args:
            variable (str): Possible values: "access_token", "refresh_token", "workspace_id", "folder_id", "profile_id"  # noqa: E501

        Raises:
            ValueError: when the value is invalid

        Returns:
            str: one of the vars
        """
        VARS = {
            'access_token': cls._access_token,
            'refresh_token': cls._refresh_token,
            'workspace_id': cls.workspace_id,
            'folder_id': cls.folder_id,
            'profile_id': cls.profile_id,
        }
        if variable not in VARS:
            raise ValueError(
                f"Unsupported variable: {variable}. "
                f"Possible variables are: {', '.join(VARS.keys())}"
            )
        return VARS[variable]

    @classmethod
    def update_token(cls, access_token: str) -> None:
        """Update access_token

        Args:
            access_token (str): JWT access_token
        """
        cls._access_token = access_token

    @classmethod
    def update_refresh_token(cls, refresh_token: str) -> None:
        """Update refresh token

        Args:
            refresh_token (str): refresh token
        """
        cls._refresh_token = refresh_token

    @classmethod
    def update_workspace_id(cls, workspace_id: str) -> None:
        """Update workspace ID

        Args:
            workspace_id (str): workspace ID
        """
        cls.workspace_id = workspace_id

    @classmethod
    def update_folder_id(cls, folder_id: str) -> None:
        """Update folder ID

        Args:
            folder_id (str): folder ID
        """
        cls.folder_id = folder_id

    @classmethod
    def update_profile_id(cls, profile_id: str) -> None:
        """Update profile ID

        Args:
            profile_id (str): profile ID
        """
        cls.profile_id = profile_id
