import logging

from config import ConfigManager

# Constants
CONFIG_FOLDER_PATH = "config"


logger = logging.getLogger("main")


def main():
    config = ConfigManager(CONFIG_FOLDER_PATH)
    config.load_config()
    print(config.get())
    # for key, value in config.get().items():
    #     print(f"{key}: {value}")
    print("Hello from tennis-simulator!")


if __name__ == "__main__":
    main()
