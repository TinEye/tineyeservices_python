# Copyright (c) 2012 Idee Inc. All rights reserved worldwide.

import requests

from exception import TinEyeServiceError, TinEyeServiceWarning
from image import Image
from requests.auth import HTTPBasicAuth

class TinEyeServiceRequest():
    """ Class to send requests to a TinEye servies API. """
    
    def __init__(self, api_url='http://localhost/rest/', username=None, password=None):
        self.api_url = api_url
        self.username = username
        self.password = password

    def _request(self, method, params, file_params=None):
        """ Make an HTTP request. """
        
        # Handle basic authentication if needed
        headers = {}
        auth = None
        if self.username is not None:
            auth = HTTPBasicAuth(self.username, self.password)

        response = None
        url = self.api_url + method + '/'
        if file_params == None:
            response = requests.get(url, params=params, auth=auth)
        else:
            response = requests.post(url, params=params, files=file_params, auth=auth)

        # Handle any HTTP errors
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        
        # Handle API errors
        if response.json['status'] == 'fail':
            raise TinEyeServiceError(response.json.get('error'))
        elif response.json['status'] == 'warn':
            raise TinEyeServiceWarning(response.json.get('error'))

        return response.json

    def delete(self, filepaths):
        """
        Delete images from the collection.
        
        Arguments:
        
        - `filepaths`, a list of string filepaths as returned by
          a search or list call.
              
        Returned:
        
        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        """
        params = {}
        counter = 0
            
        if not isinstance(filepaths, list):
            raise TypeError('Need to pass a list of filepaths')

        for filepath in filepaths:
            params['filepaths[%i]' % counter] = filepath
            counter += 1
        
        return self._request('delete', params)

    def count(self):
        """
        Get the number of items currently in the collection.

        Returned:
        
        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list containing the number of images in the collection.
        """
        return self._request('count', {})
        
    def list(self, offset=0, limit=20):
        """
        List the images present in the collection.

        Arguments:
        
        - `offset`, offset of results from the start.
        - `limit`, maximum number of images that should be returned.

        Returned:
        
        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list of filepaths.
        """
        return self._request('list', {'offset': offset, 'limit': limit})

    def ping(self):
        """
        Check whether the API search server is running.

        Returned:
        
        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        """
        return self._request('ping', {})
