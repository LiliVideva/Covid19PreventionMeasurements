from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from commons import all_countries, wiki


def drive_login():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    return drive


def get_directory(gdrive):
    covid_dir = gdrive.ListFile({'q': "title = 'COVID-19-Reasearch'"}).GetList()[0]

    return covid_dir


def upload_files(gdrive, covid_dir):
    for c in all_countries:
        year = ("2020", "2019-20")[c == "mainland China"]
        page = wiki.page(f'{year} coronavirus pandemic in {c}')
        file_name = f'{c} - full.txt'
        file = gdrive.CreateFile({'title': file_name, 'parents': [{u'id': covid_dir['id']}]})
        # content = file.GetContentString()
        file.SetContentString(page.text)  # content + page.text
        file.Upload()
        print(f'"{file_name}" has been uploaded')


drive = drive_login()
directory = get_directory(drive)
upload_files(drive, directory)
