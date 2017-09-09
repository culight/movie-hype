import sqlite3
import csv
import os

DB_FILE = ''

def create_file(filepath):
    global DB_FILE
    DB_FILE = filepath

def create_tables(connection):
    print('creating tables...')
    cursor = connection.cursor()
    finance_table = """
        CREATE TABLE finance (
            name  TEXT PRIMARY KEY NOT NULL,
            year INTEGER,
            budget INTEGER,
            domestic_bo INTEGER,
            international_bo INTEGER,
            genre TEXT,
            sequel INTEGER,
            duration INTEGER
        );
    """

    feedback_table = """
        CREATE TABLE feedback (
            name  TEXT PRIMARY KEY NOT NULL,
            interest REAL NOT NULL,
            FOREIGN KEY (name) REFERENCES finance(name)
        );
    """

    ratings_table = """
        CREATE TABLE ratings (
            name  TEXT PRIMARY KEY NOT NULL,
            imdbRating REAL NOT NULL,
            ratingCount INTEGER,
            year INTEGER,
            nrOfWins INTEGER,
            nrOfNominations INTEGER,
            nrOfNewsArticles INTEGER,
            nrOfUserReviews INTEGER,
            FOREIGN KEY (name) REFERENCES finance(name)
        );
    """
    cursor.execute(finance_table)
    cursor.execute(feedback_table)
    cursor.execute(ratings_table)
    connection.commit()
    print('done!')

def insert_finance_data(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO finance (name, year, budget, domestic_bo, \
            international_bo, genre, sequel, duration) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)", records)
        print('done!')
    connection.commit()

def insert_feedback(input_file, connection):
    cursor = connection.cursor()
    #print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO feedback (name, interest)\
          VALUES (?, ?)", records)
        print('done!')
    connection.commit()

def insert_ratings_data(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO ratings ('name','imdbRating','ratingCount', \
        'year','nrOfWins','nrOfNominations','nrOfNewsArticles','nrOfUserReviews') \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)", records)
        print('done!')
    connection.commit()

def run_query(query, connection):
    cursor = connection.cursor()
    print('executing query...')
    results = cursor.execute(query)
    connection.commit()
    print('done!')
    return results

def clear_tables(connection):
    cursor = connection.cursor()
    print('clearing tables...')
    cursor.execute('drop table if exists finance')
    cursor.execute('drop table if exists feedback')
    cursor.execute('drop table if exists ratings')
    print('done!')
