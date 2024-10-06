from __future__ import annotations

import toml
from typing import cast
from types_.config import Config


def load_config(file_path: str) -> Config:
    try:
        with open(file_path, "r") as fp: 
            return cast(Config, toml.load(fp))
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file {file_path} not found.")
    except toml.TomlDecodeError:
        raise RuntimeError(f"Error decoding TOML file {file_path}.")


CONFIG: Config = load_config("config.toml")
