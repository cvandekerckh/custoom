from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


DRIVE_FOLDER = '16HaMGCCmVBZihVNcgQQNPZ2FJPyE29Yw'
DRIVE_URL = 'https://drive.google.com/file/d/{}'
ID_FIELD = 'id'
ALBUMS_PATH = "albums"


def initialize_drive():
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    drive = GoogleDrive(g_login)
    return drive


def upload_on_drive(drive, filename, albums_path):
    local_filename = f"{filename}.pdf"
    local_file = f"{albums_path}/{local_filename}"
    drive_file = drive.CreateFile({'title': local_filename, 'parents': [{'id': DRIVE_FOLDER}]})
    drive_file.SetContentFile(local_file)
    drive_file.Upload()
    os.remove(local_file)
    drive_id = drive_file[ID_FIELD]
    return DRIVE_URL.format(drive_id)

