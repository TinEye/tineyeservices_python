# Copyright (c) 2012 Idee Inc. All rights reserved worldwide.

from image import Image
from tineye_service_request import TinEyeServiceRequest

class MetadataRequest(TinEyeServiceRequest):
    """ Class to send requests to a TinEye Services API. """

    def add_image(self, images, ignore_background=True, **kwargs):
        """
        Add images to the collection using data.
        
        Arguments:

        - `images`, a list of Image objects.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.
              
        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        """
        params = {'ignore_background': ignore_background}
        file_params = {}
        counter = 0

        if not isinstance(images, list):
            raise TypeError('Need to pass a list of Image objects')

        for image in images:
            if not isinstance(image, Image):
                raise TypeError('Need to pass a list of Image objects')
            file_params['images[%i]' % counter] = (image.collection_filepath, image.data)
            if image.metadata is not None:
                params['metadata[%i]' % counter] = image.metadata
            counter += 1

        return self._request('add', params, file_params, **kwargs)

    def add_url(self, images, ignore_background=True, **kwargs):
        """
        Add images to the collection via URLs.
        
        Arguments:

        - `images`, a list of Image objects.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        """
        params = {'ignore_background': ignore_background}
        counter = 0
            
        if not isinstance(images, list):
            raise TypeError('Need to pass a list of Image objects')

        for image in images:
            if not isinstance(image, Image):
                raise TypeError('Need to pass a list of Image objects')
            params['urls[%i]' % counter] = image.url
            params['filepaths[%i]' % counter] = image.collection_filepath
            if image.metadata is not None:
                params['metadata[%i]' % counter] = image.metadata
            counter += 1

        return self._request('add', params, **kwargs)

    def update_metadata(self, filepaths, metadata, **kwargs):
        """
        Force a metadata update for images already present in the collection.

        Arguments:

        - `filepaths`, a list of filepath strings of an image already in the collection
          as returned by a search or list operation.
        - `metadata`, the metadata to be stored with the image.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        """
        params = {}
        counter = 0
        
        if not isinstance(filepaths, list):
            raise TypeError('Need to pass a list of filepaths')
       
        if not isinstance(metadata, list):
            raise TypeError('Need to pass a list of metadata')
        
        for filepath in filepaths:
            params['filepaths[%i]' % counter] = filepath
            counter += 1

        counter = 0
        for m in metadata:
            params['metadata[%i]' % counter] = metadata
            counter += 1

        return self._request('update_metadata', params, **kwargs)

    def get_metadata(self, filepaths, **kwargs):
        """
        Get associated keywords from the index given a list of image filepaths.
        
        Arguments:

        - `filepaths`, a list of filepath strings of an image already in the collection
          as returned by a search or list operation.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, the metadata tree structure that is associated with the given filepath.
        """
        params = {}
        counter = 0
        
        if not isinstance(filepaths, list):
            raise TypeError('Need to pass a list of filepaths')
        
        for filepath in filepaths:
            params['filepaths[%i]' % counter] = filepath
            counter += 1

        return self._request('get_metadata', params, **kwargs)

    def get_search_metadata(self, **kwargs):
        """
        Get the metadata tree structure that can be searched.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, the tree structure that can be searched along with keyword type
          and the number of images from the index containing that keyword.
        """
        return self._request('get_search_metadata', {}, **kwargs)

    def get_return_metadata(self, **kwargs):
        """
        Get the metadata that can be returned by a search method along with each match.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of keywords with data type and the number of images 
          from the index containing that keyword.
        """
        return self._request('get_return_metadata', {}, **kwargs)
