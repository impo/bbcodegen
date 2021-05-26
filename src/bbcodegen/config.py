import configparser
import logging
from pathlib import Path


def load_config():
    config = configparser.ConfigParser()
    config_file = Path.home() / ".config" / "bbcodegen" / "config.ini"
    if config_file.exists() and config_file.is_file():
        config.read(config_file)
    else:
        logging.warning("Config file not found! Creating directory to config file.")
        config_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        config["tmdb"]["api_key"]
    except KeyError:
        tmdb_api_key = input("TMDB API Key not found! Please input API Key: ")
        config["tmdb"] = {"api_key": tmdb_api_key}

    try:
        config["ptpimg"]["api_key"]
    except KeyError:
        tmdb_api_key = input("ptpimg API Key not found! Please input API Key: ")
        config["ptpimg"] = {"api_key": tmdb_api_key}

    with open(config_file, "w") as config_file_buffer:
        config.write(config_file_buffer)

    return config
