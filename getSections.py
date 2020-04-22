from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from commons import all_countries, wiki

keywords = {"author", "prevent", "clos", "pandem", "govern", "measur", "lockdown", "quarantin", "restrict", "emerg",
            "develop", "event", "timelin", "effect", "impact", "react", "respons"}


def stem_sentence(sentence):
    porter = PorterStemmer()
    token_words = word_tokenize(sentence)
    sentence = []

    for word in token_words:
        sentence.append(porter.stem(word))
        sentence.append(" ")

    return "".join(sentence)


def get_section_titles():
    titles = {}

    for c in all_countries:
        year = ("2020", "2019-20")[c == "mainland China"]
        sect = wiki.page(f'{year} coronavirus pandemic in {c}').sections

        for s in sect:
            titles[s.title] = c

    return titles


def check_for_new_section_titles(all_section_titles):
    new_sections = {}

    for c in all_countries:
        sect = wiki.page(f'2020 coronavirus pandemic in {c}').sections

        for s in sect:
            if s.title not in all_section_titles:
                new_sections[s.title] = c

    return new_sections


def update_section_titles(all_section_titles, new_sections):
    for section, country in new_sections.items():
        print(f'There is new section title: "{section}" for 2020 coronavirus pandemic in {country}')

    all_section_titles.update(set(new_sections.keys()))

    return all_section_titles


def get_relevant_section_titles(all_section_titles):
    rel_section_titles = set()
    for sect_title in all_section_titles:
        if any(word in sect_title.lower() for word in keywords):
            rel_section_titles.add(sect_title)

    return rel_section_titles


section_titles = get_section_titles()

for title in section_titles:
    stemmed_title = stem_sentence(title)
    print(f'Stemmed variant of {title}: {stemmed_title}')

# new_section_titles = check_for_new_section_titles(section_titles)
# section_titles = update_section_titles(section_titles, new_section_titles)

relevant_section_titles = get_relevant_section_titles(section_titles)

for rel_sect_title in relevant_section_titles:
    print(rel_sect_title)
