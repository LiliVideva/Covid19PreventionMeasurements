import get_section_titles
import map_date_sentence
import retrieve_articles
import drive_utils

if __name__ == '__main__':
    relevant_section_titles_tokens = get_section_titles.get_relevant_section_titles_tokens()
    all_section_titles = get_section_titles.get_all_section_titles()
    relevant_section_titles = get_section_titles.get_relevant_section_titles(all_section_titles=all_section_titles, relevant_tokens=relevant_section_titles_tokens)
    print(f'Relevant section titles:\n'
          f'========================\n'
          f'{relevant_section_titles}')

    all_page_titles = retrieve_articles.get_pattern_article_titles()
    all_page_titles.extend(retrieve_articles.get_related_article_titles())
    pages_content = retrieve_articles.get_pages_content_as_json(all_page_titles)
    print(len(pages_content))

    drive = drive_utils.drive_login()
    drive_dir = drive_utils.get_directory(drive)
    drive_utils.upload_files(drive, drive_dir, pages_content)

    dates_sentences = map_date_sentence.get_event_by_date(pages_content, relevant_section_titles)
