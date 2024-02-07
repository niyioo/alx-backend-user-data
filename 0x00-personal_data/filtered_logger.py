#!/usr/bin/env python3
"""
Module for filtered logger.
"""

import logging
import os
import mysql.connector
from typing import List, Tuple
import re

# Define the PII fields
PII_FIELDS: Tuple[str, str, str, str, str] = (
    "name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    FORMAT = "[HOLBERTON] user_data INFO %(asctime)-15s: %(message)s"

    def __init__(self, fields: Tuple[str, ...]):
        """
        Initialize RedactingFormatter with fields to redact.

        Args:
            fields (Tuple[str, ...]): Tuple of fields to redact.
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
        message = record.msg
        for field in self.fields:
            message = message.replace(field, "***")
        return super().format(logging.LogRecord(
            name=record.name,
            level=record.levelno,
            pathname=record.pathname,
            lineno=record.lineno,
            msg=message,
            args=record.args,
            exc_info=record.exc_info,
            func=record.funcName,
            sinfo=record.stack_info,
        ))


def get_logger() -> logging.Logger:
    """
    Create and configure a logger named "user_data".

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Create a connection to the database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=db_user,
        password=db_pwd,
        host=db_host,
        database=db_name
    )


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


def main() -> None:
    """
    Retrieve all rows from the "users" table in the database
    and log each row under a filtered format.
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        filtered_row = {
            key: "***" if key in PII_FIELDS else value
            for key, value in row.items()}
        logger.info(filtered_row)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
