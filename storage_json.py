from istorage import IStorage
import json


class StorageJson(IStorage): #implements the IStorage interface for JSON storage
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self): # method reads the JSON data from the file
        with open(self.file_path, "r") as json_file:
            data = json.load(json_file)
        return data

    def add_movie(self, title, year, rating, poster): #adds a new movie to the JSON data
        existing_data = {}
        with open(self.file_path, "r") as json_file:
            existing_data = json.load(json_file)

        if title.lower() in (existing.lower() for existing in existing_data):
            print("Movie already exists in Json File")
        else:
            movie_data = {
                "year": year,
                "rating": rating,
                "poster_image_url": poster
            }
            existing_data[title] = movie_data

            with open(self.file_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)

            print("Movie data stored in Json File")

    def delete_movie(self, title): #removes a movie from the JSON data
        with open(self.file_path, "r") as json_file:
            data = json.load(json_file)

        if title in data:
            del data[title]
            print(f"Movie '{title}' deleted.")

            with open(self.file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
        else:
            print(f"Movie '{title}' not found.")

    def update_movie(self, title, rating, notes): #method updates the rating and notes of a movie in the JSON data
        with open(self.file_path, "r") as json_file:
            data = json.load(json_file)

        if title in data:
            data[title]["rating"] = rating
            data[title]["notes"] = notes
            print(f"Movie '{title}' successfully updated.")

            with open(self.file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
        else:
            print(f"Movie '{title}' not found.")
