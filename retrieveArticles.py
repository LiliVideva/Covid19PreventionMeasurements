import wikipedia
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


def get_related_articles():
    related_key_phrases = {"measure", "impact", "related to", "pandemic on"}
    related_page_titles = set()

    all_page_titles = wikipedia.search("2019-20 coronavirus pandemic", 1000)

    for title in all_page_titles:
        if any(phrase in title.lower() for phrase in related_key_phrases):
            related_page_titles.add(title)

    return related_page_titles


def upload_files(gdrive, covid_dir, page_title):
    page = wiki.page(page_title)
    file_name = f'{page_title} - full.txt'
    file = gdrive.CreateFile({'title': file_name, 'parents': [{u'id': covid_dir['id']}]})
    # content = file.GetContentString()
    file.SetContentString(page.text)  # content + page.text
    file.Upload()
    print(f'"{file_name}" has been uploaded')


drive = drive_login()
directory = get_directory(drive)

for c in all_countries:
    year = ("2020", "2019-20")[c == "mainland China"]
    upload_files(drive, directory, f'{year} coronavirus pandemic in {c}')

additional_articles = get_related_articles()
# for article in additional_articles:
#     upload_files(drive, directory, article)
