"""
Module Overview
---------------
This module provides configuration for the logger used in the application.

The module sets up the logging configuration using the `logging.config.dictConfig` method.
It defines the loggers, handlers, and formatters to be used for logging.

The `LOGGING_CONFIG` dictionary contains the configuration settings for the logger.
It specifies the log format, log levels, log handlers, and log file location.

Structure
---------
- Imports: Necessary libraries and modules.
- Logging Configuration: Dictionary containing the logging settings.
- Logger Initialization: Setting up the logger with the configuration.

Example usage:
    import logger

    logger.module_function()

Note:
    This module should be imported and the `module_function` should be called to configure the logger.
"""

import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "[%(levelname)s] %(filename)s:%(lineno)d: %(message)s"},
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "src/logger/app.log",
            "mode": "a",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
l = logging.getLogger(__name__)  # noqa: E741
l.info("Logger initialized.")
