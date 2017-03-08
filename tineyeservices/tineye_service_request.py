# Copyright (c) 2017 TinEye. All rights reserved worldwide.

import requests
from exception import TinEyeServiceError, TinEyeServiceWarning
from requests.auth import HTTPBasicAuth


class TinEyeServiceRequest(object):
    """ Class to send requests to a TinEye servies API. """

    def __init__(self, api_url='http://localhost/rest/', username=None, password=None):

        # The API URL must end in /rest/, if it does not, suggest a URL
        if not api_url.endswith('/rest/'):
            correction = '/rest/'
            if api_url.endswith('/'):
                correction = 'rest/'
            error = ("The API URL must end with %s (are you sure you didn't mean "
                     "%s%s?)" % (correction, api_url, correction))
            raise TinEyeServiceWarning(error)

        self.api_url = api_url
        self.username = username
        self.password = password

    def _request(self, method, params, file_params=None, **kwargs):
        """ Make an HTTP request. """

        # Handle basic authentication if needed
        auth = None
        if self.username is not None:
            auth = HTTPBasicAuth(self.username, self.password)

        # Check for timeout and pass to requests too
        timeout = kwargs.get('timeout', None)

        # Pass the extra arguments as parameters to the call
        params.update(kwargs)

        response = None
        url = self.api_url + method + '/'
        if file_params is None:
            response = requests.get(url, params=params, auth=auth, timeout=timeout)
        else:
            response = requests.post(
                url, params=params, files=file_params, auth=auth, timeout=timeout)
        response_json = response.json()

        # Handle any HTTP errors
        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        # Handle API errors.
        # No, let the caller see everything.  Doing this may lose info.
        #if response_json['status'] == 'fail':
        #    raise TinEyeServiceError(response_json.get('error'))
        #elif response_json['status'] == 'warn':
        #    raise TinEyeServiceWarning(response_json.get('error'))

        return response_json

    def delete(self, filepaths, **kwargs):
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

        return self._request('delete', params, **kwargs)

    def count(self, **kwargs):
        """
        Get the number of items currently in the collection.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        - `result`, a list containing the number of images in the collection.
        """
        return self._request('count', {}, **kwargs)

    def list(self, offset=0, limit=20, **kwargs):
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
        return self._request('list', {'offset': offset, 'limit': limit}, **kwargs)

    def ping(self, **kwargs):
        """
        Check whether the API search server is running.

        Returned:

        - `status`, one of ok, warn, fail.
        - `error`, describes the error if status is not set to ok.
        """
        return self._request('ping', {}, **kwargs)
