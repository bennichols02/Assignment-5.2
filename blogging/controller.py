import hashlib
import os
from blogging.blog import Blog
from blogging.post import Post
from blogging.configuration import Configuration
from blogging.dao.blog_dao_json import BlogDAOJSON
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException

class Controller():
    ''' Main controller class that handles all system operations for the blogging system
    Manages users aunthentication, blog operation, and  post operation
    Delegates persistence to DAO classes for separation of concerns.
    '''

    def __init__(self, autosave=False):
        ''' Initializes the controller with the default state and persistence configuration. '''
        self.autosave = autosave or Configuration.autosave
        self.users = {}
        self.load_users()
        self.username = None
        self.password_hash = None
        self.logged = False
        
        self.blog_dao = BlogDAOJSON()
        self.current_blog = None



    def load_users(self):
        ''' Loads user credentials from users.txt file into memory.
        Handles FileNotFoundError by starting with empty user dictionary.
        Only loads users if autosave is enabled. '''
        try:
            with open(Configuration.users_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:  # Skip empty lines
                        username, password_hash = line.split(',')
                        self.users[username] = password_hash
        except FileNotFoundError:
            # If file doesn't exist, start with empty users
            self.users = {}


    def password_hash(self, password):
        '''generates SHA-256 hash for a given password for secure storage.'''
        encoded_password = password.encode('utf-8')     
        hash_object = hashlib.sha256(encoded_password)      
        hex_dig = hash_object.hexdigest()       
        return hex_dig

    def login(self, username, password):
        ''' Authenticates user with username and password.
        User must not be already logged in and credentials must match stored values.
        '''
        if self.logged:
            raise DuplicateLoginException("User already logged in")
        
        if username not in self.users:
            raise InvalidLoginException("Invalid username")
        
        # Hash the provided password and compare with stored hash
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != self.users[username]:
            raise InvalidLoginException("Invalid password")
            
        self.username = username
        self.password_hash = password_hash
        self.logged = True
        return True

    def logout(self):
        ''' Logs out the currently authenticated user.
        Clears all user-specific data including current blog selection.
        '''
        if not self.logged:
            raise InvalidLogoutException("No user is currently logged in")
            
        self.username = None
        self.password_hash = None
        self.logged = False
        self.current_blog = None
        return True

    def search_blog(self, blog_id):
        ''' Searches for a blog by its unique identifier.
        User must be logged in to perform this operation.
        '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to search blogs")
            
        return self.blog_dao.search_blog(blog_id)

    def create_blog(self, blog_id, blog_name, blog_url, blog_email):
        '''Creates a new blog with the specified attributes.
        Blog ID must be unique across the system.
        '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to create blogs")
        
        blog = Blog(blog_id, blog_name, blog_url, blog_email)
        success = self.blog_dao.create_blog(blog)
        if not success:
            raise IllegalOperationException("Blog ID already exists")
        return blog

    def retrieve_blogs(self, search_term):
        ''' Retrieves all blogs whose names contain the search term.
        User must be logged in to perform this operation. '''

        if not self.logged:
            raise IllegalAccessException("User must be logged in to retrieve blogs")
            
        return self.blog_dao.retrieve_blogs(search_term)

    def update_blog(self, original_blog_id, blog_id, blog_name, blog_url, blog_email):
        ''' Updates an existing blog's attributes, optionally changing its ID.
        Cannot update the currently selected blog.
        '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to update blogs")
        
        blog = self.blog_dao.search_blog(original_blog_id)
        if not blog:
            raise IllegalOperationException("Blog not found")
            
        if self.current_blog and blog == self.current_blog:
            raise IllegalOperationException("Cannot update current blog")
        
        # Update blog fields
        blog.name = blog_name
        blog.url = blog_url
        blog.email = blog_email
        
        # Handle ID change
        if original_blog_id != blog_id:
            if self.blog_dao.search_blog(blog_id):
                raise IllegalOperationException("New blog ID already exists")
            self.blog_dao.delete_blog(original_blog_id)
            blog.id = blog_id
            self.blog_dao.create_blog(blog)
        else:
            self.blog_dao.update_blog(original_blog_id, blog)
            
        return True
            
    def delete_blog(self, blog_id):
        ''' Deletes a blog by its ID.
        Cannot delete the currently selected blog.
        '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to delete blogs")
            
        blog = self.blog_dao.search_blog(blog_id)
        if not blog:
            raise IllegalOperationException("Blog not found")
            
        if self.current_blog and blog == self.current_blog:
            raise IllegalOperationException("Cannot delete current blog")
            
        return self.blog_dao.delete_blog(blog_id)

    def list_blogs(self):
        ''' Retrieves all blogs in the system.
        User must be logged in to perform this operation.
        '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to list blogs")
            
        return self.blog_dao.list_blogs()

    def set_current_blog(self, blog_id):
        ''' Sets the specified blog as the current working blog.
        User must be logged in and blog must exist.
        '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to set current blog")
            
        blog = self.blog_dao.search_blog(blog_id)
        if not blog:
            raise IllegalOperationException("Blog not found")
            
        self.current_blog = blog
        return True

    def get_current_blog(self):
        '''Retrieves the currently selected blog.
        User must be logged in to perform this operation.'''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to get current blog")
            
        return self.current_blog

    def unset_current_blog(self):
        ''' Clears the current blog selection.
        User must be logged in to perform this operation.
        '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to unset current blog")
            
        self.current_blog = None
        return True

    def search_post(self, post_code):
        ''' Searches for a post in the current blog by post code.
        User must be logged in and have a blog selected.'''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to search posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.search_post(post_code)

    def create_post(self, post_title, post_text):
        ''' Creates a new post in the current blog.
        User must be logged in and have a blog selected. '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to create posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.create_post(post_title, post_text)

    def retrieve_posts(self, search_term):
        ''' Retrieves posts from current blog that match search term in title or content.
        User must be logged in and have a blog selected.'''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to retrieve posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.retrieve_posts(search_term)

    def update_post(self, post_code, new_post_title, new_post_text):
        '''   Updates title and content of an existing post in the current blog.
        User must be logged in and have a blog selected. '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to update posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.update_post(post_code, new_post_title, new_post_text)

    def delete_post(self, post_code):
        ''' Deletes a post from the current blog.
        User must be logged in and have a blog selected. '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to delete posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.delete_post(post_code)

    def list_posts(self):
        ''' Lists all posts from the current blog in reverse chronological order.
        User must be logged in and have a blog selected . '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to list posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.list_posts()
