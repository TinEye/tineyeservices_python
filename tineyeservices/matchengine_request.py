# -*- coding: utf-8 -*-
# Copyright (c) 2018 TinEye. All rights reserved worldwide.

import time
from .image import Image
from .tineye_service_request import TinEyeServiceRequest


class MatchEngineRequest(TinEyeServiceRequest):
    """
    Class to send requests to a MatchEngine API.

    Adding an image using data:

        >>> from tineyeservices import MatchEngineRequest, Image
        >>> api = MatchEngineRequest(api_url='http://localhost/rest/')
        >>> image = Image(filepath='/path/to/image.jpg')
        >>> api.add_image(images=[image])
        {u'error': [], u'method': u'add', u'result': [], u'status': u'ok'}

    Searching for an image using an image URL:

        >>> api.search_url(url='https://tineye.com/images/meloncat.jpg')
        {'error': [],
         'method': 'search',
         'result': [{'filepath': 'match1.png',
                     'score': '97.2',
                     'overlay': 'overlay/query.png/match1.png[...]'}],
         'status': 'ok'}
    """

    def __repr__(self):
        return "MatchEngineRequest(api_url=%r, username=%r, password=%r)" %\
               (self.api_url, self.username, self.password)

    def add_image(self, images, **kwargs):
        """
        Add images to the collection using data.

        Arguments:

        - `images`, a list of Image objects.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        """
        params = {}
        file_params = {}
        counter = 0

        if not isinstance(images, list):
            raise TypeError('Need to pass a list of Image objects')

        for image in images:
            if not isinstance(image, Image):
                raise TypeError('Need to pass a list of Image objects')
            # Put dummy filename here, we are going to use the API's filepath params instead
            file_params['images[%i]' % counter] = ('%s.%i' % (time.time(), counter), image.data)
            params['filepaths[%i]' % counter] = image.collection_filepath
            counter += 1

        return self._request('add', params, file_params, **kwargs)

    def add_url(self, images, **kwargs):
        """
        Add images to the collection via URLs.

        Arguments:

        - `images`, a list of Image objects.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        """
        params = {}
        counter = 0

        if not isinstance(images, list):
            raise TypeError('Need to pass a list of Image objects')

        for image in images:
            if not isinstance(image, Image):
                raise TypeError('Need to pass a list of Image objects')
            params['urls[%i]' % counter] = image.url
            params['filepaths[%i]' % counter] = image.collection_filepath
            counter += 1

        return self._request('add', params, **kwargs)

    def search_image(self, image, min_score=0, offset=0, limit=10, check_horizontal_flip=False, **kwargs):
        """
        Search against the collection using image data and return any matches
        with corresponding scores.

        Arguments:

        - `image`, an Image object.
        - `min_score`, minimum score that should be returned.
        - `offset`, offset of results from the start.
        - `limit`, maximum number of matches that should be returned.
        - `check_horizontal_flip`, whether to incorporate a horizontal flip check.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `overlay`, URL pointing to overlay image.
          + `filepath`, match image path.
        """
        params = {
            'min_score': min_score,
            'offset': offset,
            'limit': limit,
            'check_horizontal_flip': check_horizontal_flip}

        if not isinstance(image, Image):
            raise TypeError('Need to pass an Image object')

        file_params = {'image': (image.collection_filepath, image.data)}

        return self._request('search', params, file_params, **kwargs)

    def search_filepath(
            self, filepath, min_score=0, offset=0, limit=10,
            check_horizontal_flip=False, **kwargs):
        """
        Search against the collection using an image already in the
        collection and return any matches with corresponding scores.

        Arguments:

        - `filepath`, a filepath string of an image already in the collection
          as returned by a search or list operation.
        - `min_score`, minimum score that should be returned.
        - `offset`, offset of results from the start.
        - `limit`, maximum number of matches that should be returned.
        - `check_horizontal_flip`, whether to incorporate a horizontal flip check.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `overlay`, URL pointing to overlay image.
          + `filepath`, match image path.
        """
        params = {
            'filepath': filepath,
            'min_score': min_score,
            'offset': offset,
            'limit': limit,
            'check_horizontal_flip': check_horizontal_flip}

        return self._request('search', params, **kwargs)

    def search_url(
            self, url, min_score=0, offset=0, limit=10,
            check_horizontal_flip=False, **kwargs):
        """
        Search against the collection using an image URL
        and return any matches with corresponding scores.

        Arguments:

        - `url`, a URL string pointing to an image.
        - `min_score`, minimum score that should be returned.
        - `offset`, offset of results from the start.
        - `limit`, maximum number of matches that should be returned.
        - `check_horizontal_flip`, whether to incorporate a horizontal flip check.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `overlay`, URL pointing to overlay image.
          + `filepath`, match image path.
        """
        params = {
            'url': url,
            'min_score': min_score,
            'offset': offset,
            'limit': limit,
            'check_horizontal_flip': check_horizontal_flip}

        return self._request('search', params, **kwargs)

    def compare_image(self, image_1, image_2, min_score=0, check_horizontal_flip=False, **kwargs):
        """
        Given two images, compare them and return the match score if there
        is a match.

        Arguments:

        - `image_1`, an Image object representing the first image.
        - `image_2`, an Image object representing the second image.
        - `min_score`, minimum score that should be returned.
        - `check_horizontal_flip`, whether to incorporate a horizontal flip check.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `match_percent`, percent of image matching.
        """
        params = {
            'min_score': min_score,
            'check_horizontal_flip': check_horizontal_flip}

        image_params = {
            'image1': (image_1.collection_filepath, image_1.data),
            'image2': (image_2.collection_filepath, image_2.data)}

        return self._request('compare', params, image_params, **kwargs)

    def compare_url(self, url_1, url_2, min_score=0, check_horizontal_flip=False, **kwargs):
        """
        Given two images, compare them and return the match score if there
        is a match.

        Arguments:

        - `url_1`, a URL string pointing to the first image.
        - `url_2`, a URL string pointing to the second image.
        - `min_score`, minimum score that should be returned.
        - `offset`, offset of results from the start.
        - `limit`, maximum number of matches that should be returned.
        - `check_horizontal_flip`, whether to incorporate a horizontal flip check.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of dictionaries representing an image match.

          + `score`, relevance score.
          + `match_percent`, percent of image matching.
        """
        params = {
            'url1': url_1,
            'url2': url_2,
            'min_score': min_score,
            'check_horizontal_flip': check_horizontal_flip}

        return self._request('compare', params, **kwargs)
