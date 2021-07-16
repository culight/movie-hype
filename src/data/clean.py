import csv
import os
from datetime import datetime as dt
import json


def clean_imdb_data(data_dir):
    read_file = os.path.join(data_dir, "interim/tmdb_data.csv")
    write_file = os.path.join(data_dir, "processed/tmdb_data.csv")

    if not os.path.exists(read_file):
        print("csv file not found")
        return

    headers = []
    cleaned_data = []
    cleaned_names = []

    with open(read_file, "r") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        headers.remove("release_date")
        headers.append("title_year")
        for row in reader:
            # clean the movie name
            cleaned_name = "".join(
                e for e in row["movie_title"] if e.isalnum() or e.isspace()
            ).lower()
            row.pop("movie_title")
            if cleaned_name not in cleaned_names:
                cleaned_names.append(cleaned_name)
                row["movie_title"] = cleaned_name
            else:
                # this movie name already exists... skip
                continue

            # convert date to year
            if row["release_date"]:
                row["title_year"] = dt.strptime(row["release_date"], "%m/%d/%y").year
                row.pop("release_date")
            else:
                continue

            # extract genres from json string
            if row["genres"]:
                genre_json = json.loads(row["genres"])
                genres = "|".join([g["name"] for g in genre_json])
                row["genres"] = genres
            else:
                continue

            # remove entries with missing financial data
            if row["budget"] == "0" or row["revenue"] == "0":
                continue

            # add the updated row
            cleaned_data.append(row)

    with open(write_file, "wb") as w:
        writer = csv.DictWriter(w, headers)
        writer.writeheader()
        for row in cleaned_data:
            writer.writerow(row)


def clean_additional_data(data_dir):
    read_file = os.path.join(data_dir, "interim/additional_data.csv")
    write_file = os.path.join(data_dir, "processed/additional_data.csv")

    if not os.path.exists(read_file):
        print("csv file not found")
        return

    cleaned_data = []
    cleaned_names = []

    with open(read_file, "r") as r:
        reader = csv.DictReader(r)
        for row in reader:
            name = row["title"]
            row.pop("title")
            short_name = name[0:-7]
            cleaned_name = "".join(
                e for e in short_name if e.isalnum() or e.isspace()
            ).lower()
            if cleaned_name not in cleaned_names:
                cleaned_names.append(cleaned_name)
                row["movie_title"] = cleaned_name
                cleaned_data.append(row)

    with open(write_file, "wb") as w:
        writer = csv.DictWriter(
            w,
            [
                "movie_title",
                "imdbRating",
                "ratingCount",
                "year",
                "nrOfWins",
                "nrOfNominations",
                "nrOfNewsArticles",
                "nrOfUserReviews",
            ],
        )
        writer.writeheader()
        for row in cleaned_data:
            writer.writerow(row)
