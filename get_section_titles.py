from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import wikipediaapi
from commons import all_countries


def get_relevant_section_titles_tokens():
    with open("stemmed_keywords_for_relevant_section_titles.txt", "r") as input_file:
        res = input_file.readlines()
    return [x.strip() for x in res]


def stem_sentence(sentence):
    porter = PorterStemmer()
    token_words = word_tokenize(sentence)
    sentence = []

    for word in token_words:
        sentence.append(porter.stem(word))

    return " ".join(sentence)


def get_all_section_titles():
    titles = {}
    wiki = wikipediaapi.Wikipedia()
    for c in all_countries.keys():
        year = "2019-20" if c == "mainland China" else "2020"
        sect = wiki.page(f'{year} coronavirus pandemic in {c}').sections

        for s in sect:
            titles[s.title] = c
    print('\n')
    return titles


def check_for_new_section_titles(all_section_titles):
    new_section_titles = []
    wiki = wikipediaapi.Wikipedia()
    for c in all_countries.keys():
        sect = wiki.page(f'2020 coronavirus pandemic in {c}').sections

        for s in sect:
            if s.title not in all_section_titles:
                new_section_titles.append(s.title)

    return new_section_titles


def update_section_titles(all_section_titles, new_sections):
    for section, country in new_sections.items():
        print(f'There is new section title: "{section}" for 2020 coronavirus pandemic in {country}')

    all_section_titles.update(set(new_sections.keys()))

    return all_section_titles


def get_relevant_section_titles(all_section_titles, relevant_tokens):
    rel_section_titles = set()
    for sect_title in all_section_titles:
        if any(word in sect_title.lower() for word in relevant_tokens):
            rel_section_titles.add(sect_title)

    return rel_section_titles
