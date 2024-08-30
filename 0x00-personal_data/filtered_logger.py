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

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """
    Filtering log data
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """
    Creating a new logger
    """
    new_logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    new_logger.setLevel(logging.INFO)
    new_logger.propagate = False
    new_logger.addHandler(stream_handler)
    return new_logger
