#!/usr/bin/env python3
"""
Module for filtered logger.
"""

import logging
import re
from typing import List


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize RedactingFormatter with fields to redact.

        Args:
            fields (List[str]): List of fields to redact.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting specified fields.

        Args:
            record (logging.LogRecord): Log record to format.

        Returns:
            str: Formatted log message with specified fields redacted.
        """
        message = super().format(record)
        redacted_message = filter_datum(
            self.fields, "***", message, self.SEPARATOR)
        return redacted_message


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Replace occurrences of specified fields in a log message with redaction.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String representing the redaction for the field.
        message (str): Log line message.
        separator (str): Character separating all fields in the log line.

    Returns:
        str: Log message with specified fields obfuscated.
    """
    regex_pattern = '|'.join(fields)
    return re.sub(
        r'({})=[^{}{}]*'.format(regex_pattern, separator, separator),
        r'\1={}'.format(redaction),
        message
    )
