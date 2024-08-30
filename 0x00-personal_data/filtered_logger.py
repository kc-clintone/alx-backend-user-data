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


def filter_datum(fields, redaction, message, separator):
    """
    This function filters data
    """

    pattern = f"({'|'.join(fields)})=([^ {separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
