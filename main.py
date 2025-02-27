
from models.MLX.ready_profile_response import ReadyProfileResponse
from utils import Helper

helper = Helper()
logs = helper.read_logs()
finger: ReadyProfileResponse = helper.get_fingerprints_from_logs('39a258f4-b840-4c8e-9749-b6bd7cfe4210')
print(finger.data.core.proxy.host)