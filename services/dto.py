from pydantic import BaseModel
from typing import Optional, Union

class RegionDTO(BaseModel):
    name: str
    polygon: list[list[float]]
