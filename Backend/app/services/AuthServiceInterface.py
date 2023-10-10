from abc import ABC, abstractmethod


class AuthServiceInterface(ABC):
    @abstractmethod
    def register_user(self, data):
        pass

    @abstractmethod
    def login_user(self, data):
        pass



