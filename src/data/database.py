import sqlite3
import csv
import os

DB_FILE = ""


def create_file(filepath):
    global DB_FILE
    DB_FILE = filepath


def create_tables(connection):
    print("creating tables...")
    cursor = connection.cursor()

    movie_hype_table = """
        CREATE TABLE movie_hype (
            id TEXT,
            genres TEXT,
            revenue REAL,
            popularity INTEGER,
            budget REAL,
            vote_count INTEGER,
            movie_title TEXT NOT NULL,
            vote_average REAL,
            runtime REAL,
            title_year TEXT NOT NULL,
            interest_score REAL,
            rating REAL,
            total_votes INTEGER,
            profit_margin REAL,
            PRIMARY KEY (movie_title, title_year)
        );
    """
    cursor.execute(movie_hype_table)
    connection.commit()
    print("done!")


def insert_movie_hype_data(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany(
            """
            INSERT INTO movie_hype ('id', 'genres', 'revenue', 'popularity', 'budget',
            'vote_count', 'movie_title', 'vote_average', 'runtime', 'title_year', 'interest_score',
            'rating', 'total_votes', 'profit_margin') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            records,
        )
        print("done!")
    connection.commit()


def run_query(query, connection):
    cursor = connection.cursor()
    print("executing query...")
    results = cursor.execute(query)
    connection.commit()
    print("done!")
    return results


def clear_tables(connection):
    cursor = connection.cursor()
    print("clearing tables...")
    cursor.execute("drop table if exists movie_hype")
    print("done!")
