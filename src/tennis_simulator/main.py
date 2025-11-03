import logging

from config.read import ConfigManager


# Constants
CONFIG_FOLDER_PATH = "config"


logger = logging.getLogger("main")


def main():
    config = ConfigManager(CONFIG_FOLDER_PATH)
    config.load_config()
    print(config.get())
    print("Hello from tennis-simulator!")


if __name__ == "__main__":
    main()
