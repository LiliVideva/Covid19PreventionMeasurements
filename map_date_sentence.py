from word2number import w2n
import re

import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


def get_event_by_date(page_contents, relevant_section_titles):
    pages_date_sentences = {}

    for page_title, page_content in page_contents.items():
        date_sentence = {}
        page_relevant_sections = [key for key in page_content.keys() if key in relevant_section_titles]
        for section in page_relevant_sections:
            current_date = ""
            for line in page_content[section]:
                doc = nlp(line)
                # if len(doc.ents) > 0:
                #     displacy.serve(doc, style='ent')
                date_entities = [entity for entity in doc.ents if entity.label_ == "DATE"]
                for d_entity in date_entities:
                    sentence = doc[doc[d_entity.start].sent.start].sent
                    if d_entity.text in sentence.text and d_entity.text != sentence.text:
                        new_date, current_date = reformat_date(d_entity.text, current_date)
                        if new_date == "":
                            continue
                        sent_content = date_sentence.get(new_date)
                        if sent_content:
                            s = f'{sent_content}\n'

                            if sentence.text in sent_content:
                                continue
                        else:
                            s = ""
                        date_sentence[new_date] = s + sentence.text

        pages_date_sentences[page_title] = date_sentence
    return pages_date_sentences


def reformat_date(dt, current_date):
    try:
        changed_date = pd.to_datetime(dt + " 2020").strftime("%b %d")
        return changed_date, changed_date
    except ValueError:
        decoded_date, new_current_date = resolve_date(dt, current_date)
        # if dt != decoded_date:
        #     print(f'current date: {current_date}')
        #     print(f'raw date: {dt}')
        #     print(f'decoded date: {decoded_date}')
        return decoded_date, new_current_date


def resolve_date(dt, current_date):
    if len(current_date) == 0:
        return dt, current_date

    recalculated_date = ""
    date_pattern = "([0-2]?[0-9])|(3[0-1])"
    month_pattern = "((Jan|Febr)uary|March|April|May|June|July|August|(Octo|(Sept|Nov|Dec)em)ber)"

    date_month_pattern = re.match(f".*(on|the|as of|the end of) ({date_pattern}) {month_pattern}", dt, re.IGNORECASE)
    month_date_pattern = re.match(f".*(on|late)?\\s*{month_pattern} ({date_pattern})$", dt, re.IGNORECASE)

    yesterday_pattern = re.match("^((the end of )?(the )?(previous|last) day|"
                                 "(a|the) day (ago|before|earlier)|yesterday).*", dt)
    today_pattern = re.match("^(((earl(y|ier)|later)?\\s*(the|this|that)\\s*(same )?(day|date)|today).*)", dt, re.IGNORECASE)
    tomorrow_pattern = re.match("^((the end of )?(the )?(following|next) day|"
                                "(less than )?(a|one) day later|tomorrow).*", dt, re.IGNORECASE)

    past_pattern = re.match(f"^(just )*({date_pattern}|[a-z]*) days (ago|before|earlier).*", dt, re.IGNORECASE)
    future_pattern = re.match(f"^(just )*({date_pattern}|[a-z]*) days later.*", dt, re.IGNORECASE)

    if date_month_pattern:
        d = re.search(f'({date_pattern}) {month_pattern}', date_month_pattern.group(0)).group(0)
        recalculated_date = pd.to_datetime(d + " 2020")
        current_date = pd.to_datetime(recalculated_date).strftime("%b %d")
    elif month_date_pattern:
        d = re.search(f'{month_pattern} ({date_pattern})', month_date_pattern.group(0)).group(0)
        recalculated_date = pd.to_datetime(d + " 2020")
        current_date = pd.to_datetime(recalculated_date).strftime("%b %d")
    elif yesterday_pattern:
        recalculated_date = pd.to_datetime(current_date, errors='coerce', format="%b %d") - pd.DateOffset(days=1)
    elif today_pattern:
        recalculated_date = pd.to_datetime(current_date + " 2020")
    elif tomorrow_pattern:
        recalculated_date = pd.to_datetime(current_date, errors='coerce', format="%b %d") + pd.DateOffset(days=1)
    elif past_pattern:
        try:
            number = extract_number_from_string(past_pattern)
        except ValueError:
            return dt, current_date
        recalculated_date = pd.to_datetime(current_date, errors='coerce', format="%b %d") - pd.DateOffset(days=number)
    elif future_pattern:
        try:
            number = extract_number_from_string(future_pattern)
        except ValueError:
            return dt, current_date
        recalculated_date = pd.to_datetime(current_date, errors='coerce', format="%b %d") + pd.DateOffset(days=number)

    if recalculated_date == "":
        new_date = ""
    else:
        new_date = pd.to_datetime(recalculated_date).strftime("%b %d")

    return new_date, current_date


def extract_number_from_string(pattern):
    number_pattern = re.search('(\\S+?) days', pattern.group(0))

    return w2n.word_to_num(number_pattern.group(1))
