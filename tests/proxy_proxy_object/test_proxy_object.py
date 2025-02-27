import pytest
import API
import data
import logging
from models import MLX as mlx_models
from pytest import FixtureRequest
from utils import Helper

logger = logging.getLogger("my_logger")
helper = Helper()


class TestProxyObject:

    @pytest.mark.parametrize(data.PROXY_ARGS, data.PROXY_VALS, ids=data.PROXY_IDS)
    def test_create_profile_with_proxy(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        mlx_api: API.MLX,
        sign_in: tuple,
        get_folder_id: str,
        proxy: dict
    ) -> None:
        """_summary_

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            mlx_api (API.MLX): API.MLX
            sign_in (tuple): Bearer token and refresh_token
            get_folder_id (str): Folder ID
            profile_params (dict): Parameterized value for the proxy object
        """
        logger.info(f"Executing {request.node.name}")
        token, _ = sign_in  # Unpacking Bearer token

        # Creating a profile with a valid proxy
        body = data.PROFILE_PROXY_CUSTOM
        body['folder_id'] = get_folder_id
        body['parameters']['proxy'] = proxy
        r = mlx_api.create_profile(
            profile_params=body, token=token,
        )
        profile_response = mlx_models.ArrayOfIDsResponse(**r)
        profile_list = profile_response.data.ids

        assert profile_response.status.http_code == 201, f"Profile not created {r}"

        # Starting the profile to populate adapter logs
        profile_start = launcher_api.start_profile(
            folder_id=get_folder_id, profile_id=profile_list[0], token=token)

        assert profile_response.status.http_code == 201, f"Profile failed to start {profile_start}"

        # Verifying the proxy sent tp to the adapter tester
        profile = helper.get_fingerprints_from_logs(
            profile_id=profile_list[0]
        )
        assert profile.data.core.proxy.type == body['parameters']['proxy']['type']
        assert profile.data.core.proxy.host == body['parameters']['proxy']['host']
        assert profile.data.core.proxy.port == body['parameters']['proxy']['port']
        assert profile.data.core.proxy.username == body['parameters']['proxy']['username']
        assert profile.data.core.proxy.password == body['parameters']['proxy']['password']
