from abc import ABC, abstractmethod

class IUserService(ABC):
    @abstractmethod
    def get_user(self):
        pass

    @abstractmethod
    def update_user(selfuser_data):
        pass

    @abstractmethod
    def delete_user(self):
        pass
