from pydantic import BaseModel
from typing import Optional


class PaginatorSearch(BaseModel):

    filter: Optional[str] = None
    order_by: Optional[str] = None
    order: Optional[str] = None
    # current_page: int
    # page_size: int