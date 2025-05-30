"""
Utilities Package.

This package provides various utility functions and classes for the scanner
controller application. It centralizes common functionality used across
different modules.
"""

# Core functionality - import in exact order specified by the error message
from utilities.core.command_library import (
    getScannerInterface,
    readFrequency,
    readModel,
    readRSSI,
    readSMeter,
    readSquelch,
    readSWVer,
    readVolume,
    scanner_command,
    writeFrequency,
    writeSquelch,
    writeVolume,
)
from utilities.core.command_registry import build_command_table
from utilities.core.serial_utils import (
    clear_serial_buffer,
    read_response,
    send_command,
    wait_for_data,
)
from utilities.log_utils import configure_logging, get_logger
from utilities.readlineSetup import initialize_readline

# Only export specific names (instead of using __all__ = ['*'])
__all__ = [
    "configure_logging",
    "get_logger",
    "initialize_readline",
    "scanner_command",
    "getScannerInterface",
    "readVolume",
    "writeVolume",
    "readSquelch",
    "writeSquelch",
    "readFrequency",
    "writeFrequency",
    "readRSSI",
    "readSMeter",
    "readModel",
    "readSWVer",
    "build_command_table",
    "clear_serial_buffer",
    "read_response",
    "send_command",
    "wait_for_data",
]
