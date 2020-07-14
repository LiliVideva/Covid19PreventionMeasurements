import get_section_titles
import map_date_sentence
import retrieve_articles
import drive_utils
import retrieve_virus_statistics
import plot


def update_page_contents():
    print("Getting pages content ......")
    pages_content = retrieve_articles.get_pages_content_as_json(all_page_titles)
    drive_utils.update_database(pages_content)


def get_information_about_country(country, relevant_section_titles):
    page_content = drive_utils.get_page_content_for_country(country)

    print("Getting data sentences ......")
    dates_sentences = map_date_sentence.get_event_by_date(page_content, relevant_section_titles)

    print("Getting virus_country_results ......")
    virus_country_results = retrieve_virus_statistics.retrieve_statistics(country)

    plotter = plot.PlotGraphics(virus_country_results, dates_sentences, country)
    plotter.plot_page_statistics()
    rt_statistics = plotter.rt_stats()

    retrieve_virus_statistics.calculate_cases_increase(dates_sentences, virus_country_results, rt_statistics)


if __name__ == '__main__':
    print("Getting relevant section title tokens ......")
    relevant_section_titles_tokens = get_section_titles.get_relevant_section_titles_tokens()
    print("Getting all section titles ......")
    all_section_titles = get_section_titles.get_all_section_titles()
    print("Getting relevant section titles ......")
    relevant_section_titles = get_section_titles.get_relevant_section_titles(all_section_titles=all_section_titles,
                                                                             relevant_tokens=relevant_section_titles_tokens)
    print(f'Relevant section titles:\n'
          f'========================\n'
          f'{relevant_section_titles}')

    print("Getting all page titles......")
    all_page_titles = retrieve_articles.get_pattern_article_titles()
    all_page_titles.extend(retrieve_articles.get_related_article_titles())

    get_information_about_country("Bulgaria", relevant_section_titles)
