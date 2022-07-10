class ConfigNotFound(Exception):
    """Raised when a config is not found in the database

    Attributes:
        config_name -- Name of config
    """

    def __init__(self, config_name):
        self.config_name = config_name
        self.message = f"{self.config_name!r} config not found."
        super().__init__(self.message)


class SyncProfileNotFound(Exception):
    """Raised when a sync profile is not found in the database

    Attributes:
        profile_name -- Name of profile
    """

    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.message = f"{self.profile_name!r} profile not found"
        super().__init__(self.message)


class GoogleQueryEmptyResultSet(Exception):
    """Raised when the google query returns zero results"""

    def __init__(self):
        self.message = f"Google query returned an empty result set"
        super().__init__(self.message)
