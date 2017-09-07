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
    movie_table = """
        CREATE TABLE movie (
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
            FOREIGN KEY (name) REFERENCES movie(name)
        );
    """
    cursor.execute(movie_table)
    cursor.execute(feedback_table)
    connection.commit()
    print('done!')

def insert_movies(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO movie (name, year, budget, domestic_bo, \
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
    cursor.execute('drop table if exists movie')
    cursor.execute('drop table if exists feedback')
    print('done!')
