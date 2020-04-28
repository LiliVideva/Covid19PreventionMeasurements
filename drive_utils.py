import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def drive_login():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive


def get_directory(gdrive):
    covid_dir = gdrive.ListFile({'q': "title = 'COVID-19-Reasearch'"}).GetList()[0]
    return covid_dir


def upload_files(gdrive, covid_dir, page_contents):
    for page_title, page_content in page_contents.items():
        file = gdrive.CreateFile({'title': page_title, 'parents': [{u'id': covid_dir['id']}]})
        file.SetContentString(json.dumps(page_content))
        file.Upload()
        print(f'"{page_title}" has been uploaded')
