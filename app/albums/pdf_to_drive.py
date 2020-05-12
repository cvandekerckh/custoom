from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)


file1 = drive.CreateFile({'title': 'planche_out.pdf', 'parents': [{'id': '16HaMGCCmVBZihVNcgQQNPZ2FJPyE29Yw'}]})
file1.SetContentFile("planche_out.pdf")
file1.Upload()

