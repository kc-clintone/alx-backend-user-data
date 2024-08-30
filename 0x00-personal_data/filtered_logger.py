#!/usr/bin/env python3
"""
Filtered data
"""


import logging
import re


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    def __init__(self, fields, redaction="***", separator=";"):
        super().__init__()
        self.fields = fields
        self.redaction = redaction
        self.separator = separator

    def format(self, record):
        message = super().format(record)
        return filter_datum(self.fields, self.redaction, message, self.separator)

def filter_datum(fields, redaction, message, separator):
    """Return the log message with fields obfuscated."""
    pattern = f"({'|'.join(fields)})=([^ {separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
