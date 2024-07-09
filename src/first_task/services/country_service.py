from typing import List
from models.country_info import CountryInfo
from repositories.country_repository import CountryRepository


class CountryService:
    def __init__(self, repository: CountryRepository):
        self.repository = repository

    def get_country_data(self) -> List[CountryInfo]:
        return self.repository.fetch_data()
