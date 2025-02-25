# import os
# from data import IMPORT_PROFILE_DATA
# from models import launcher


# import_data = IMPORT_PROFILE_DATA
# file_path = import_data['import_path'] / "83dc2b96-1f7c-4fea-bd3f-685c25760e25.zip"

# print(str(file_path))
import pathlib


path = pathlib.Path('C:\\Users\\Andrey Nguyen\\mlx\\exports\\49525321-2c5c-44a0-b32a-ae51d5.zip')

print(path.exists())