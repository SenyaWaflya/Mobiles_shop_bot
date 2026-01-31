from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str
    SHOP_BACKEND_API_URL: str
    FILE_STORAGE_API_URL: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
