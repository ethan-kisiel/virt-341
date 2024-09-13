"""
Manages the configuration of the overall application
"""

from configparser import ConfigParser


class Config:
    """
    Class representing a full app configuration
    """

    database_url: str

    is_development: bool
    ip: str
    port: int

    def __init__(
        self, is_development: bool, ip: str, port: int, database_url: str
    ) -> None:

        # wsgi settings
        self.is_development = is_development
        self.ip = ip
        self.port = port

        # database settings
        self.database_url = database_url

    @classmethod
    def default(cls):
        """Default config"""

        return cls(True, "127.0.0.1", 5000, "sqlite://persistent/app.db")


class ConfigManager:
    """
    Configuration manager
    """

    config: Config = Config.default()

    @classmethod
    def load_config(cls, filepath: str) -> None:
        """loads configuration from file

        Keyword arguments:
        filepath -- path to config file
        Return: None
        """

        try:
            config_file = ConfigParser()
            config_file.read(filepath)

            wsgi_config = config_file["wsgi"]
            database_config = config_file["database"]

            is_development = wsgi_config.getboolean("development")
            ip = wsgi_config["ip"]
            port = wsgi_config["port"]

            database_url = database_config["url"]

            cls.config = Config(is_development, ip, port, database_url)

        except FileNotFoundError:
            print("file not found")  # TODO: Replace with log
        except Exception as e:
            print(f"Exception: {e}")
