"""This file contains all the custom errors used in the project."""

class HostsListError(Exception):
    """This error is raised when the hosts list is invalid."""
    def __init__(self, message: str) -> None:
        """Initialize the error."""
        message = "HostsListError: "+message
        super().__init__(message)

class ConfigError(Exception):
    """This error is raised when the config file is invalid."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""
        message = "ConfigError: "+message
        super().__init__(message)

class SettingsError(Exception):
    """This error is raised when the settings file is invalid."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""
        message = "SettingsError: "+message
        super().__init__(message)

class SetupError(Exception):
    """This error is raised when setup fails."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""
        message = "SetupError: "+message
        super().__init__(message)
