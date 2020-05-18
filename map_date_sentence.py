import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


def get_event_by_date(page_contents, relevant_section_titles):
    date_sentences = {}

    for page_title, page_content in page_contents.items():
        page_relevant_sections = [key for key in page_content.keys() if key in relevant_section_titles]

        for section in page_relevant_sections:
            for line in page_content[section]:
                doc = nlp(line)
                # if len(doc.ents) > 0:
                #     displacy.serve(doc, style='ent')
                dates = [entity.text for entity in doc.ents if entity.label_ == "DATE"]
                for sent in doc.sents:
                    for d in dates:
                        if d in sent.text:
                            date_sentences[reformat_date(d)] = sent.text
            # print(f'{section}:\n'
            #       f'========================\n')
            # for key, value in date_sentences.items():
            #     print(f'"{key}" - "{value}"')
    return date_sentences


def reformat_date(dt):
    try:
        return pd.to_datetime(dt + " 2020").strftime("%b %d")
    except ValueError:
        return dt
