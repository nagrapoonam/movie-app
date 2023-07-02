import csv
from pathlib import Path

from istorage import IStorage


class StorageCsv(IStorage):  # implements the IStorage interface for JSON storage
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):  # method reads the CSV data from the file
        movies = {}
        with open(self.file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                title = row["title"]
                year = row["year"]
                rating = row["rating"]
                poster = row["poster"]
                movies[title] = {
                    "year": year,
                    "rating": rating,
                    "poster_image_url": poster
                }
        return movies

    def add_movie(self, title, year, rating, poster):  # adds a new movie to the CSV data
        header = ["title", "year", "rating", "poster"]
        movie_data = [title, year, rating, poster]

        file_exists = Path(self.file_path).is_file()

        with open(self.file_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)

            if not file_exists:
                writer.writerow(header)

            writer.writerow(movie_data)

        print("Movie data stored in Csv File")

    def delete_movie(self, title):  # removes a movie from the CSV data
        movies = self.list_movies()
        if title in movies:
            with open(self.file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["title", "year", "rating", "poster"])
                for movie_title, movie_info in movies.items():
                    if movie_title != title:
                        writer.writerow(
                            [movie_title, movie_info["year"], movie_info["rating"], movie_info["poster_image_url"]])
            print(f"Movie '{title}' deleted.")
        else:
            print(f"Movie '{title}' not found.")

    def update_movie(self, title, rating, notes):  # method updates the rating and notes of a movie in the csv data
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            movies[title]["notes"] = notes
            with open(self.file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["title", "year", "rating", "poster"])
                for movie_title, movie_info in movies.items():
                    writer.writerow(
                        [movie_title, movie_info["year"], movie_info["rating"], movie_info["poster_image_url"]])
            print(f"Movie '{title}' successfully updated.")
        else:
            print(f"Movie '{title}' not found.")
