from abc import ABC, abstractmethod
class BlogDAO(ABC):
    @abstractmethod
    def search_blog(self, key):
        pass
    @abstractmethod
    def create_blog(self, blog):
        pass
    @abstractmethod
    def retrieve_blogs(self, search_string):
        pass
    @abstractmethod
    def update_blog(self, key, blog):
        pass
    @abstractmethod
    def delete_blog(self, key):
        pass
    @abstractmethod
    def list_blogs(self):
        pass

