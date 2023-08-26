from envparse import Env


env = Env()
env.read_envfile(".env")


class Settings:
    """class for storing environment variables"""
    
    DB_USER = env.str("DB_USER")
    DB_PASSWORD = env.str("DB_PASSWORD")
    DB_NAME = env.str("DB_NAME")
    DB_PATH = env.str("DB_PATH")

    ARCHIVE = "egrul.json.zip"
    UNPACK_FILES_COUNT = 100
    NAME_CITY = "ХАБАРОВСК"


settings = Settings()