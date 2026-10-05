import sqlite3
from pathlib import Path

DB_PATH = Path("database/jobs.db")


def connect():
    return sqlite3.connect(DB_PATH)


def setup_database():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                url TEXT PRIMARY KEY,
                company TEXT,
                position TEXT,
                location TEXT,
                first_found TEXT
            )
        """)


def job_exists(url):
    with connect() as conn:
        result = conn.execute(
            "SELECT 1 FROM jobs WHERE url = ?",
            (url,)
        ).fetchone()

    return result is not None


def save_job(job, first_found):
    with connect() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO jobs
            (url, company, position, location, first_found)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                job["url"],
                job["company"],
                job["position"],
                job["location"],
                first_found
            )
        )