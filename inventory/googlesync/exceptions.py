class ConfigNotFound(Exception):
    """Raised when a config is not found in the database

    Attributes:
        config_name -- Name of config
    """

    def __init__(self, config_name):
        self.config_name = config_name
        self.message = f"{self.config_name} config not found."
