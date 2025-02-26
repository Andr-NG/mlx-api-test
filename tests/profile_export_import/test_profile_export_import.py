import pytest
import API
import logging
import time
import data
import pathlib
from data.profile_data import IMPORT_PROFILE_DATA
from models import MLX as mlx_models
from pytest import FixtureRequest
from models import launcher

logger = logging.getLogger("my_logger")


class TestProfileExportImport:
    """Test class contaning tests regarding the profile export/import feature.

    test_profile_import has to be invoked along with test_profile_export
    as the former is dependant on export_id and imported_profile_id
    """
    export_id = None
    imported_profile_id = None

    @classmethod
    def test_profile_export(
        cls,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
        create_profile: list,
    ) -> None:
        """ Testing profile export

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            sign_in (tuple): token and refresh_token
            create_profile (list): List of profiles
        """
        token, _ = sign_in
        logger.info(f"Executing {request.node.name}")

        # Exporting a profile
        r = launcher_api.export_profile(profile_id=create_profile[0], token=token)
        response = launcher.ProfileExportStatusResponse(**r)

        # Assigning export_id for futher use by test_profile_import
        cls.export_id = response.data.export_id

        # Create a Path object with the export path
        path = pathlib.Path(response.data.export_path)

        assert path.exists(), "Exported profile does not exist"
        assert response.status.http_code == 200, f"Failed to export profile {r}"
        assert response.data.profile_id == create_profile[0]

        time.sleep(2)

        # Checking profile export status
        logger.info(f"Retreiving the export status for {response.data.export_id}")
        raw_data = launcher_api.get_profile_export_status(
            export_id=response.data.export_id, token=token
        )
        export_status = launcher.ProfileExportStatusResponse(**raw_data)
        assert export_status.status.http_code == 200, "Failed to get the export status"
        assert export_status.data.status == "done", "Export not completed"

    # @pytest.mark.skip(reason='Skipping for now')
    @pytest.mark.parametrize(
        argnames=data.UNAUTH_ARGS, argvalues=data.UNAUTH_VALS, ids=data.UNAUTH_IDS
    )
    def test_profile_export_unauth(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        create_profile: list,
        token: str,
        http_code: str,
        error_code: str,
        msg: str,
    ) -> None:
        """Testing unauthorised calls to profile/import

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            create_profile (list): List of profiles
            token (str): parametrized value for token
            http_code (str): parametrized value for http_code
            error_code (str): parametrized value for error_code
            msg (str): parametrized value for msg
        """
        logger.info(f"Executing {request.node.name}")

        # Attempting to call the endpoint
        data = launcher_api.export_profile(profile_id=create_profile[0], token=token)
        response = launcher.ProfileExportStatusResponse(**data)

        assert response.status.error_code == error_code
        assert response.status.http_code == http_code
        assert response.status.message == msg

    # @pytest.mark.skip(reason='Skipping for now')
    @pytest.mark.parametrize(
            data.PROFILE_EXPORT_INVALID_ID_ARGS,
            data.PROFILE_EXPORT_INVALID_ID_VALS,
            ids=data.PROFILE_EXPORT_INVALID_ID_IDS
        )
    def test_profile_export_invalid_id(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
        profile_id: str,
        http_code: str,
        error_code: str,
        msg: str,
    ) -> None:
        """Testing sending calls with invalid profile id

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            sign_in (tuple): Bearer token and refresh token
            profile_id (str): parametrized value for profile id
            http_code (str): parametrized value for http_code
            error_code (str): parametrized value for error_code
            msg (str): parametrized value for msg
        """
        logger.info(f"Executing {request.node.name}")

        token, _ = sign_in  # Unpacking token and refresh_token after signing in

        data = launcher_api.export_profile(profile_id=profile_id, token=token)
        response = launcher.ProfileExportStatusResponse(**data)

        assert response.status.error_code == error_code
        assert response.status.http_code == http_code
        assert response.status.message == msg

    @classmethod
    # @pytest.mark.skip(reason='Skipping for now')
    @pytest.mark.parametrize(
        data.PROFILE_IMPORT_ARGS, data.PROFILE_IMPORT_VALS, ids=data.PROFILE_IMPORT_IDS
    )
    def test_profile_import(
        cls,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
        mlx_api: API.MLX,
        imported_data: dict
    ) -> None:
        """Testing profile import with different values for is_local

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            sign_in (tuple): token and refresh_token
            mlx_api (API.MLX): API.MLX
            imported_data (dict): parametrized input with different values for is_local
        """
        logger.info(f"Executing {request.node.name}")
        token, _ = sign_in  # Unpacking token and refresh_token after signing in

        # Importing a profile
        import_data = imported_data
        file_path = import_data['import_path'] / f"{cls.export_id}.zip"
        import_data['import_path'] = str(file_path)

        r = launcher_api.import_profile(
            token=token,
            export_id=cls.export_id,
            import_data=import_data)

        response = launcher.ProfileImportStatusResponse(**r)
        assert response.status.http_code == 200, f"Failed to import profile {r}"
        assert response.data.status == "running"

        time.sleep(1)

        # Checking the import status
        r = launcher_api.get_profile_import_status(
            import_id=response.data.import_id, token=token
        )
        status_import = launcher.ProfileImportStatusResponse(**r)

        assert status_import.status.http_code == 200, f"Failed to get the import status{r}"
        assert status_import.data.status == "done", "Import not finished"

        # Receiving the baked meta for the imported profile
        response = mlx_api.get_baked_meta(
            profile_id=status_import.data.new_profile_id,
            token=token)
        imported_profile_meta = mlx_models.ReadyProfileResponse(**response)

        # Verifying the storage type of the imported profile
        assert imported_profile_meta.data.is_local == import_data['is_local']

    # @pytest.mark.skip(reason='Skipping for now')
    def test_profile_import_invalid_path(
        cls,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
    ) -> None:
        """Testing profile import with invalid path

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            sign_in (tuple): tuple
        """
        logger.info(f"Executing {request.node.name}")
        token, _ = sign_in

        # Importing a profile
        import_data = IMPORT_PROFILE_DATA
        import_data['import_path'] = str(import_data['import_path']) + 'some_id.zip'

        r = launcher_api.import_profile(
            token=token,
            export_id=cls.export_id,
            import_data=import_data)

        response = launcher.ProfileImportStatusResponse(**r)
        assert response.status.http_code == 400
        assert response.status.error_code == 'BAD_REQUEST_BODY'
        assert response.status.message == 'import file not found'

    # @pytest.mark.skip(reason='Skipping for now')
    @pytest.mark.parametrize(
        argnames=data.UNAUTH_ARGS, argvalues=data.UNAUTH_VALS, ids=data.UNAUTH_IDS
    )
    def test_profile_import_unauth(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        token: str,
        http_code: str,
        error_code: str,
        msg: str,
    ) -> None:
        """Testing unauthorised calls to profile import

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            token (str): parametrized value for token
            http_code (str): parametrized value for http_code
            error_code (str): parametrized value for error_code
            msg (str): parametrized value for msg
        """
        logger.info(f"Executing {request.node.name}")

        # Attempting to call the endpoint with dummy data for import_data and export_id
        import_data = IMPORT_PROFILE_DATA
        import_data['import_path'] = str(import_data['import_path']) + 'some_id.zip'

        r = launcher_api.import_profile(
            export_id='some_id', import_data=import_data, token=token
        )
        response = launcher.ProfileExportStatusResponse(**r)

        assert response.status.error_code == error_code
        assert response.status.http_code == http_code
        assert response.status.message == msg

    # @pytest.mark.skip(reason='Skipping for now')
    @pytest.mark.parametrize(
        argnames=data.UNAUTH_ARGS, argvalues=data.UNAUTH_VALS, ids=data.UNAUTH_IDS
    )
    def test_get_import_status_unauth(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        token: str,
        http_code: str,
        error_code: str,
        msg: str,
    ) -> None:
        """Testing unauthorised calls to /profile/imports/import_id/status

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            token (str): parametrized value for token
            http_code (str): parametrized value for http_code
            error_code (str): parametrized value for error_code
            msg (str): parametrized value for msg
        """
        logger.info(f"Executing {request.node.name}")

        # Calling the endpoint with dummy data for import_id
        r = launcher_api.get_profile_import_status(import_id='some_id', token=token)
        response = launcher.ProfileImportStatusResponse(**r)

        assert response.status.error_code == error_code
        assert response.status.http_code == http_code
        assert response.status.message == msg

    # @pytest.mark.skip(reason='Skipping for now')
    @pytest.mark.parametrize(
        argnames=data.UNAUTH_ARGS, argvalues=data.UNAUTH_VALS, ids=data.UNAUTH_IDS
    )
    def test_get_export_status_unauth(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        token: str,
        http_code: str,
        error_code: str,
        msg: str,
    ) -> None:
        """Testing unauthorised calls to /profile/imports/import_id/status

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            token (str): parametrized value for token
            http_code (str): parametrized value for http_code
            error_code (str): parametrized value for error_code
            msg (str): parametrized value for msg
        """
        logger.info(f"Executing {request.node.name}")

        # Calling the endpoint with dummy data for import_id
        r = launcher_api.get_profile_export_status(export_id='some_id', token=token)
        response = launcher.ProfileExportStatusResponse(**r)

        assert response.status.error_code == error_code
        assert response.status.http_code == http_code
        assert response.status.message == msg

    # @pytest.mark.skip(reason='Skipping for now')
    def test_get_all_export_status(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
        create_profile: list,
    ) -> None:
        """Testing receiving all profile export status

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            sign_in (tuple): Bearer token and refresh token
            create_profile (list): List of profile
        """
        logger.info(f"Executing {request.node.name}")
        token, _ = sign_in  # Unpacking token and refresh_token after signing in
        r = launcher_api.get_all_export_status(token=token)
        response = launcher.ProfileExportStatusesResponse(**r)

        assert response.status.http_code == 200, f"Failed to receive the status: {r}"
        assert response.data.statuses, f"No exports executed {response.data.statuses}"
        assert response.data.statuses[0].status == 'done', 'Wrong status'

        for el in response.data.statuses:  # Iterating over the list of exports to get the profile_id # noqa: E501
            if create_profile[0] in el:
                assert el.profile_id == create_profile[0]

    # @pytest.mark.skip(reason='Skipping for now')
    def test_get_all_import_status(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        sign_in: tuple,
    ) -> None:
        """Testing receiving all profile import status

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            sign_in (tuple): Bearer token and refresh token
        """
        logger.info(f"Executing {request.node.name}")
        token, _ = sign_in  # Unpacking token and refresh_token after signing in
        r = launcher_api.get_all_import_status(token=token)
        response = launcher.ProfileImportStatusesResponse(**r)

        assert response.status.http_code == 200, f"Failed to receive the status: {r}"
        assert response.data.statuses, f"No exports executed {response.data.statuses}"
        assert response.data.statuses[0].status == 'done', 'Wrong status'

    # @pytest.mark.skip(reason='Skipping for now')
    @pytest.mark.parametrize(data.UNAUTH_ARGS, data.UNAUTH_VALS, ids=data.UNAUTH_IDS)
    def test_get_all_export_status_unauth(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        token: str,
        http_code: str,
        error_code: str,
        msg: str,
    ) -> None:
        """Testing unauthorised profile export status calls

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            token (str): parametrized value for token
            http_code (str): parametrized value for http_code
            error_code (str): parametrized value for error_code
            msg (str): parametrized value for msg
        """
        logger.info(f"Executing {request.node.name}")
        r = launcher_api.get_all_export_status(token=token)
        response = launcher.ProfileExportStatusesResponse(**r)

        assert response.status.error_code == error_code
        assert response.status.http_code == http_code
        assert response.status.message == msg

    # @pytest.mark.skip(reason='Skipping for now')
    @pytest.mark.parametrize(data.UNAUTH_ARGS, data.UNAUTH_VALS, ids=data.UNAUTH_IDS)
    def test_get_all_import_status_unauth(
        self,
        request: FixtureRequest,
        launcher_api: API.Launcher,
        token: str,
        http_code: str,
        error_code: str,
        msg: str,
    ) -> None:
        """Testing unauthorised profile import status calls

        Args:
            request (FixtureRequest): FixtureRequest
            launcher_api (API.Launcher): API.Launcher
            token (str): parametrized value for token
            http_code (str): parametrized value for http_code
            error_code (str): parametrized value for error_code
            msg (str): parametrized value for msg
        """
        logger.info(f"Executing {request.node.name}")
        r = launcher_api.get_all_import_status(token=token)
        response = launcher.ProfileImportStatusesResponse(**r)

        assert response.status.error_code == error_code
        assert response.status.http_code == http_code
        assert response.status.message == msg
