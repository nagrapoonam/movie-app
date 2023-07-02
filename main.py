from movie_app import MovieApp
from storage_csv import StorageCsv
from storage_json import StorageJson


def main():
    option = int(input("Choose your Movies File (0-4): "))

    storage = None  # Default assignment

    if option == 0:
        print("Bye!!")
    elif option == 1:  # for using data.json file
        storage = StorageJson('data.json')
    elif option == 2:  # for using movies.csv file
        storage = StorageCsv('movies.csv')
    elif option == 3:  # for using abc.csv file
        storage = StorageCsv('abc.csv')
    elif option == 4:  # for using xyz.json file
        storage = StorageJson('xyz.json')
    else:
        print("Invalid choice. Please enter between 0-4")

    if storage:
        movie_app = MovieApp(storage)
        movie_app.run()


if __name__ == '__main__':
    main()
