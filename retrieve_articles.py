import wikipedia
import wikipediaapi

import commons


def get_related_article_titles():
    related_key_phrases = {"measure", "impact", "related to", "pandemic on"}
    related_page_titles = set()

    all_page_titles = wikipedia.search("2019-20 coronavirus pandemic", 1000)

    for title in all_page_titles:
        if any(phrase in title.lower() for phrase in related_key_phrases):
            related_page_titles.add(title)

    return related_page_titles


def get_pattern_article_titles():
    titles = []
    for c in commons.all_countries:
        # year = ("2020", "2019-20")[c == "mainland China"]
        year = "2019-20" if c == "mainland China" else "2020"
        titles.append(f'{year} coronavirus pandemic in {c}')
    return titles


def get_pages_content_as_json(page_titles):
    page_on_sections = {}
    wiki = wikipediaapi.Wikipedia()
    for page_title in page_titles:
        page = wiki.page(page_title)
        page_content = {}
        for s in page.sections:
            page_content[s.title] = [t for t in s.full_text().split('\n') if t][1:]
        page_on_sections[page_title] = page_content

    return page_on_sections


def print_sections(sections, level=0):
    for s in sections:
        print("%s: %s" % ("*" * (level + 1), s.title))
        print_sections(s.sections, level + 1)
