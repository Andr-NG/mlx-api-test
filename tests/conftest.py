# flake8: noqa
import pytest
import logging
import API
import utils
import os
import hashlib
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


@pytest.fixture(scope='session')
def sign_in(mlx_api: API.MLX) -> tuple[str, str]:
    """Sign in

    Args:
        mlx_api (API.MLX): MLX API

    Returns:
        tuple[str, str]: token and refresh token
    """
    email = os.getenv("EMAIL")
    hashed_pass = hashlib.md5(os.getenv("PASSWORD").encode()).hexdigest()
    response: mlx_models.SigninResponse = mlx_api.sign_in(
            login=email, password=hashed_pass
        )
    token = response.data.token
    refresh_token = response.data.refresh_token
    return token, refresh_token

@pytest.fixture(scope='session')
def get_folder_id(mlx_api: API.MLX):
    response = mlx_api.get_folder_id()    