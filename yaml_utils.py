"""Shared utilities for creating YAML fixture files from MySQL database."""
import sys

from mysql.connector import connect


def parse_db_arguments():
    """Parse database connection arguments from command line.

    Returns:
        tuple: (db_host, db_port, db_user, db_password, db_database)

    Raises:
        SystemExit: If required arguments are missing.
    """
    if len(sys.argv) < 6:
        print("Error: Missing required arguments", file=sys.stderr)
        print("Usage: python3 script.py <hostname> <port> <user> <password> <database>", file=sys.stderr)
        sys.exit(1)

    db_host = sys.argv[1]
    db_port = int(sys.argv[2])
    db_user = sys.argv[3]
    db_password = sys.argv[4]
    db_database = sys.argv[5]

    return db_host, db_port, db_user, db_password, db_database


def create_db_connection(db_host, db_port, db_user, db_password, db_database):
    """Create a connection to MySQL database.

    Args:
        db_host: Database hostname
        db_port: Database port number
        db_user: Database username
        db_password: Database password
        db_database: Database name

    Returns:
        Connection object
    """
    return connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_database
    )


def format_yaml_field(key, value):
    """Format a single YAML field.

    Args:
        key: Field name
        value: Field value

    Returns:
        str: Formatted YAML field string
    """
    return f"    {key}: {value}\n"


def format_yaml_entry(model_name, pk, fields_dict):
    """Format a complete YAML entry.

    Args:
        model_name: Django model name (e.g., "moneybook.Data")
        pk: Primary key value
        fields_dict: Dictionary of field names to values

    Returns:
        str: Formatted YAML entry string
    """
    result = f"- model: {model_name}\n"
    result += f"  pk: {pk}\n"
    result += "  fields:\n"
    for key, value in fields_dict.items():
        result += format_yaml_field(key, value)
    return result
