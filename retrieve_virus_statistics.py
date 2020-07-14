import re
from collections import OrderedDict

import demjson
import requests
import texttable
import pandas as pd
from bs4 import BeautifulSoup

from commons import all_countries


def retrieve_statistics(country):
    country_statistics = {}

    worldometer_country = all_countries[country]
    url = f"https://www.worldometers.info/coronavirus/country/{worldometer_country}/"

    try:
        html_page = requests.get(url)
    except requests.exceptions.RequestException:
        print(f'No data found for {country}')

    soup = BeautifulSoup(html_page.content, features="html.parser")

    plots_data = {}
    for match in re.finditer(r"<script type=\"text\/javascript\">\s+Highcharts\.chart\('(.*?)',\s({.*?})\);",
                             str(soup), flags=re.S):
        name, data = match.groups()
        try:
            parsed = demjson.decode(data, "utf-8")
        except demjson.JSONDecodeError:
            continue

        title = parsed["yAxis"]["title"]["text"]
        plots_data[title] = {
            "dates": parsed["xAxis"]["categories"],
            "values": [0 if x is None else x for x in parsed["series"][0]["data"]],
        }

    plots_data = OrderedDict(sorted(plots_data.items(), reverse=True))
    if not plots_data:
        print(f"No data found for {country}({worldometer_country})")
    else:
        country_statistics = dict(plots_data)

    return country_statistics


def calculate_cases_increase(dates_sentences, virus_country_results, rt_stats):
    stat_dates = virus_country_results["Total Coronavirus Cases"]["dates"]
    stat_values = virus_country_results["Total Coronavirus Cases"]["values"]
    result_data = [["Date", "Measure", "Rt", "Rt in 2 weeks", "Cases increase for 2 weeks"]]

    for date, sentence in sorted(dates_sentences.items()):
        if date in stat_dates:
            date_cases = stat_values[stat_dates.index(date)]

            checked_date = pd.to_datetime(date, errors='coerce', format="%b %d") + pd.DateOffset(days=14)
            checked_date_cases = "In the future. We will see."

            if checked_date != "NaT" and checked_date.strftime("%b %d") in stat_dates:
                checked_date_cases = stat_values[stat_dates.index(checked_date.strftime("%b %d"))]

            increase_percentage = str("{:.2f}".format((int(checked_date_cases) - int(date_cases))/14))
            result_data.append([date, sentence, rt_stats.get(date), rt_stats.get(checked_date.strftime("%b %d")), increase_percentage + "%"])

    result_table = texttable.Texttable()
    result_table.set_cols_align(["c", "l", "c", "c", "c"])
    result_table.set_cols_valign(["m", "t", "m", "m", "m"])
    result_table.set_cols_width([15, 120, 10, 25, 25])
    result_table.add_rows(result_data)

    print(result_table.draw())
