from abc import ABC, abstractmethod
class PostDAO(ABC):
    @abstractmethod
    def search_post(self, key):
        pass
    @abstractmethod
    def create_post(self, post):
        pass
    @abstractmethod
    def retrieve_posts(self, search_string):
        pass
    @abstractmethod
    def update_post(self, key, new_title, new_text):
        pass
    @abstractmethod
    def delete_post(self, key):
        pass
    @abstractmethod
    def list_posts(self):
        pass
