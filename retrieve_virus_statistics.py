import re
from collections import OrderedDict

import demjson
import requests
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
