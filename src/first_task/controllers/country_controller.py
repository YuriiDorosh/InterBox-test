from services.country_service import CountryService
from prettytable import PrettyTable


class CountryController:
    def __init__(self, service: CountryService):
        self.service = service

    def display_data(self) -> None:
        countries = self.service.get_country_data()
        table = PrettyTable()
        table.field_names = ["Country Name", "Capital", "Flag URL"]

        for country in countries:
            table.add_row([country.name, country.capital, country.flag_url])

        print(table)
