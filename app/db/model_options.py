from pydantic import BaseModel
from typing import Any

class ModelOptions(BaseModel):
    db : Any
