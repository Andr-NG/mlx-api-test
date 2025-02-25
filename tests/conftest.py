# flake8: noqa
import time
import pytest
import logging
import websocket
import API
import utils
import os
import data
import hashlib
from typing import List
from pydantic import ValidationError
from models import MLX as mlx_models
from models import launcher

# Create a logger with a name specific to your project
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Create a handler and a formatter (console/file handler as needed)
handler = logging.FileHandler(filename="my_logs.log", mode="w")
formatter = logging.Formatter(
    fmt="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]",
    datefmt="%d/%m/%Y %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Avoid duplicating logs
logger.propagate = False

@pytest.fixture(scope='session')
def config() -> utils.ConfigProvider:
    """Setting up a config provider

    Returns:
        utils.ConfigProvider: ConfigProvider class
    """
    return utils.ConfigProvider()


@pytest.fixture(scope='session')
def mlx_api(config: utils.ConfigProvider) -> API.MLX:
    logger.info("MLX API instantiated")
    URL = config.get_url()
    return API.MLX(url=URL)


@pytest.fixture(scope='session')
def launcher_api(config: utils.ConfigProvider) -> API.Launcher:
    logger.info("Launcher API instantiated")
    URL = config.get_launcher_url()
    return API.Launcher(url=URL)


@pytest.fixture(scope='module')
def sign_in(mlx_api: API.MLX) -> tuple[str, str]:
    """Sign in

    Args:
        mlx_api (API.MLX): MLX API

    Returns:
        tuple[str, str]: token and refresh token
    """
    email = os.getenv("EMAIL")
    hashed_pass = hashlib.md5(os.getenv("PASSWORD").encode()).hexdigest()
    try:
        data = mlx_api.sign_in(
                login=email, password=hashed_pass
            )
        response = mlx_models.SigninResponse(**data)
        token = response.data.token
        refresh_token = response.data.refresh_token
        return token, refresh_token

    except ValidationError as e:
        logger.error('Validation Error occurred: %s', e)
    
    except Exception as e:
        logger.error('Unknown Error occurred: %s', e)


@pytest.fixture(scope='module')
def create_profile(mlx_api: API.MLX, sign_in: tuple, get_folder_id: str) -> List[str]:
    try:
        body = data.PROFILE_GENERIC
        logger.info("Adding folder_id to the body request")
        body.update({"folder_id": get_folder_id})
        token, _ = sign_in
        response = mlx_api.create_profile(profile_params=body, token=token)

        parsed = mlx_models.ArrayOfIDsResponse(**response)
        profile_list: List[str] = parsed.data.ids
        return profile_list

    except ValidationError as e:
        logger.error('Validation Error occurred: %s', e)
    
    except Exception as e:
        logger.error('Unknown Error occurred: %s', e)

@pytest.fixture(scope='module')
def get_folder_id(mlx_api: API.MLX, sign_in: tuple) -> str | None:
    token, _ = sign_in
    try:
        folder_name = 'Default folder'
        response = mlx_api.get_folder_id(token=token)
        parsed = mlx_models.UserFolderArrayResponse(**response)
        for folder in parsed.data.folders:
            if folder.name == folder_name:
                return folder.folder_id

    except ValidationError as e:
        logger.error('Validation Error occurred: %s', e)
    
    except Exception as e:
        logger.error('Unknown Error occurred: %s', e)


@pytest.fixture(scope='module')
def connect_ws():
    RETRIES = 3
    DELAY = 2
    URI = "wss://launcher.mlx.yt:45003/ws/data"
 
    for attempt in range(1, RETRIES + 1):
        try:
            logger.info(f"Attempt {attempt} to set up websocket connection")
            ws = websocket.WebSocket()
            ws.connect(url=URI)

            assert ws.connected, "Connection failed"
            logger.info("Connection successfull!")
            yield ws
            logger.info("Shutting down connection")
            ws.close()
            break

        except websocket.WebSocketException as e:
            logger.error(f"Connection attempt {attempt} failed: {e}")
            if attempt < RETRIES:
                logger.info("Attempting to connect again")
                time.sleep(DELAY)
            else:
                pytest.fail("Failed to connect to WebSocket after multiple retries")

            assert ws.connected, "Connection failed"
            logger.info("Connection successfull!")
            yield ws
            logger.info("Shutting down connection")
            ws.close()
            break

        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            raise