import sqlite3

from app.config import get_database_path
from app.models import CREATE_STUDENTS_TABLE


def get_connection() -> sqlite3.Connection:
    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(CREATE_STUDENTS_TABLE)


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)