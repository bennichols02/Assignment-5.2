import json
from blogging.blog import Blog

class BlogDecoder(json.JSONDecoder):
    ''' Custom JSON decoder for Blog objects.
    Converts serialized Blog dictionaries back to Blog instances during JSON loading.
    Works in conjunction with BlogEncoder for complete serialization cycle. '''
    
    def __init__(self, *args, **kwargs):
    #Initialize decoder with custom object hook for Blog reconstruction.
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, data_dict):

        '''
        Convert dictionary back to Blog object during JSON parsing.
        '''

        if '__type__' in data_dict and data_dict['__type__'] == 'Blog':
            # Reconstruct Blog object from dictionary data
            return Blog(data_dict['id'], data_dict['name'], data_dict['url'], data_dict['email'])
        return data_dict