# settings/config_manager.py
import os
import json
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "app_settings.json"
)


@dataclass
class ApplicationConfig:
    visited: bool
    census_api_key: str
    data_path: str


class ConfigurationManager:
    _instance = None
    _config: Dict[str, Any] = {}
    settings: ApplicationConfig = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            pass
            with open(CONFIG_PATH, "r") as f:
                self._config = json.load(f)
        else:
            self._config = {
                "visited": False,
                "census_api_key": "Please set your API key",
                "data_path": "please set your data path to save the data",
            }
            print("Config file not found. Creating a new one.")
            with open(CONFIG_PATH, "w") as f:
                json.dump(self._config, f, indent=4)

        with open(CONFIG_PATH, "r") as file:
            self._config = json.load(file)

        self.settings = ApplicationConfig(**self._config)

    def save_config(self, new_config: Dict[str, Any]):
        new_config['visited'] = True
        with open(CONFIG_PATH, "w") as f:
            json.dump(new_config, f, indent=4)
        self.load_config()
