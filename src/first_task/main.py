import sys
from typing import List
from prettytable import PrettyTable
from services import CountryAPI
from models import CountryInfo
from settings import USE_CACHE

def display_data(countries: List[CountryInfo]) -> None:
    table = PrettyTable()
    table.field_names = ["Country Name", "Capital", "Flag URL"]

    for country in countries:
        table.add_row([country.name, country.capital, country.flag_url])

    print(table)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--no-cache':
        USE_CACHE = False

    api = CountryAPI()
    country_data = api.fetch_data()
    display_data(country_data)
