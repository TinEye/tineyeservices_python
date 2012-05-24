# Copyright (c) 2012 Idee Inc. All rights reserved worldwide.

import contextlib
import os

class Image():
    """ 
    Class representing an image.

    Image on filesystem:

        >>> from tineyeservices import Image
        >>> image = Image(filepath='/path/to/image.jpg', collection_filepath='collection.jpg')
        
    Image URL:

        >>> image = Image(url='http://www.tineye.com/images/meloncat.jpg', collection_filepath='collection.jpg')
  
    Image with metadata:

        >>> import simplejson
        >>> metadata = simplejson.dumps({"keywords": ["dolphin"]})
        >>> image = Image(filepath='/path/to/image.jpg', metadata=metadata)
  
    """
    
    def __init__(self, filepath='', url='', collection_filepath='', metadata=None):
        self.data = None
        self.filepath = filepath
        self.url = url
        self.collection_filepath = ''

        # If a filepath is specified, read the image and use that as the collection filepath
        if filepath != '':
            with contextlib.closing(open(filepath, 'rb')) as fp:
                self.data = fp.read()
            self.collection_filepath = filepath
            
        # If no filepath but a URL is specified, use the basename of the URL
        # as the collection filepath
        self.url = url
        if self.data == None and self.url != '':
            self.collection_filepath = os.path.basename(self.url)

        # If user specified their own filepath, then use that instead
        if collection_filepath != '':
            self.collection_filepath = collection_filepath

        # Need to make sure there is at least data or a URL
        if self.data == None and self.url == '':
            raise ValueError('Image object needs either data or a URL.')

        self.metadata = metadata

    def __repr__(self):
        return "Image(filepath=%r, url=%r, collection_filepath=%r, metadata=%r)" %\
               (self.filepath, self.url, self.collection_filepath, self.metadata)
