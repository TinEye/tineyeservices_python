# -*- coding: utf-8 -*-
# Copyright (c) 2018 TinEye. All rights reserved worldwide.

from .mobileengine_request import MobileEngineRequest


class WineEngineRequest(MobileEngineRequest):
    """
    Class to send requests to a WineEngine API.

    Adding an image using data:

        >>> from tineyeservices import WineEngineRequest, Image
        >>> api = WineEngineRequest(api_url='http://localhost/rest/')
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
        return "WineEngineRequest(api_url=%r, username=%r, password=%r)" %\
               (self.api_url, self.username, self.password)
