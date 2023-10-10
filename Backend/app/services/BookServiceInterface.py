from abc import ABC, abstractmethod

class BookServiceInterface(ABC):
    @abstractmethod
    def add_book(self, data):
        pass

    @abstractmethod
    def get_book(self, book_id):
        pass

    @abstractmethod
    def update_book(self, book_id, data):
        pass

    @abstractmethod
    def delete_book(self, book_id):
        pass

    @abstractmethod
    def list_books(self):
        pass
