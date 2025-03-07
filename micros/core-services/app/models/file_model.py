from pydantic import BaseModel
from typing import Optional


class FileModel(BaseModel):
    file_name: Optional[str]