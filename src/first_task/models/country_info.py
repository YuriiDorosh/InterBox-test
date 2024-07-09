from pydantic import BaseModel

class CountryInfo(BaseModel):
    name: str
    capital: str
    flag_url: str
