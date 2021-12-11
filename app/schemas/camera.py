from pydantic import BaseModel


class CameraBase(BaseModel):
    """The base camera model."""

    on: bool
