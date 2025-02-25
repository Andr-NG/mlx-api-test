import json
import websocket
import API
import logging
import time
import os
import data
import pathlib
from data import QUICK_PROFILE_SELENIUM
from utils import Helper
from pytest import FixtureRequest
from models import MLX as mlx_models
from models import launcher


logger = logging.getLogger("my_logger")
path = pathlib.Path()
home_dir = path.home()
helper = Helper()


class TestLauncherRegression:
    export_id = None

    # @pytest.mark.xfail()
    def test_get_launcher_details(
        self, request: FixtureRequest, launcher_api: API.Launcher
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        data = launcher_api.get_launcher_version()
        response = launcher.VersionResponse(**data)

        assert response.status.http_code == 200, "Failed to get launcher version"
        assert response.data.env.lower() == os.getenv("ENV").lower()

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_ws_connection(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
        connect_ws: websocket.WebSocket,
    ) -> None:
        logger.info(f"Executing {request.node.name}")

        token, _ = sign_in
        data = launcher_api.start_quick_profile(
            profile_param=QUICK_PROFILE_SELENIUM, token=token)
        response = launcher.Response(**data)
        assert response.status.http_code == 200, f"Failed to start quick profile {response}"

        ws = connect_ws
        ws_message = ws.recv()
        parsed = json.loads(ws_message)
        logger.info(f"Websocket messages are : {ws_message}")

        assert parsed, "Empty message"
        assert parsed["Profiles"][0]["IsQuick"] is True, "Wrong value for IsQuick"
        assert parsed["Profiles"][0]["Status"] == "start_browser"

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_import_cookies(
        self,
        launcher_api: API.Launcher,
        request: FixtureRequest,
        sign_in: str,
        create_profile: list,
        get_folder_id: str,
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        cookies = helper.read_cookies()
        token, _ = sign_in
        data = launcher_api.import_cookies(
            cookies=cookies,
            profile_id=create_profile[0],
            folder_id=get_folder_id,
            token=token,
        )
        response = launcher.Response(**data)
        assert response.status.http_code == 200, f"Cookies not imported {response}"

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_launcher_profile(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        get_folder_id: str,
        create_profile: list,
        sign_in: tuple,
    ) -> None:
        token, _ = sign_in
        logger.info(f"Executing {request.node.name}")
        data = launcher_api.start_profile(
            profile_id=create_profile[0], folder_id=get_folder_id, token=token
        )
        response = launcher.Response(**data)
        assert response.status.http_code == 200, f"Failed to launch profile {response}"

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_adapter_data(
        self,
        request: FixtureRequest,
        mlx_api: API.MLX,
        sign_in: tuple,
        create_profile: list,
    ) -> None:
        logger.info(f"Executing {request.node.name}")

        token, _ = sign_in

        # Reading the adpater log file to validate
        start_meta, params = helper.read_adapter_logs()
        cookies = params.get("Cookies")
        start_profile_data = mlx_models.ReadyProfile(**start_meta["data"])

        # Retrieving real profile data
        data = mlx_api.get_baked_meta(token=token, profile_id=create_profile[0])
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

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_profile_status_before_close(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
        create_profile: list,
    ) -> None:
        token, _ = sign_in
        logger.info(f"Executing {request.node.name}")
        data = launcher_api.retrieve_profile_status(token=token)
        response = launcher.ProfileStatusesResponse(**data)
        status_data = response.data

        assert (
            response.status.http_code == 200
        ), f"Failed to retrieve profile status {response}"
        assert create_profile[0] in status_data.states, "Profile not found"
        assert status_data.active_counter.cloud >= 1, "No cloud profile running"
        assert status_data.active_counter.quick >= 0, "No quick profile running"
        assert status_data.states[create_profile[0]].status == "browser_running"

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_close_all_profile(
        self, request: FixtureRequest, launcher_api: API.Launcher, sign_in: tuple
    ) -> None:
        token, _ = sign_in
        logger.info(f"Executing {request.node.name}")
        time.sleep(1)
        data = launcher_api.stop_all_profiles(token=token)
        response = launcher.Response(**data)

        assert response.status.http_code == 200, "Failed to stop profile"

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_profile_status_after_close(
        self, request: FixtureRequest, launcher_api: API.Launcher, sign_in: tuple
    ) -> None:
        token, _ = sign_in
        logger.info(f"Executing {request.node.name}")
        data = launcher_api.retrieve_profile_status(token=token)
        response = launcher.ProfileStatusesResponse(**data)
        status_data = response.data

        assert response.status.http_code == 200, "Failed to retrieve profile status"
        assert len(status_data.states) == 0
        assert status_data.active_counter.cloud == 0, "Cloud profile still running"
        assert status_data.active_counter.quick == 0, "Quick profile still running"

    # @pytest.mark.skip(reason="Skipping this test for now.")
    @classmethod
    def test_profile_export(
        cls,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
        create_profile: list,
    ) -> None:
        token, _ = sign_in
        logger.info(f"Executing {request.node.name}")
        data = launcher_api.export_profile(profile_id=create_profile[0], token=token)
        response = launcher.ProfileExportStatusResponse(**data)
        cls.export_id = response.data.export_id

        assert response.data.export_path, "Exported profile does not exist"
        assert response.status.http_code == 200, "Failed to export profile"
        assert response.data.profile_id == create_profile[0]

        time.sleep(2)

        logger.info(f"Retreiving the export status for {response.data.export_id}")
        raw_data = launcher_api.get_profile_export_status(
            export_id=response.data.export_id, token=token
        )
        export_status = launcher.ProfileExportStatusResponse(**raw_data)
        assert export_status.status.http_code == 200, "Failed to get the export status"
        assert export_status.data.status == "done", "Export not completed"

    # @pytest.mark.skip(reason="Skipping this test for now.")
    @classmethod
    def test_profile_import(
        cls,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        token, _ = sign_in
        import_data = data.IMPORT_PROFILE_DATA
        file_path = import_data['import_path'] / f"{cls.export_id}.zip"
        import_data['import_path'] = str(file_path)

        r = launcher_api.import_profile(
            token=token,
            export_id=cls.export_id,
            import_data=import_data)
        response = launcher.ProfileImportStatusResponse(**r)

        assert response.status.http_code == 200, "Failed to import profile"
        assert response.data.status == "running"

        time.sleep(1)

        logger.info(f"Retrieving the import status for {response.data.import_id}")
        raw_data = launcher_api.get_profile_import_status(
            import_id=response.data.import_id, token=token
        )
        status_import = launcher.ProfileImportStatusResponse(**raw_data)

        assert status_import.status.http_code == 200, "Failed to get the import status"
        assert status_import.data.status == "done", "Import not finished"

    # @pytest.mark.skip(reason="Skipping this test for now.")
    def test_delete_profile(
        self,
        request: FixtureRequest,
        mlx_api: API.MLX,
        sign_in: tuple,
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        token, _ = sign_in
        r = mlx_api.search_profile(token=token)
        search_output = mlx_models.ProfileSearchQueryResponse(**r)
        profile_list = [profile.id for profile in search_output.data.profiles]
        data = mlx_api.delete_profile(profile_ids=profile_list, token=token)
        delete_resp = mlx_models.MLXResponse(**data)

        assert delete_resp.status.http_code == 200, "Profiles not deleted"
