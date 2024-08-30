#!/usr/bin/env python3
"""
Filtered data 
"""


import re

def filter_datum(fields, redaction, message, separator):
    """
    This function filters data
    """

    pattern = f"({'|'.join(fields)})=([^ {separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
