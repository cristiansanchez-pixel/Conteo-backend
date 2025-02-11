from pydantic import BaseModel


class PaginatorSearch(BaseModel):
    current_page: int
    page_size: int
    filter: str
    order_by: str
    order: str