import hashlib
import json
import pytest
import websocket
import API
import ssl
import logging
import time
import os
import pathlib
import data
from data import IMPORT_PROFILE_DATA
from utils import Helper
from pytest import FixtureRequest
from models import MLX as mlx_models
from models import launcher


logger = logging.getLogger("my_logger")
path = pathlib.Path()
home_dir = path.home()
helper = Helper()


class TestLauncherRegression:

    def test_sign_in(self, request: FixtureRequest, mlx_api: API.MLX) -> None:
        logger.info(f"Executing {request.node.name}")
        email = os.getenv("EMAIL")
        hashed_pass = hashlib.md5(os.getenv("PASSWORD").encode()).hexdigest()
        response: mlx_models.SigninResponse = mlx_api.sign_in(
            login=email, password=hashed_pass
        )

        assert response.status.http_code == 200, "Failed sign-in attempt"
        logger.info(f"Finishing {request.node.name}")

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_get_launcher_details(
        self, request: FixtureRequest, launcher_api: API.Launcher
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        response: launcher.VersionResponse = launcher_api.get_launcher_version()

        assert response.status.http_code == 200, "Failed to get launcher version"
        assert response.data.env == os.getenv("ENV")
        logger.info(f"Finishing {request.node.name}")

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_ws_connection(
        self, request: FixtureRequest, launcher_api: API.Launcher
    ) -> websocket.WebSocket | None:
        logger.info(f"Executing {request.node.name}")
        RETRIES = 3
        DELAY = 2
        URI = "wss://launcher.mlx.yt:45003/ws/data"

        # Connecting to websocket
        for attempt in range(1, RETRIES + 1):
            try:
                logger.info(f"Attempt {attempt} to set up websocket connection")
                ws = websocket.WebSocket()
                ws.connect(url=URI)

                assert ws.connected, "Connection failed"
                logger.info("Connection successfull!")
                break

            except websocket.WebSocketException as e:
                logger.error(f"Connection attempt {attempt} failed: {e}")
                if attempt < RETRIES:
                    logger.info("Attempting to connect again")
                    time.sleep(DELAY)
                else:
                    pytest.fail("Failed to connect to WebSocket after multiple retries")

            except ssl.SSLCertVerificationError as e:
                logger.error(
                    f"SSL Certification error: {e}. Re-connecting with verification skipped"
                )
                ws = websocket.WebSocket(sslopt={"cert_reqs": 0})
                ws.connect(url=URI)

                assert ws.connected, 'Connection failed'
                logger.info("Connection successfull!")
                break

            except Exception as e:
                logger.error(f"Unexpected error occurred: {e}")
                raise

        # Starting a QBP to populate messages.
        logger.info("Starting a QBP")
        response = launcher_api.start_quick_profile(
            profile_param=data.QUICK_PROFILE_SELENIUM
        )
        assert response.status.http_code == 200, 'Failed to start quick profile'

        ws_message = ws.recv()
        parsed = json.loads(ws_message)
        logger.info(f"Websocket messages are : {ws_message}")

        assert parsed, "Empty message"
        assert parsed["Profiles"][0]["IsQuick"] is True, 'Wrong value for IsQuick'
        assert parsed["Profiles"][0]["Status"] == "start_browser"
        ws.close()

    # @pytest.mark.skip(reason="Skipping this test for now")
    def test_get_folder_id(self, request: FixtureRequest, mlx_api: API.MLX) -> None:
        logger.info(f"Executing {request.node.name}")
        response = mlx_api.get_folder_id()

        assert response.status.http_code == 200, 'Failed to retrieve folder_id'
        logger.info(f"Finishing {request.node.name}")

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_create_profile(self, mlx_api: API.MLX, request: FixtureRequest) -> None:
        logger.info(f"Executing {request.node.name}")
        body = data.PROFILE_GENERIC
        logger.info("Adding folder_id to the body request")
        body.update({"folder_id": mlx_api.folder_id})
        response = mlx_api.create_profile(profile_params=body)

        assert response.status.http_code == 201, 'Failed to create a profile'
        logger.info(f"Finishing {request.node.name}")

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_import_cookies(self, launcher_api: API.Launcher, request: FixtureRequest) -> None:
        logger.info(f"Executing {request.node.name}")
        cookies = helper.read_cookies()
        response = launcher_api.import_cookies(cookies=cookies)
        assert response.status.http_code == 200
        logger.info(f"Finishing {request.node.name}")

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_launcher_profile(
        self, request: FixtureRequest, launcher_api: API.Launcher
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        response: launcher.Response = launcher_api.start_profile(
                # profile_id=launcher_api.get_var('profile_id'),
                # folder_id=launcher_api.get_var('folder_id'),
                profile_id=launcher_api.profile_id,
                folder_id=launcher_api.folder_id,
            )
        assert response.status.http_code == 200, 'Failed to launch profile'
        logger.info(f"Finishing {request.node.name}")

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_adapter_data(self, request: FixtureRequest, mlx_api: API.MLX) -> None:
        logger.info(f"Executing {request.node.name}")

        # Reading the adpater log file to validate
        start_meta, params = helper.read_adapter_logs()
        cookies = params.get('Cookies')
        start_profile_data = mlx_models.ReadyProfile(**start_meta['data'])

        # Retrieving real profile data
        data = mlx_api.get_baked_meta()
        response = mlx_models.ReadyProfileResponse(**data)

        # Checking cookies
        adapter_cookies = helper.read_cookies()
        assert cookies == adapter_cookies

        # Checking general data
        start_profile_data.is_local == response.data.is_local
        start_profile_data.name == response.data.name
        start_profile_data.folder_id == response.data.folder_id

        # Checking profile core
        start_profile_data.core.auto_update_core == response.data.core.auto_update_core
        start_profile_data.core.browser == response.data.core.browser
        start_profile_data.core.geolocation_fill_based_on_external_ip == response.data.core.geolocation_fill_based_on_external_ip  # noqa: E501
        start_profile_data.core.timezone_fill_based_on_external_ip == response.data.core.timezone_fill_based_on_external_ip  # noqa: E501

        # Checking profile fingerprints
        start_profile_data.fingerprint == response.data.fingerprint

        # Checking profile flags
        start_profile_data.flags == response.data.flags

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_profile_status_before_close(
        self, request: FixtureRequest, launcher_api: API.Launcher
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        response = launcher_api.retrieve_profile_status()
        status_data = response.data

        assert response.status.http_code == 200, 'Failed to retrieve profile status'
        assert launcher_api.profile_id in status_data.states, 'Profile not found'
        assert status_data.active_counter.cloud >= 1, 'No cloud profile running'
        assert status_data.active_counter.quick >= 1, 'No quick profile running'
        assert status_data.states[launcher_api.profile_id].status == 'browser_running'

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_close_all_profile(
        self, request: FixtureRequest, launcher_api: API.Launcher
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        time.sleep(2)
        response: launcher.Response = launcher_api.stop_all_profiles()

        assert response.status.http_code == 200, "Failed to stop profile"
        logger.info(f"Finishing {request.node.name}")

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_profile_status_after_close(
        self, request: FixtureRequest, launcher_api: API.Launcher
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        response = launcher_api.retrieve_profile_status()
        status_data = response.data

        assert response.status.http_code == 200, 'Failed to retrieve profile status'
        assert len(status_data.states) == 0
        assert status_data.active_counter.cloud == 0, 'Cloud profile still running'
        assert status_data.active_counter.quick == 0, 'Quick profile still running'
        logger.info(f"Finishing {request.node.name}")

    def test_profile_export(
        self, request: FixtureRequest, launcher_api: API.Launcher
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        response = launcher_api.export_profile(
            profile_id=launcher_api.profile_id
        )
        export_path: pathlib.Path = (
            IMPORT_PROFILE_DATA["import_path"] / f"{response.data.export_id}.zip"
        )

        assert export_path.exists(), 'Exported profile does not exist'
        assert response.status.http_code == 200, 'Failed to export profile'
        assert response.data.profile_id == launcher_api.profile_id

        time.sleep(2)

        logger.info(f"Retreiving the export status for {response.data.export_id}")
        export_status = launcher_api.get_profile_export_status(
            export_id=response.data.export_id
        )

        assert export_status.status.http_code == 200, 'Failed to get the export status'
        assert export_status.data.status == 'done', 'Export not completed'
        logger.info(f"Finishing {request.node.name}")

    def test_profile_import(self, request: FixtureRequest, launcher_api: API.Launcher) -> None:
        logger.info(f"Executing {request.node.name}")
        response = launcher_api.import_profile(
            export_id=launcher_api.export_id
        )

        assert response.status.http_code == 200, 'Failed to import profile'
        assert response.data.status == 'running'

        time.sleep(1)

        logger.info(f"Retrieving the import status for {response.data.import_id}")
        status_import = launcher_api.get_profile_import_status(
            import_id=response.data.import_id
        )
        assert status_import.status.http_code == 200, 'Failed to get the import status'
        assert status_import.data.status == 'done', 'Import not finished'

        logger.info(f"Finishing {request.node.name}")

    @pytest.mark.skip(reason="Skipping this test for now.")
    def test_delete_profile(self, request: FixtureRequest, mlx_api: API.MLX) -> None:
        logger.info(f"Executing {request.node.name}")
        r = mlx_api.search_profile()
        search_output = mlx_models.ProfileSearchQueryResponse(**r)
        profile_list = [profile.id for profile in search_output.data.profiles]
        delete_resp = mlx_api.delete_profile(profile_ids=profile_list)

        assert delete_resp.status.http_code == 200, 'Profiles not deleted'
        logger.info(f"Finishing {request.node.name}")
