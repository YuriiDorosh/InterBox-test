from pydantic import BaseModel
from typing import Union


class Product(BaseModel):
    url: str
    name: str
    price: float
    main_img_url: str
    second_img_url: str
    seller: str
    seller_link: str
    seller_joined_at: str
    seller_items_sold: float
    shipping_price: Union[float, str]
    returns_day: int
