import random

import requests
from colorama import Fore, Style  # allows to add colors to the console output


class MovieApp:  # handles the user interface and commands for the movie application
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):  # list the movies
        movies = self._storage.list_movies()
        print(f"list of movies : \n {movies}")
        # print(Fore.BLUE + f"List of movies: \n {Fore.YELLOW}{json.dumps(movies, indent=4)}" + Style.RESET_ALL)

    def _command_add_movie(self):  # adding the movies
        title = input("Enter the movie title: ")
        api_url = f"http://www.omdbapi.com/?apikey=4bf81bd7&t={title}"

        response = requests.get(api_url)
        data = response.json()

        if data.get("Response") == "False":
            print("Movie not found. Please try again.")
            return

        year = data.get("Year")
        rating = data.get("imdbRating")
        poster = data.get("Poster")

        self._storage.add_movie(title, year, rating, poster)

    def _command_delete_movie(self):  # deleting the movies
        title = input("Enter the movie title to delete: ")
        self._storage.delete_movie(title)

    def _command_update_movie(self):  # update movie with new rating and notes
        title = input("Enter the movie title: ")
        rating = input("Enter the new rating: ")
        notes = input("Enter movie notes: ")
        self._storage.update_movie(title, rating, notes)

    def _command_movie_stats(self):  # generating and displaying statistics
        movies = self._storage.list_movies()

        rated_movies = [movie for movie in movies.values() if movie["rating"] != 'N/A']
        total_rated_movies = len(rated_movies)

        if total_rated_movies > 0:
            avg_rating = sum(float(movie["rating"]) for movie in rated_movies) / total_rated_movies
            sorted_ratings = sorted(float(movie["rating"]) for movie in rated_movies)
            mid = total_rated_movies // 2

            if total_rated_movies % 2 == 0:
                median_rating = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
            else:
                median_rating = sorted_ratings[mid]

            best_rating = max(float(movie["rating"]) for movie in rated_movies)
            best_movies = [name for name, movie in movies.items() if movie["rating"] == str(best_rating)]
            worst_rating = min(float(movie["rating"]) for movie in rated_movies)
            worst_movies = [name for name, movie in movies.items() if movie["rating"] == str(worst_rating)]

            print(Fore.BLUE + f"Total rated movies: {total_rated_movies}")
            print(f"Average rating of rated movies: {avg_rating:.2f}")
            print(f"Median rating of rated movies: {median_rating:.2f}")
            print(f"Best movie(s):")
            for movie in best_movies:
                print(f"{movie} (Rating: {best_rating:.1f})")
            print(f"Worst movie(s):")
            for movie in worst_movies:
                print(f"{movie} (Rating: {worst_rating:.1f})")
        else:
            print(Fore.YELLOW + "No rated movies found." + Style.RESET_ALL)

    def _command_random_movie(self):  # displaying random movie
        movies = self._storage.list_movies()

        if not movies:
            print("No movies found.")
            return

        random_movie = random.choice(list(movies.keys()))
        rating = movies[random_movie]['rating']
        print(Fore.BLUE + f"Random movie: {random_movie} (Rating: {rating})" + Style.RESET_ALL)

    def _command_search_movie(self):  # search movies as per user requirement
        movies = self._storage.list_movies()

        movie_to_search = input(Fore.BLUE + "Enter part of movie name: " + Style.RESET_ALL).lower()

        matches = []
        for movie, details in movies.items():
            if movie_to_search.lower() in movie.lower():
                matches.append((movie, details["rating"]))

        if len(matches) > 0:
            print(Fore.YELLOW + "Matches found:")
            for match in matches:
                print(match[0], ": ", match[1])
        else:
            print(Fore.RED + "No matches found." + Style.RESET_ALL)

    def _command_movies_by_rating(self):  # sort movies by rating
        movies = self._storage.list_movies()

        # Sort the movies by rating in descending order
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)

        # Print out the sorted movies
        print(Fore.BLUE + "Movies sorted by rating:" + Style.RESET_ALL)
        for name, details in sorted_movies:
            print(Fore.YELLOW + f"{name}, {details['rating']}" + Style.RESET_ALL)

    def _command_generate_website(self):  # generate website
        movies_data = self._storage.list_movies()

        movie_grid = ''
        for movie_title, movie_info in movies_data.items():
            movie_grid += '<li class="movie">\n'
            movie_grid += '  <div class="movie-container">\n'
            movie_grid += f'    <div class="movie-poster">\n'
            movie_grid += f' <a href="https://www.imdb.com/" target="_blank"><img src="{movie_info["poster_image_url"]}" alt="{movie_info.get("notes", "")}" title="{movie_info.get("notes", "")}" width="128" height="193"></a>\n'
            movie_grid += f'    </div>\n'
            movie_grid += '    <div class="movie-details">\n'
            movie_grid += f'      <div class="movie-title">{movie_title}</div>\n'
            movie_grid += f'      <div class="movie-year">{movie_info["year"]}</div>\n'
            movie_grid += f'      <div class="movie-rating"><b>{movie_info["rating"]}</b></div>\n'
            movie_grid += '    </div>\n'
            movie_grid += '  </div>\n'
            movie_grid += '</li>\n'

        # Open the HTML template file
        with open('_static/index_template.html', 'r') as file:
            # Read the contents of the file
            template = file.read()

        # Replace the placeholder with the movie grid
        output_html = template.replace('__TEMPLATE_MOVIE_GRID__', movie_grid)

        # Write the output to a new HTML file
        with open('_static/index.html', 'w') as file:
            file.write(output_html)

        print(Fore.LIGHTGREEN_EX + "Website generated successfully!" + Style.RESET_ALL)

    def run(self):  # runs movie application
        while True:
            print(Fore.MAGENTA + "\n********** My Movies Database **********\n")
            print(Fore.CYAN + "Menu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Movie statistics")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Generate website\n")

            choice = input(Fore.YELLOW + "Enter choice (0-9): " + Style.RESET_ALL)

            if choice == "0":
                print(Fore.BLUE + "Bye!" + Style.RESET_ALL)
                break
            elif choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_movie_stats()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_movies_by_rating()
            elif choice == "9":
                self._command_generate_website()
            else:
                print(Fore.RED + "Invalid choice. Please enter a number between 0 and 9.\n" + Style.RESET_ALL)
