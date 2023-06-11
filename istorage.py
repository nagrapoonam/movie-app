from abc import ABC, abstractmethod

class IStorage(ABC): # abstract base class. Interface for storage implementations
    @abstractmethod
    def list_movies(self): # abstract method
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster): # abstract method
        pass

    @abstractmethod
    def delete_movie(self, title): # abstract method
        pass

    @abstractmethod
    def update_movie(self, title, notes): # abstract method
        pass
