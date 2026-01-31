"""Shared utilities for creating YAML fixture files from MySQL database."""
import sys

from mysql.connector import connect


def parse_db_arguments():
    """Parse database connection arguments from command line.

    Returns:
        tuple: (db_host, db_port, db_user, db_password, db_database)

    Raises:
        SystemExit: If required arguments are missing or invalid.
    """
    if len(sys.argv) < 6:
        print("Error: Missing required arguments", file=sys.stderr)
        print("Usage: python3 script.py <hostname> <port> <user> <password> <database>", file=sys.stderr)
        sys.exit(1)

    db_host = sys.argv[1]
    try:
        db_port = int(sys.argv[2])
    except ValueError:
        print(f"Error: Invalid port number '{sys.argv[2]}'. Port must be a number.", file=sys.stderr)
        sys.exit(1)
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
        mysql.connector.connection.MySQLConnection: MySQL database connection object

    Raises:
        mysql.connector.Error: If the connection fails
    """
    try:
        return connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_database
        )
    except Exception as e:
        print(f"Error: Failed to connect to database: {e}", file=sys.stderr)
        sys.exit(1)
