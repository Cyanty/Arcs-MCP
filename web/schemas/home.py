from typing import Dict
from pydantic import BaseModel, Field


class HomePageData(BaseModel):
    result_dict: Dict[str, Dict[str, str]]
    show_confirm: bool = Field(
        default=False,
        description="Whether to display a confirmation popup"
    )
