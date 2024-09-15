import os
from config import MEDIA_ROOT

async def create_dir(profile_id, filename):
    # this is neseccary for django admin as it adds media dir itself so to save
    # we should pass just the path after media
    file_dir_for_django = f"/profile_images/{profile_id}/"
    file_directory = f"{MEDIA_ROOT}{file_dir_for_django}"
    try:
        os.makedirs(file_directory)
        file_full_path = file_directory + filename
    except FileExistsError:
        file_full_path = file_directory + filename
    return {
        'file_dir': file_dir_for_django,
        'file_full_path': file_full_path}