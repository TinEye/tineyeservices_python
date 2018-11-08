# -*- coding: utf-8 -*-
# Copyright (c) 2018 TinEye. All rights reserved worldwide.

import os
import sys
import unittest

from tineyeservices import MatchEngineRequest
from tineyeservices import Image
from tineyeservices.exception import TinEyeServiceError, TinEyeServiceWarning

imagepath = os.path.abspath("test/images")
sys.path.append('../')


class TestMatchEngine(unittest.TestCase):
    """ Test MatchEngineRequest class. """

    def setUp(self):
        self.request = MatchEngineRequest(api_url='http://staging02.tc:5001/rest/')
        r = self.request.list(limit=1000)
        if len(r['result']) > 0:
            r = self.request.delete(r['result'])

    def tearDown(self):
        r = self.request.list(limit=1000)
        if len(r['result']) > 0:
            r = self.request.delete(r['result'])

    def test_add(self):
        # Image upload
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='folder/banana.jpg'),
                  Image(filepath='%s/banana_flip.jpg' % imagepath, collection_filepath='banana_flip.jpg')]
        r = self.request.add_image(images)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'add')
        self.assertEqual(r['error'], [])
        self.assertEqual(r['result'], [])

        r = self.request.list()
        self.assertEqual(r['result'], ['folder/banana.jpg', 'banana_flip.jpg'])

        # URL
        images = [Image(url='https://tineye.com/images/meloncat.jpg')]
        r = self.request.add_url(images)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'add')
        self.assertEqual(r['error'], [])
        self.assertEqual(r['result'], [])

        r = self.request.list()
        self.assertEqual(r['result'], ['folder/banana.jpg', 'banana_flip.jpg', 'meloncat.jpg'])

    def test_delete(self):
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='folder/banana.jpg'),
                  Image(filepath='%s/banana_flip.jpg' % imagepath, collection_filepath='banana_flip.jpg')]
        r = self.request.add_image(images)
        self.assertEqual(r['status'], 'ok')

        r = self.request.delete(['folder/banana.jpg'])
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'delete')
        self.assertEqual(r['error'], [])
        self.assertEqual(r['result'], [])

        r = self.request.list()
        self.assertEqual(r['result'], ['banana_flip.jpg'])

        # Try deleting a file not in the collection
        try:
            self.request.delete(['banana_flip.jpg', 'folder/banana.jpg'])
        except TinEyeServiceWarning as e:
            self.assertEqual(e.args[0], ['folder/banana.jpg: Failed to remove from index.'])

        r = self.request.list()
        self.assertEqual(r['result'], [])

    def test_search(self):
        # Image upload
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg')]
        r = self.request.add_image(images)
        self.assertEqual(r['status'], 'ok')

        image = Image('%s/banana.png' % imagepath)
        r = self.request.search_image(image)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'search')
        self.assertEqual(r['error'], [])
        self.assertEqual(len(r['result']), 1)
    
        # URL
        images = [Image(url='https://tineye.com/images/meloncat.jpg')]
        r = self.request.add_url(images)
        self.assertEqual(r['status'], 'ok')

        r = self.request.search_url('https://tineye.com/images/meloncat.jpg')
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'search')
        self.assertEqual(r['error'], [])
        if len(r['result']) > 0:
            self.assertTrue(r['result'][0]['score'] > 90)
        self.assertEqual(len(r['result']), 1)

        # Test bad URL
        try:
            r = self.request.search_url('https://tineye.com/404')
        except TinEyeServiceError as e:
            self.assertEqual(e.args[0], ['https://tineye.com/404: Failed to download file.'])

        # Filepath
        r = self.request.search_filepath('meloncat.jpg')
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'search')
        self.assertEqual(r['error'], [])
        if len(r['result']) > 0:
            self.assertTrue(float(r['result'][0]['score']) > 90)
        self.assertEqual(len(r['result']), 1)

        # Test min score
        image = Image('%s/banana.png' % imagepath)
        r = self.request.search_image(image, min_score=70)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'search')
        self.assertEqual(r['error'], [])
        self.assertEqual(len(r['result']), 1)

        # Test offset and limit
        image = Image('%s/banana.png' % imagepath)
        r = self.request.search_image(image, offset=0, limit=1)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'search')
        self.assertEqual(r['error'], [])
        self.assertEqual(len(r['result']), 1)

    def test_compare(self):
        # Image upload
        image_1 = Image(filepath='%s/banana.jpg' % imagepath)
        image_2 = Image(filepath='%s/banana_flip.jpg' % imagepath)
        r = self.request.compare_image(image_1, image_2, check_horizontal_flip=False)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'compare')
        self.assertEqual(r['error'], [])
        self.assertEqual(len(r['result']), 0)

        # With flip enabled
        r = self.request.compare_image(image_1, image_2, check_horizontal_flip=True)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'compare')
        self.assertEqual(r['error'], [])
        self.assertEqual(len(r['result']), 1)

        # Flip disabled
        r = self.request.compare_image(image_1, image_2, min_score=100, check_horizontal_flip=True)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'compare')
        self.assertEqual(r['error'], [])
        self.assertEqual(len(r['result']), 0)

        # URL
        r = self.request.compare_url(
            'https://tineye.com/images/meloncat.jpg',
            'https://tineye.com/images/meloncat.jpg',
            min_score=100)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'compare')
        self.assertEqual(r['error'], [])
        self.assertEqual(len(r['result']), 1)

    def test_count(self):
        # No images
        r = self.request.count()
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'count')
        self.assertEqual(r['error'], [])
        self.assertEqual(r['result'][0], 0)

        images = [Image(filepath='%s/banana.png' % imagepath, collection_filepath='banana.png'),
                  Image(filepath='%s/banana_flip.jpg' % imagepath)]
        r = self.request.add_image(images)
        self.assertEqual(r['status'], 'ok')

        # Added two images
        r = self.request.count()
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'count')
        self.assertEqual(r['error'], [])
        self.assertEqual(r['result'][0], 2)

        r = self.request.delete(['banana.png'])
        self.assertEqual(r['status'], 'ok')

        # Deleted one image
        r = self.request.count()
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'count')
        self.assertEqual(r['error'], [])
        self.assertEqual(r['result'][0], 1)

    def test_list(self):
        # No images
        r = self.request.list()
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'list')
        self.assertEqual(r['error'], [])
        self.assertEqual(r['result'], [])

        # Added one image
        images = [Image(filepath='%s/banana.png' % imagepath, collection_filepath='banana.png')]
        r = self.request.add_image(images)
        self.assertEqual(r['status'], 'ok')

        r = self.request.list()
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'list')
        self.assertEqual(r['error'], [])
        self.assertEqual(r['result'], ['banana.png'])

    def test_ping(self):
        # Ping!
        r = self.request.ping()
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['method'], 'ping')
