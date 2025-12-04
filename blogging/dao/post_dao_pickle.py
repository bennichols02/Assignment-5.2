import pickle
import os
from blogging.dao.post_dao import PostDAO
from blogging.configuration import Configuration

class PostDAOPickle(PostDAO):
    '''
    Concrete pickle-based implementation of PostDAO for post persistence.
    Handles CRUD operations for Post objects with binary file storage.
    Each blog's posts are stored in separate .dat files in the records directory.
    Files are named using blog ID with .dat extension (e.g., '12345.dat').
    '''

    def __init__(self, blog):
        '''
        Initialize the PostDAOPickle for a specific blog.
        '''
        self.autosave = Configuration.autosave
        self.blog = blog
        self.posts = []
        self.counter = 0
        
        # Load posts from file if autosave is enabled
        if self.autosave:
            self.load_posts()

    def get_record_file_path(self):
        ''' Construct file path for this blog's posts file 
        using blog ID and configured extension. '''
        filename = f"{self.blog.id}{Configuration.records_extension}"
        return os.path.join(Configuration.records_path, filename)

    def load_posts(self):
        '''
        Load posts from blog-specific binary file using pickle.
        Handles various file-related errors gracefully.
        Updates counter to maintain proper post code sequencing after load..
        '''
        try:
            pickle_file_path = self.get_record_file_path()
            if os.path.exists(pickle_file_path) and os.path.getsize(pickle_file_path) > 0:
                with open(pickle_file_path, 'rb') as pickle_file:
                    posts_list = pickle.load(pickle_file)
                    if posts_list is not None:  # Ensure we don't get None
                        self.posts = posts_list
                        # Update counter to ensure new posts get proper codes
                        if self.posts:
                            self.counter = max(post.code for post in self.posts)
        except (FileNotFoundError, pickle.PickleError, EOFError, AttributeError):
            # Handle corrupted or missing files by starting fresh
            self.posts = []
            self.counter = 0

    def save_posts(self):
        ''' Save current posts to binary file using pickle.
        Creates necessary directories and writes posts list in binary format.
        Only executes if autosave is enabled.
        '''
        
        if self.autosave:
            try:
                os.makedirs(Configuration.records_path, exist_ok=True)
                pickle_file_path = self.get_record_file_path()
                with open(pickle_file_path, 'wb') as pickle_file:
                    pickle.dump(self.posts, pickle_file)
            except Exception as e:
                print(f"Error saving posts: {e}")

    def search_post(self, post_code):
        ''' Search for a post by its unique code.
        Linear search through posts list - returns first matching Post or None.
        '''
        for post in self.posts:
            if post.code == post_code:
                return post
        return None

    def create_post(self, post):
        ''' Add a new post to the collection.
        Updates counter and automatically saves to file if autosave enabled.
        Returns True on success. '''
        self.posts.append(post)
        self.counter = max(self.counter, post.code)
        self.save_posts()
        return True

    def retrieve_posts(self, search_term):
        ''' Retrieve posts containing search term in title or text.
        Returns list of matching Post objects.
        Search is case-sensitive. '''
        matching_posts = []
        for post in self.posts:
            if search_term in post.title or search_term in post.text:
                matching_posts.append(post)
        return matching_posts

    def update_post(self, post_code, new_post_title, new_post_text):
        ''' Update title and text of an existing post.
        Returns False if post doesn't exist, True on successful update.
        Automatically saves changes to file.'''
        post = self.search_post(post_code)
        if not post:
            return False
        post.update(new_post_title, new_post_text)
        self.save_posts()
        return True

    def delete_post(self, post_code):
        '''Delete a post by its code.
        Returns False if post doesn't exist, True on successful deletion.
        Automatically saves changes to file.'''
        for i, post in enumerate(self.posts):
            if post.code == post_code:
                del self.posts[i]
                self.save_posts()
                return True
        return False

    def list_posts(self):
        ''' Return all posts in reverse chronological order (most recent first).
        Uses creation time for ordering - newer posts appear first . '''
        return list(reversed(self.posts))
