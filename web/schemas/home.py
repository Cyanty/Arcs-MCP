from typing import Dict
from pydantic import BaseModel


class HomePageData(BaseModel):
    result_dict: Dict[str, Dict[str, str]]
    show_confirm: bool
