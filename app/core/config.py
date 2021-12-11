from pydantic import BaseSettings


class API(BaseSettings):
    """The API settings."""

    name: str = "Camera Socket"
    endpoint: str = "/api/v1"

    host: str = "0.0.0.0"
    port: int = 8080

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "API_"


class Global(BaseSettings):
    """The app settings."""

    api: API = API()

    youtube_stream_key: str
    stream_url: str = "rtmp://a.rtmp.youtube.com/live2"

    debug: bool = False

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"


settings = Global()
