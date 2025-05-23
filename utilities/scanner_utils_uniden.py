"""Utility functions for interacting with Uniden-style scanners.

This module provides utility functions for interacting with Uniden-style
scanners and other compatible devices via serial communication. It includes
functionality for detecting connected scanners, sending commands, reading
responses, and managing serial port buffers. The module is designed to work
with devices that communicate using specific command protocols, such as Uniden
scanners and AOR-DV1 scanners.

Key Features:
- Automatically detects connected scanners by scanning available COM ports and
  identifying devices based on their responses to specific commands.
- Supports Uniden-style scanners that respond to the "MDL" command with a model
  code and AOR-DV1 scanners that respond to the "WI" command with "AR-DV1".
- Provides helper functions for clearing serial buffers, sending commands, and
  reading responses with configurable timeouts.
- Includes functionality to wait for incoming data on the serial port within a
  specified time frame.

Dependencies:
- `pyserial`: Used for serial communication and port scanning.
- `re`: Used for regular expression matching to identify scanner responses.
- `logging`: Used for logging debug information to a file.

Usage:
This module is intended to be used as part of a larger application for
controlling and interacting with scanners. It can be imported and its functions
called to perform tasks such as detecting connected scanners, sending commands,
and reading responses.

Example:
Scanner Utils Uniden module.

This module provides functionality related to scanner utils uniden.
"""

import re
import time

import serial
from serial.tools import list_ports

# Import centralized logging utilities
from utilities.log_utils import get_logger

# Get a logger for this module
logger = get_logger(__name__)


def clear_serial_buffer(ser):
    """
    Clear accumulated data in the serial buffer.

    This function clears the serial input and output buffers before sending
    commands.
    """
    ser.reset_input_buffer()
    ser.reset_output_buffer()


def read_response(ser, timeout=1.0):
    """
    Read bytes from the serial port until a carriage return.

    Reads a response from the serial port with a timeout.
    """
    ser.timeout = timeout
    response = ser.read_until(b"\r").decode("utf-8").strip()
    return response


def send_command(ser, cmd):
    """
    Clear the buffer and send a command (with CR termination) to a scanner.

    This function sends a command to the serial port and returns the response.
    """
    ser.write(f"{cmd}\r".encode("utf-8"))
    return read_response(ser)


def find_scanner_port(baudrate=115200, timeout=0.5, max_retries=2):
    """
    Scan all COM ports and return a list of tuples.

    - If the scanner responds to "MDL" with "MDL,[A-Za-z0-9,]+", it is treated
    as a Uniden-style scanner.
    - If the scanner responds to "WI" with "AR-DV1", it is treated as an AOR-DV1
    scanner.
    """
    detected = []
    retries = 0
    mdl_pattern = re.compile(r"^MDL,([A-Za-z0-9,]+)$")
    while retries < max_retries:
        ports = list_ports.comports()
        for port in ports:
            try:
                with serial.Serial(
                    port.device, baudrate, timeout=timeout
                ) as ser:
                    # Check for Uniden-style scanners
                    logger.info(f"Trying port: {port.device}")
                    logger.info(f"Port description: {port.description}")
                    ser.write(b"MDL\r")
                    response = read_response(ser)
                    logger.info(f"Response from {port.device}: {response}")
                    if mdl_pattern.match(response):
                        model_code = mdl_pattern.match(response).group(1)
                        detected.append((port.device, model_code, "uniden"))
                        continue

                    # Check for AOR-DV1 scanners
                    ser.write(b"WI\r")
                    response = read_response(ser)
                    logger.info(f"Response from {port.device}: {response}")
                    if response.strip() == "AR-DV1":
                        detected.append((port.device, "AR-DV1", "aordv1"))
            except Exception as e:
                logger.warning(f"Error checking port {port.device}: {e}")
                continue

        if detected:
            return detected

        retries += 1
        logger.info("No scanners found. Retrying in 3 seconds...")
        time.sleep(3)

    logger.error("No scanners found after maximum retries.")
    return detected


def wait_for_data(ser, max_wait=0.3):
    """
    Wait up to max_wait seconds for incoming data on the serial port.

    Return True if data is available, otherwise False.
    """
    start = time.time()
    while time.time() - start < max_wait:
        if ser.in_waiting:
            return True
        time.sleep(0.01)
    return False
