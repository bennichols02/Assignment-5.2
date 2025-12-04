import datetime

class Post():
    ''' class that represents a post '''

    def __init__(self, post_code, post_title, post_text):
        ''' constructs a post '''
        self.code = post_code
        self.title = post_title
        self.text = post_text
        now = datetime.datetime.now()
        self.creation_time = now
        self.update_time = now

    def update(self, new_post_title, new_post_text):
        ''' update post post_title and post_text '''
        self.title = new_post_title
        self.text = new_post_text
        self.update_time = datetime.datetime.now()	

    def __eq__(self, other):
        ''' checks whether this post is the same as other post '''
        return self.code == other.code and self.title == other.title and self.text == other.text

    def __str__(self):
        ''' converts the post object to a string representation '''
        return str(self.code) + "; " + str(self.creation_time) + "; " + str(self.update_time) + "\n" + str(self.title) + "\n\n" + self.text

    def __repr__(self):
        ''' converts the post object to a string representation for debugging '''
        return "Post(%r, %r, %r,\n%r,\n\n%r\n)" % (self.code, self.creation_time, self.update_time, self.title, self.text)
