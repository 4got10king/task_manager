from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_prefix="BACKEND_SERVER__",
    )
    PORT: int
    HOST: str
    WORKERS: int
    SECRET_KEY: str
    METHODS: List[str]
    HEADERS: List[str]
    origins: List[str] = ["*"]
    @property
    def app_settings(self):
        return self

    @property
    def swagger_conf(self) -> dict:
        return dict(
            version="0.0.1",
            description="TASK MANAGER REST API",
            title="task_manager",
            docs_url="/swagger",
            openapi_url="/api/openapi.json",
        )

    @computed_field(return_type=str)
    @property
    def server_url(self) -> str:
        return f"http://{self.PORT}:{self.PORT}"


app_config = AppSettings()