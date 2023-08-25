from envparse import Env


env = Env()
env.read_envfile("../.env")


class Settings:
    archive = "egrul.json.zip"
    unpack_files = 100


settings = Settings()