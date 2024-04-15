import os
from typing import Any, Dict

import yaml
from pydantic import BaseSettings


class Settings(BaseSettings):
    # app_name: str = "ON-Limited"
    # admin_email: "on-limited@email.com"
    # items_per_user: int = 50

    user_name: str
    password: str
    host_name: str
    port_number: str
    db_name: str
    jwt_secret: str
    algorithm: str
    access_token_expire_minutes: int
    email_host: str
    email_from: str
    email_port: int
    email_username: str
    email_password: str
    email_server: str
    suppress_send: int
    api_URI: str
    frontend_URI: str


def load_settings_yaml(secret_file_path: str):
    assert os.path.isfile(secret_file_path), f"settings path {secret_file_path} does not exist.."
    with open(secret_file_path, "r+") as secret_txt:
        settings_dict: Dict[str, Any] = yaml.safe_load(secret_txt)
    return Settings(**settings_dict)


def load_settings_env():

    settings_dict: Dict[str, Any] = {
        "user_name": os.environ.get("USER_NAME"),
        "password": os.environ.get("PASSWORD"),
        "host_name": os.environ.get("HOST_NAME"),
        "port_number": os.environ.get("PORT_NUMBER"),
        "db_name": os.environ.get("DB_NAME"),
        "jwt_secret": os.environ.get("JWT_SECRET"),
        "algorithm": os.environ.get("ALGORITHM"),
        "access_token_expire_minutes": os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
        "email_host": os.environ.get("EMAIL_HOST"),
        "email_from": os.environ.get("EMAIL_FROM"),
        "email_username": os.environ.get("EMAIL_USERNAME"),
        "email_password": os.environ.get("EMAIL_PASSWORD"),
        "email_port": os.environ.get("EMAIL_PORT"),
        "email_server": os.environ.get("EMAL_SERVER"),
        "suppress_send": os.environ.get("SUPPRESS_SEND"),
        "api_URI": os.environ.get("API_URI"),
        "frontend_URI": os.environ.get("FRONTEND_URI"),

    }
    return Settings(**settings_dict)


settings = load_settings_env()
