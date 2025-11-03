import logging
import os
import yaml
from pathlib import Path
from typing import Any, Dict, List
from pydantic import ValidationError


logger = logging.getLogger("config")


class ConfigManager:
    def __init__(self, config_folder_path):
        self._config = None
        self.config_folder_path: Path = Path(config_folder_path)
        self.config_files: List[str] = ["simulation.yml", "tennis.yml"]

    def load_config(self, merge_strategy: str = "deep") -> None:
        """Load config settings."""
        if not self.config_folder_path:
            logger.warning("No config folder. Provided a config folder.")
            return

        # Init merged config
        merged_config = {}

        for config_file in self.config_files:
            config_path = self.config_folder_path / config_file
            # Check if file exists
            if not os.path.exists(config_path):
                print(f"Warning: Config file not found: {config_path}")
                continue  # Skip to next file

            # Load YAML file if possible
            try:
                with open(config_path, "r") as file:
                    config_data = yaml.safe_load(file) or {}
                logger.info(f"Successfully loaded config file: {config_path}")

                if merge_strategy == "deep":
                    merged_config = self._deep_merge(merged_config, config_data)
                else:
                    merged_config.update(config_data)

            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML file {config_path}: {e}")

        # Ensure at least one config was loaded
        if not merged_config:
            raise ValueError("No configuration files were successfully loaded")

        # Validate with Pydantic
        try:
            self._config = merged_config
            logger.info(f"Loading configuration from {self.config_folder_path}")
        except ValidationError as e:
            logger.error(f"Configuration validation error: {e}")

    def _deep_merge(
        self, base: Dict[str, Any], update: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Recursively merge two dictionaries.

        Args:
            base (Dict[str, Any]): The base dictionary to be updated.
            update (Dict[str, Any]): The dictionary with updates to apply.
        """
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def get(self) -> Dict[str, Any]:
        """Get the loaded configuration"""
        if self._config is None:
            raise RuntimeError(
                "Configuration not loaded. Please call load_config() first."
            )
        return self._config
