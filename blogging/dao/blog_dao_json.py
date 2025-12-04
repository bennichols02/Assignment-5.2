import json
import os
from blogging.dao.blog_dao import BlogDAO
from blogging.blog import Blog
from blogging.configuration import Configuration
from blogging.dao.blog_encoder import BlogEncoder
from blogging.dao.blog_decoder import BlogDecoder
from blogging.exception.illegal_operation_exception import IllegalOperationException

class BlogDAOJSON(BlogDAO):
    '''
    Concrete implementation of BlogDAO that uses JSON for persistence.
    Handles all CRUD operations for Blog objects with automatic file saving.
    Manages automatic saving/loading of blogs to/from blogs.json file.
    '''

    def __init__(self):
        '''
        Initialize the BlogDAOJSON with persistence configuration.
        Loads existing blogs from file if autosave is enabled.
        '''
        self.autosave = Configuration.autosave
        self.blogs = {}
        
        # Load blogs from file if autosave is enabled
        if self.autosave:
            self.load_blogs()

    def load_blogs(self):
        ''' Load blogs from JSON file into memory.
        Handles cases where file doesn't exist or contains invalid JSON.
        Creates empty blog collection if loading fails. '''
        if self.autosave and os.path.exists(Configuration.blogs_file):
            try:
                with open(Configuration.blogs_file, 'r') as json_file:
                    blogs_list = json.load(json_file)
                    # Convert each dictionary in the list to a Blog object
                    for blog_dict in blogs_list:
                        blog = Blog(
                            blog_dict['id'],
                            blog_dict['name'], 
                            blog_dict['url'],
                            blog_dict['email']
                        )
                        self.blogs[blog.id] = blog
            except (FileNotFoundError, json.JSONDecodeError):
                # If file doesn't exist or is invalid, start with empty blogs
                self.blogs = {}

    def save_blogs(self):
        ''' Save current blog collection to JSON file.
        Creates necessary directories and writes blogs as JSON array.
        Only executes if autosave is enabled. '''
        if self.autosave:
            blogs_list = []
            # Convert each Blog object to serializable dictionary
            for blog in self.blogs.values():
                blogs_list.append({
                    'id': blog.id,
                    'name': blog.name,
                    'url': blog.url,
                    'email': blog.email
                })
            
            # Ensure directory exists before writing file
            os.makedirs(os.path.dirname(Configuration.blogs_file), exist_ok=True)
            
            with open(Configuration.blogs_file, 'w') as json_file:
                json.dump(blogs_list, json_file, indent=2)

    def search_blog(self, blog_id):
        ''' Search for a blog by its unique ID. Returns Blog object or None if not found. '''
        return self.blogs.get(blog_id)

    def create_blog(self, blog):
        ''' Create a new blog in the collection.
        Returns False if blog with same ID already exists, True on success.
        Automatically saves to file if autosave is enabled. '''
        if blog.id in self.blogs:
            return False
        self.blogs[blog.id] = blog
        self.save_blogs()
        return True

    def retrieve_blogs(self, search_term):
        ''' Retrieve all blogs whose names contain the search term.
        Returns list of matching Blog objects.
        Search is case-sensitive.'''
        matching_blogs = []
        for blog in self.blogs.values():
            if search_term in blog.name:
                matching_blogs.append(blog)
        return matching_blogs

    def update_blog(self, blog_id, blog):
        ''' Update an existing blog with new data.
        Returns False if blog doesn't exist, True on successful update.
        Automatically saves changes to file. '''
        if blog_id not in self.blogs:
            return False
        self.blogs[blog_id] = blog
        self.save_blogs()
        return True

    def delete_blog(self, blog_id):
        ''' Delete a blog by its ID.
        Returns False if blog doesn't exist, True on successful deletion.
        Automatically saves changes to file. '''
        if blog_id not in self.blogs:
            return False
        del self.blogs[blog_id]
        self.save_blogs()
        return True

    def list_blogs(self):
        ''' Return list of all blogs currently in the collection .'''
        return list(self.blogs.values())