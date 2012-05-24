# Copyright (c) 2012 Idee Inc. All rights reserved worldwide.

from image import Image
from metadata_request import MetadataRequest

class MulticolorEngineRequest(MetadataRequest):
    """
    Class to send requests to a MulticolorEngine API. 
    
    Adding an image using data:

        >>> from tineyeservices import MulticolorEngineRequest, Image
        >>> api = MulticolorEngineRequest(api_url='http://localhost/rest/')
        >>> image = Image(filepath='/path/to/image.jpg')
        >>> api.add_image(images=[image])
        {u'error': [], u'method': u'add', u'result': [], u'status': u'ok'}
        
    Searching for an image using colors:
    
        >>> api.color_search_color(colors=['255,255,235', '12FA3B'])
        {'error': [],
         'method': 'color_search',
         'result': [{'filepath': 'path/to/file.jpg',
                     'score': '13.00'}],
         'status': 'ok'}
    """

    def __repr__(self):
        return "MulticolorEngineRequest(api_url=%r, username=%r, password=%r)" %\
               (self.api_url, self.username, self.password)

    def color_search_image(self, image, ignore_background=True, metadata='', 
                           return_metadata='', sort_metadata=False, min_score=0,
                           offset=0, limit=5000):
        """
        Do a color search against the collection using image data
        and return matches with corresponding scores.
        
        Arguments:

        - `image`, an Image object.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.
        - `metadata`, metadata to be used for additional filtering.
        - `return_metadata`, metadata to be returned with each match.
        - `sort_metadata`, whether the search results are sorted by metadata score.
        - `min_score`, minimum score that should be returned.
        - `offset`, offset of results from the start.
        - `limit`, maximum number of matches that should be returned.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `filepath`, match image path.
        """
        params = {'ignore_background': ignore_background,
                  'metadata': metadata,
                  'return_metadata': return_metadata,
                  'sort_metadata': sort_metadata,
                  'min_score': min_score,
                  'offset': offset,
                  'limit': limit}

        if not isinstance(image, Image):
            raise TypeError('Need to pass an Image object')

        file_params = {'image': (image.collection_filepath, image.data)}

        return self._request('color_search', params, file_params)

    def color_search_filepath(self, filepath, ignore_background=True, metadata='',
                              return_metadata='', sort_metadata=False, min_score=0,
                              offset=0, limit=5000):
        """
        Do a color search against the collection using an image already in the
        collection and return matches with corresponding scores.
        
        Arguments:

        - `filepath`, a filepath string of an image already in the collection.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.
        - `metadata`, metadata to be used for additional filtering.
        - `return_metadata`, metadata to be returned with each match.
        - `sort_metadata`, whether the search results are sorted by metadata score.
        - `min_score`, minimum score that should be returned.
        - `offset`, offset of results from the start.
        - `limit`, maximum number of matches that should be returned.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `filepath`, match image path.
        """
        params = {'filepath': filepath,
                  'ignore_background': ignore_background,
                  'metadata': metadata,
                  'return_metadata': return_metadata,
                  'sort_metadata': sort_metadata,
                  'min_score': min_score,
                  'offset': offset,
                  'limit': limit}
                  
        return self._request('color_search', params)
        
    def color_search_url(self, url, ignore_background=True, metadata='', 
                         return_metadata='', sort_metadata=False, min_score=0, 
                         offset=0, limit=5000):
        """
        Do a color search against the collection using an image URL 
        and return matches with corresponding scores.

        Arguments:

        - `url`, a URL string pointing to an image.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.
        - `metadata`, metadata to be used for additional filtering.
        - `return_metadata`, metadata to be returned with each match.
        - `sort_metadata`, whether the search results are sorted by metadata score.
        - `min_score`, minimum score that should be returned.
        - `offset`, offset of results from the start.
        - `limit`, maximum number of matches that should be returned.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `filepath`, match image path.
        """
        params = {'url': url,
                  'ignore_background': ignore_background,
                  'metadata': metadata,
                  'return_metadata': return_metadata,
                  'sort_metadata': sort_metadata,
                  'min_score': min_score,
                  'offset': offset,
                  'limit': limit}

        return self._request('color_search', params)
        
    def color_search_color(self, colors, weights=[], metadata='',
                           return_metadata='', sort_metadata=False, min_score=0, 
                           offset=0, limit=5000):
        """
        Do a color search against the collection using specified colors
        and return matches with corresponding scores.
        
        Arguments:

        - `colors`, a list of string of colors in RGB ('255,112,223') or hex ('DF4F23') format.
        - `weights`, a list of weights.
        - `metadata`, metadata to be used for additional filtering.
        - `return_metadata`, metadata to be returned with each match.
        - `sort_metadata`, whether the search results are sorted by metadata score.
        - `min_score`, minimum score that should be returned.
        - `offset`, offset of results from the start.
        - `limit`, maximum number of matches that should be returned.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `filepath`, match image path.
        """
        params = {'metadata': metadata,
                  'return_metadata': return_metadata,
                  'sort_metadata': sort_metadata,
                  'min_score': min_score,
                  'offset': offset,
                  'limit': limit}

        if not isinstance(colors, list) or not isinstance(weights, list):
            raise TypeError('Need to pass lists of colors and weights')

        counter = 0
        for color in colors:
            params['colors[%i]' % counter] = color
            counter += 1

        counter = 0
        for weight in weights:
            params['weights[%i]' % counter] = str(weight)
            counter += 1

        return self._request('color_search', params)

    def extract_image_colors_image(self, images, ignore_background=True, limit=32,
                                   color_format='rgb'):
        """
        Extract the dominant colors given image upload data.

        Arguments:

        - `images`, a list of Image objects.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.
        - `limit`, maximum number of colors that should be returned.
        - `color_format`, RGB or hex formatted colors, can be either 'rgb' or 'hex'.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries each representing a color with
          associated ranking and weight.
        """
        params = {'limit': limit,
                  'ignore_background': ignore_background,
                  'color_format': color_format}
        file_params = {}
        counter = 0

        if not isinstance(images, list):
            raise TypeError('Need to pass a list of Image objects')

        for image in images:
            if not isinstance(image, Image):
                raise TypeError('Need to pass a list of Image objects')
            file_params['images[%i]' % counter] = (image.collection_filepath, image.data)
            counter += 1

        return self._request('extract_image_colors', params, file_params)
        
    def extract_image_colors_url(self, urls, ignore_background=True, limit=32, 
                                 color_format='rgb'):
        """
        Extract the dominant colors given image URLs.
        
        Arguments:

        - `urls`, a list of URL strings pointing to images.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.
        - `limit`, maximum number of colors that should be returned.
        - `color_format`, RGB or hex formatted colors, can be either 'rgb' or 'hex'.
        
        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries each representing a color with
          associated ranking and weight.
        """
        params = {'limit': limit,
                  'ignore_background': ignore_background,
                  'color_format': color_format}
        counter = 0
        
        if not isinstance(urls, list):
            raise TypeError('Need to pass a list of URL strings')

        for url in urls:
            params['urls[%i]' % counter] = url
            counter += 1

        return self._request('extract_image_colors', params)

    def count_image_colors_image(self, images, ignore_background=True, colors=[]):
        """
        Generate a counter for each color from the palette specifying
        how many of the input images contain that color given image upload data.

        Arguments:

        - `images`, a list of Image objects.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.
        - `colors`, a list of colors (palette) which you want to count.
          Can be rgb "255,255,255" or hex format "ffffff".

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries each representing a color.
        
          + `color`, the color that was passed in.
          + `num_images_partial_area`, the number of images that partially matched the color.
          + `num_images_full_area`, the number of images that fully matched the color.
        """
        params = {'ignore_background': ignore_background}
        file_params = {}

        if not isinstance(images, list):
            raise TypeError('Need to pass a list of Image objects')

        if not isinstance(colors, list):
            raise TypeError('Need to pass a list of colors')

        counter = 0
        for color in colors:
            params['colors[%i]' % counter] = color
            counter += 1

        counter = 0
        for image in images:
            if not isinstance(image, Image):
                raise TypeError('Need to pass a list of Image objects')
            file_params['images[%i]' % counter] = (image.collection_filepath, image.data)
            counter += 1

        return self._request('count_image_colors', params, file_params)

    def count_image_colors_url(self, urls, ignore_background=True, colors=[]):
        """
        Generate a counter for each color from the palette specifying
        how many of the input images contain that color given image URLs.

        Arguments:

        - `urls`, a list of URL strings pointing to images.
        - `ignore_background`, if true, ignore the background color of the images,
          if false, include the background color of the images.
        - `colors`, a list of colors (palette) which you want to count.
          Can be rgb "255,255,255" or hex format "ffffff".

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries each representing a color.
        
          + `color`, the color that was passed in.
          + `num_images_partial_area`, the number of images that partially matched the color.
          + `num_images_full_area`, the number of images that fully matched the color.
        """
        params = {'ignore_background': ignore_background}

        if not isinstance(urls, list):
            raise TypeError('Need to pass a list of URL strings')

        if not isinstance(colors, list):
            raise TypeError('Need to pass a list of colors')
        
        counter = 0
        for color in colors:
            params['colors[%i]' % counter] = color
            counter += 1
        
        counter = 0
        for url in urls:
            params['urls[%i]' % counter] = url
            counter += 1

        return self._request('count_image_colors', params)

    def extract_collection_colors_filepath(self, filepaths, limit=32, color_format='rgb'):
        """
        Extract the dominant colors of a set of images given a list of filepaths
        already in your collection.
        
        Arguments:

        - `filepaths`, a list of string filepaths of images already in the collection.
        - `limit`, maximum number of colors that should be returned.
        - `color_format`, RGB or hex formatted colors, can be either 'rgb' or 'hex'.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries each representing a color with
          associated ranking and weight.
        """
        params = {'limit': limit,
                  'color_format': color_format}
        counter = 0
        
        if not isinstance(filepaths, list):
            raise TypeError('Need to pass a list of filepaths')
        
        for filepath in filepaths:
            params['filepaths[%i]' % counter] = filepath
            counter += 1

        return self._request('extract_collection_colors', params)

    def extract_collection_colors_metadata(self, metadata, limit=32, color_format='rgb'):
        """
        Extract the dominant colors of a set of images given a subset of the collection
        filtered using metadata.
        
        Arguments:

        - `metadata`, the metadata to be used for filtering.
        - `limit`, maximum number of colors that should be returned.
        - `color_format`, RGB or hex formatted colors, can be either 'rgb' or 'hex'

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries each representing a color with
          associated ranking and weight.
        """
        params = {'metadata': metadata,
                  'limit': limit,
                  'color_format': color_format}

        return self._request('extract_collection_colors', params)

    def count_collection_colors_filepath(self, filepaths, colors=[]):
        """
        Generate a counter for each color from the specified color palette 
        representing how many of the collection images contain that color,
        given a list of filepaths of images in the collection.

        Arguments:

        - `filepaths`, a list of string filepaths as returned by
          a search or list call.
        - `colors`, a list of colors (palette) which you want to count.
          Can be rgb "255,255,255" or hex format "ffffff".

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries each representing a color.
        
          + `color`, the color that was passed in.
          + `num_images_partial_area`, the number of images that partially matched the color.
          + `num_images_full_area`, the number of images that fully matched the color.
        """
        params = {}

        if not isinstance(filepaths, list):
            raise TypeError('Need to pass a list of filepaths')

        if not isinstance(colors, list):
            raise TypeError('Need to pass a list of colors')

        counter = 0
        for color in colors:
            params['colors[%i]' % counter] = color
            counter += 1

        counter = 0
        for filepath in filepaths:
            params['filepaths[%i]' % counter] = filepath
            counter += 1

        return self._request('count_collection_colors', params)


    def count_collection_colors_metadata(self, metadata, colors=[]):
        """
        Generate a counter for each color from the specified color palette 
        representing how many of the collection images contain that color,
        given some metadata to filter the collection images.

        Arguments:

        - `metadata`, metadata to filter the collection.
        - `colors`, a list of colors (palette) which you want to count.
          Can be rgb "255,255,255" or hex format "ffffff".

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries each representing a color.
        
          + `color`, the color that was passed in.
          + `num_images_partial_area`, the number of images that partially matched the color.
          + `num_images_full_area`, the number of images that fully matched the color.
        """
        params = {'metadata': metadata}

        if not isinstance(colors, list):
            raise TypeError('Need to pass a list of colors')

        counter = 0
        for color in colors:
            params['colors[%i]' % counter] = color
            counter += 1

        return self._request('count_collection_colors', params)
