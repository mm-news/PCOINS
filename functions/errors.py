"""This file contains all the custom errors used in the project."""


class HostsListError(ValueError):
    """This error is raised when the hosts list is invalid."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""
        message = "HostsListError: "+message
        super().__init__(message)


class ConfigNotFoundError(KeyError):
    """This error is raised when called config is not found."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""
        message = "ConfigNotFoundError: "+message
        super().__init__(message)


class ConfigError(ValueError):
    """This error is raised when the config file is invalid."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""
        message = "ConfigError: "+message
        super().__init__(message)


class SetupError(Exception):
    """This error is raised when setup fails."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""
        message = "SetupError: "+message
        super().__init__(message)
