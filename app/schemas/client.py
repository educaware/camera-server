from typing import Optional

from pydantic import BaseModel


class ClientBase(BaseModel):
    """The base client model."""

    host: str
    port: Optional[int]
