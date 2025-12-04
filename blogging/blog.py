import datetime
from blogging.post import Post
from blogging.dao.post_dao_pickle import PostDAOPickle

class Blog():
    ''' class that represents a blog '''

    def __init__(self, blog_id, blog_name, blog_url, blog_email):
        ''' construct a blog '''
        self.id = blog_id
        self.name = blog_name
        self.url = blog_url
        self.email = blog_email
        
        # Initialize DAO for posts
        self.post_dao = PostDAOPickle(self)

    def __eq__(self, other):
        ''' checks whether this blog is the same as other blog '''
        return self.id == other.id and self.name == other.name and self.url == other.url and self.email == other.email

    def __str__(self):
        ''' converts the blog object to a string representation '''
        return str(self.id) + "; " + self.name + "; " + self.url + "; " + self.email

    def __repr__(self):
        ''' converts the blog object to a string representation for debugging '''
        return "Blog(%r, %r, %r, %r)" % (self.id, self.name, self.url, self.email)

    def search_post(self, post_code):
        ''' search a post in the blog '''
        return self.post_dao.search_post(post_code)

    def create_post(self, post_title, post_text):
        ''' create a post in the blog '''
        # Get current counter from DAO and increment
        new_post_code = self.post_dao.counter + 1
        new_post = Post(new_post_code, post_title, post_text)
        success = self.post_dao.create_post(new_post)
        if success:
            return new_post
        return None

    def retrieve_posts(self, search_term):
        ''' retrieve posts in the blog that satisfy a search_term '''
        return self.post_dao.retrieve_posts(search_term)

    def update_post(self, post_code, new_post_title, new_post_text):
        ''' update a post from the blog '''
        # Check if post exists first
        if not self.search_post(post_code):
            return False
        return self.post_dao.update_post(post_code, new_post_title, new_post_text)

    def delete_post(self, post_code):
        ''' delete a post from the blog '''
        # Check if post exists first
        if not self.search_post(post_code):
            return False
        return self.post_dao.delete_post(post_code)

    def list_posts(self):
        ''' list all posts from the blog from the more recently added to the least recently added'''
        return self.post_dao.list_posts()