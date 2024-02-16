from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    url_services: str = ""
    url_devices: str = ""
    uisp_url: str = ""
    x_auth_token: str = ""

    model_config = SettingsConfigDict(env_file=".env")
