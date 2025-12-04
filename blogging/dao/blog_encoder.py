import json
from blogging.blog import Blog

class BlogEncoder(json.JSONEncoder):
    ''' Custom JSON encoder for Blog objects.
    Converts Blog instances to serializable dictionaries for JSON storage.
    Handles the special serialization requirements for Blog objects. '''
    
    def default(self, blog_obj):
        '''
        Override default JSON encoding to handle Blog objects.
        '''
        if isinstance(blog_obj, Blog):
            # Create a serializable representation without the post_dao
            return {
                '__type__': 'Blog',
                'id': blog_obj.id,
                'name': blog_obj.name,
                'url': blog_obj.url,
                'email': blog_obj.email
                # We don't serialize posts here, they're handled separately
            }
        return super().default(blog_obj)