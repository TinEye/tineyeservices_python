# Copyright (c) 2017 TinEye. All rights reserved worldwide.

from matchengine_request import MatchEngineRequest


class MobileEngineRequest(MatchEngineRequest):
    """
    Class to send requests to a MobileEngine API.

    Adding an image using data:

        >>> from tineyeservices import MobileEngineRequest, Image
        >>> api = MobileEngineRequest(api_url='http://localhost/rest/')
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
        return "MobileEngineRequest(api_url=%r, username=%r, password=%r)" %\
               (self.api_url, self.username, self.password)
