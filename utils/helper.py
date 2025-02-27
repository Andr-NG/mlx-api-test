import json
import utils
import logging
from models import MLX as mlx_models
from pathlib import Path
from pydantic import ValidationError


config = utils.ConfigProvider()
logger = logging.getLogger("my_logger")
HOME_DIR = Path.home()
adapter_log_path = HOME_DIR / 'mlx' / 'logs' / 'tester_a_mlx.log'


class Helper:

    # def decode_token(self, token: str) -> tuple[str, str, str]:
    #     """Decoding the token to extract user data

    #     Args:
    #         token (str): token

    #     Returns:
    #         tuple[str, str, str]: user role, workspace id, token expiration date
    #     """
    #     decoded = jwt.decode(jwt=token, options={"verify_signature": False})
    #     default_workspace_id = decoded["workspaceID"]
    #     role = decoded["workspaceRole"]
    #     exp_time = decoded["exp"]
    #     return role, default_workspace_id, exp_time

    # def verify_token(self, token: str) -> str | None:
    #     """Verify the token to either refresh it or simply return it

    #     Args:
    #         token (str): token to be validated

    #     Returns:
    #         str: updated token
    #     """
    #     provide: models.UserData = self.get_user_data()
    #     logger.info("Decoding the token to verify exp_time")
    #     role, _, exp_time = self.decode_token(token=token)
    #     self.mlx_api = API.MLX(url=config.get_url(section="MLX_API"))
    #     if datetime.fromtimestamp(exp_time) > datetime.now():
    #         logger.info("Returning the token, because it is still valid.")
    #         return token
    #     else:
    #         try:
    #             # Verifying the owner's token and updating it if necessary
    #             if role == "owner":
    #                 logger.info(f"Token is expired. Fetching a new {role} token.")
    #                 response = self.mlx_api.refresh_token(
    #                     email=provide.owner.email,
    #                     wid=provide.owner.workspace_id,
    #                     refresh_token=provide.owner.refresh_token,
    #                 )
    #                 logger.info('Receiving a new token %s', response)
    #                 parsed = SigninResponse(**response)
    #                 logger.info("Updating the owner token in the user data file.")
    #                 self.update_user_data_file(
    #                     token=parsed.data.token, refresh_token=parsed.data.refresh_token
    #                 )
    #                 logger.info("Returning the updated token.")
    #                 return parsed.data.token

    #             # Verifying the manager's token and updating it if necessary
    #             if role == "manager":
    #                 logger.info(f"Token is expired. Fetching a new {role} token.")
    #                 response = self.mlx_api.refresh_token(
    #                     email=provide.manager.email,
    #                     wid=provide.manager.workspace_id,
    #                     refresh_token=provide.manager.refresh_token,
    #                 )
    #                 logger.info('Receiving a new token %s', response)
    #                 parsed = SigninResponse(**response)
    #                 logger.info("Updating the manager token in the user data file.")
    #                 self.update_user_data_file(
    #                     token=parsed.data.token, refresh_token=parsed.data.refresh_token
    #                 )
    #                 logger.info("Returning the updated token.")
    #                 return parsed.data.token

    #             # Verifying the user's token and updating it if necessary
    #             if role == "user":
    #                 logger.info(f"Token is expired. Fetching a new {role} token.")
    #                 response = self.mlx_api.refresh_token(
    #                     email=provide.user.email,
    #                     wid=provide.user.workspace_id,
    #                     refresh_token=provide.user.refresh_token,
    #                 )
    #                 logger.info('Receiving a new token %s', response)
    #                 parsed = SigninResponse(**response)
    #                 logger.info("Updating the user token in the user data file.")
    #                 self.update_user_data_file(
    #                     token=parsed.data.token, refresh_token=parsed.data.refresh_token
    #                 )
    #                 logger.info("Returning the updated token.")
    #                 return parsed.data.token

    #             # Verifying the launcher's token and updating it if necessary
    #             if role == "launcher":
    #                 logger.info(f"Token is expired. Fetching a new {role} token.")
    #                 response = self.mlx_api.refresh_token(
    #                     email=provide.launcher.email,
    #                     wid=provide.launcher.workspace_id,
    #                     refresh_token=provide.launcher.refresh_token,
    #                 )
    #                 logger.info('Receiving a new token %s', response)
    #                 parsed = SigninResponse(**response)
    #                 logger.info("Updating the launcher token in the user data file.")
    #                 self.update_user_data_file(
    #                     token=parsed.data.token, refresh_token=parsed.data.refresh_token
    #                 )
    #                 logger.info("Returning the updated token.")
    #                 return parsed.data.token

    #         except ValidationError as e:
    #             logger.error("Validation error occurred: %s", e)
    #             raise
    #         except Exception as e:
    #             logger.error("An unexpected error occurred: %s", e)
    #             raise

    def read_logs(self) -> dict:
        """Read logs from adapter tester

        Returns:
            dict: profile data sent to browsers from adapater
        """
        log_data = []

    # Reading the adpater log file to validate
        with open(adapter_log_path, 'r') as log_file:
            for line in log_file:
                entry: dict = json.loads(line.strip())
                log_data.append(entry)
        return log_data

    def get_fingerprints_from_logs(self, profile_id: str) -> mlx_models.ReadyProfileResponse:
        """Get only fingerprints from the adapter tester by profile

        Args:
            profile_id (str): Profile ID

        Returns:
            ReadyProfileResponse: Log data parsed into the ReadyProfileResponse model
        """
        logs = self.read_logs()
        fingerprints = {}
        try:
            for log in logs:
                if 'startRequest' in log and log['startRequest']['ProfileID'] == profile_id:
                    fingerprints.update(log['fingerprint'])
                    return mlx_models.ReadyProfileResponse(**fingerprints)

        except KeyError as e:
            logger.error('KeyError occurred: %s', e)
            raise
        except ValidationError as e:
            logger.error('ValidationError occurred: %s', e)
            raise
        except Exception as e:
            logger.error('Unknown occurred: %s', e)
            raise

    def read_adapter_logs(self) -> dict:
        """Read logs from adapter tester

        Returns:
            dict: profile data sent to browsers from adapater
        """
        fingerprints = {}
        cookies = {}

    # Reading the adpater log file to validate
        with open(adapter_log_path, 'r') as log_file:
            for line in log_file:
                entry: dict = json.loads(line.strip())
                if 'fingerprint' in entry:
                    fingerprints.update(entry['fingerprint'])
                if 'params' in entry and entry['method'] == 'ImportCookies':
                    cookies.update(entry['params'])

        return fingerprints, cookies

    def read_cookies(self):
        with open('cookies.txt', 'r') as file:
            content = file.read()
        return content