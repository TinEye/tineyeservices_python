# Copyright (c) 2012-2013 Idee Inc. All rights reserved worldwide.

import sys
sys.path.append('../')

import contextlib
import os
import unittest
import simplejson

from tineyeservices import MulticolorEngineRequest
from tineyeservices import Image
from tineyeservices.exception import TinEyeServiceError, TinEyeServiceWarning

imagepath = os.path.abspath("test/images")

metadata_json = {"keywords": ["whale", "shark", "octopus"], "id": {"action": "return", "type": "uint", "": "12345"}}
metadata = simplejson.dumps(metadata_json)

search_metadata_json = {"keywords": "whale"}
search_metadata = simplejson.dumps(search_metadata_json)

class TestMulticolorEngine(unittest.TestCase):
    """ Test MulticolorEngineRequest class. """
        
    def setUp(self):
        self.request = MulticolorEngineRequest(api_url='http://localhost:5000/rest/')
        r = self.request.list()
        if len(r['result']) > 0:
            r = self.request.delete(r['result'])

    def tearDown(self):
        r = self.request.list()
        if len(r['result']) > 0:
            r = self.request.delete(r['result'])

    def test_add(self):
        # Image upload
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='folder/banana.jpg'),
                  Image(filepath='%s/banana_flip.jpg' % imagepath, collection_filepath='banana_flip.jpg')]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'add')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], [])
        
        # Image upload with metadata
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='folder/banana.jpg', metadata=metadata),
                  Image(filepath='%s/banana_flip.jpg' % imagepath, collection_filepath='banana_flip.jpg', metadata=metadata)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'add')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], [])
        
        r = self.request.list()
        self.assertEquals(r['result'], ['folder/banana.jpg', 'banana_flip.jpg'])
        
        # URL
        images = [Image(url='http://www.tineye.com/images/meloncat.jpg')]
        r = self.request.add_url(images)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'add')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], [])
        
        # URL with metadata
        images = [Image(url='http://www.tineye.com/images/meloncat.jpg', metadata=metadata)]
        r = self.request.add_url(images)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'add')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], [])
        
        r = self.request.list()
        self.assertEquals(r['result'], ['folder/banana.jpg', 'banana_flip.jpg', 'meloncat.jpg'])

    def test_delete(self):
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='folder/banana.jpg'),
                  Image(filepath='%s/banana_flip.jpg' % imagepath, collection_filepath='banana_flip.jpg')]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        
        r = self.request.delete(['folder/banana.jpg'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'delete')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], [])

        r = self.request.list()
        self.assertEquals(r['result'], ['banana_flip.jpg'])

        # Try deleting a file not in the collection
        try:
            self.request.delete(['banana_flip.jpg', 'folder/banana.jpg'])
        except TinEyeServiceWarning, e:
            self.assertEquals(e.args[0], ['folder/banana.jpg: Failed to remove from index.'])

        r = self.request.list()
        self.assertEquals(r['result'], [])

    def test_search(self):
        # Image upload
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg', metadata=metadata)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')

        image = Image('%s/banana.png' % imagepath)
        r = self.request.search_image(image, metadata=search_metadata)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        self.assertEquals(len(r['result']), 1)
    
        # URL
        images = [Image(url='http://www.tineye.com/images/meloncat.jpg')]
        r = self.request.add_url(images)
        self.assertEquals(r['status'], 'ok')

        r = self.request.search_url('http://www.tineye.com/images/meloncat.jpg')
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        if len(r['result']) > 0:
            self.assertEquals(r['result'][0]['score'], '100.00')
        self.assertEquals(len(r['result']), 1)

        # Test bad URL
        try:
            r = self.request.search_url('http://www.tineye.com/404')
        except TinEyeServiceError, e:
            self.assertEquals(e.args[0], ['http://www.tineye.com/404: Failed to download file.'])

        # Filepath
        r = self.request.search_filepath('meloncat.jpg')
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        if len(r['result']) > 0:
            self.assertTrue(float(r['result'][0]['score']) > 80)
        self.assertEquals(len(r['result']), 1)

        # Colors
        r = self.request.search_color(['243,249,22'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        print r
        self.assertEquals(len(r['result']), 1)

        # Colors without enough weights
        try:
            self.request.search_color(['243,249,22', 'aaaaaa', 'ffffff'], ['2'])
        except TinEyeServiceError, e:
            self.assertEquals(e.args[0], ['Please specify the same number of weights as colors.'])

        # Colors and weights
        r = self.request.search_color(['243,249,22', 'ffffff'], ['1', '2', '3'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        self.assertEquals(len(r['result']), 1)

        # Test min score and ignore background
        image = Image('%s/banana.png' % imagepath)
        r = self.request.search_image(image, min_score=10, ignore_background=True,
                                      ignore_interior_background=False)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        self.assertEquals(len(r['result']), 1)

        image = Image('%s/banana.png' % imagepath)
        r = self.request.search_image(image, min_score=10, ignore_background=False,
                                      ignore_interior_background=True)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        self.assertEquals(len(r['result']), 1)

        # Test offset and limit
        image = Image('%s/banana.png' % imagepath)
        r = self.request.search_image(image, offset=1, limit=1)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        self.assertEquals(len(r['result']), 0)

        # Try getting metadata when there are no images
        try:
            r = self.request.search_metadata(metadata=search_metadata, return_metadata=simplejson.dumps((['id'])))
        except TinEyeServiceError, e:
            self.assertTrue(e.args[0], 'The return metadata tag "tag" is missing from the per-item index')
        
        # Add two images with metadata and search for images sorted by ascending id
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg', metadata=metadata),
                  Image(filepath='%s/banana_flip.jpg' % imagepath, collection_filepath='banana_flip.jpg', metadata=metadata)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')

        r = self.request.search_metadata(metadata=search_metadata, return_metadata=simplejson.dumps(['id']))

        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'color_search')
        self.assertEquals(r['error'], [])
        self.assertEquals(len(r['result']), 2)
        self.assertEquals(r['result'][0]['metadata']['id'], '12345')

    def test_count_image_colors(self):        
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg')]

        # Image upload
        r = self.request.count_image_colors_image(images=images, count_colors=['255, 255, 255'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count_image_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 0)
        self.assertEquals(r['result'][0]['color'], [255, 255, 255])
        self.assertEquals(r['result'][0]['name'], 'White')
        self.assertEquals(r['result'][0]['class'], 'White')
        self.assertTrue('num_images_full_area' in r['result'][0])
        self.assertTrue('num_images_partial_area' in r['result'][0])

        # Image URL
        urls=['http://www.tineye.com/images/meloncat.jpg']
        r = self.request.count_image_colors_url(urls=urls, count_colors=['88, 112, 14'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count_image_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 0)
        self.assertEquals(r['result'][0]['color'], [88, 112, 14])
        self.assertEquals(r['result'][0]['name'], 'Fiji Green')
        self.assertEquals(r['result'][0]['class'], 'Green')
        self.assertTrue('num_images_full_area' in r['result'][0])
        self.assertTrue('num_images_partial_area' in r['result'][0])

    def test_count_collection_colors(self):        
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg', metadata=metadata)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')

        r = self.request.count_collection_colors_filepath(filepaths=['banana.jpg'], count_colors=['242,246,27'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 0)
        self.assertEquals(r['result'][0]['color'], [242, 246, 27])
        self.assertEquals(r['result'][0]['name'], 'Lemon')
        self.assertEquals(r['result'][0]['class'], 'Yellow')
        self.assertTrue('num_images_full_area' in r['result'][0])
        self.assertTrue('num_images_partial_area' in r['result'][0])

        r = self.request.count_collection_colors_colors(colors=['242, 246, 27'], count_colors=['123, 235, 27'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 0)
        self.assertEquals(r['result'][0]['color'], [123, 235, 27])
        self.assertEquals(r['result'][0]['name'], 'Lawn Green')
        self.assertEquals(r['result'][0]['class'], 'Green')
        self.assertTrue('num_images_full_area' in r['result'][0])
        self.assertTrue('num_images_partial_area' in r['result'][0])

        r = self.request.count_collection_colors_metadata(metadata=search_metadata, count_colors=['123, 235, 27'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 0)
        self.assertEquals(r['result'][0]['color'], [123, 235, 27])
        self.assertEquals(r['result'][0]['name'], 'Lawn Green')
        self.assertEquals(r['result'][0]['class'], 'Green')
        self.assertTrue('num_images_full_area' in r['result'][0])
        self.assertTrue('num_images_partial_area' in r['result'][0])

        r = self.request.count_collection_colors(count_colors=['123, 235, 27'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 0)
        self.assertEquals(r['result'][0]['color'], [123, 235, 27])
        self.assertEquals(r['result'][0]['name'], 'Lawn Green')
        self.assertEquals(r['result'][0]['class'], 'Green')
        self.assertTrue('num_images_full_area' in r['result'][0])
        self.assertTrue('num_images_partial_area' in r['result'][0])

    def test_extract_image_colors(self):        
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg')]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        
        # Image upload, rgb
        r = self.request.extract_image_colors_image([images[0]], limit=5)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_image_colors')
        self.assertEquals(r['error'], [])
        self.assertEquals(len(r['result']), 5)
        self.assertTrue(isinstance(r['result'][0]['color'], list))

        # Image upload, hex
        r = self.request.extract_image_colors_image([images[0]], color_format='hex', limit=10)
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_image_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 5) 
        self.assertEquals(len(r['result'][0]['color']), 6)

        # URL, rgb
        r = self.request.extract_image_colors_url(['http://www.tineye.com/images/meloncat.jpg'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_image_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 5)
        self.assertTrue(isinstance(r['result'][0]['color'], list))
        
        # URL, hex
        r = self.request.extract_image_colors_url(['http://www.tineye.com/images/meloncat.jpg'], color_format='hex')
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_image_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 5)
        self.assertEquals(len(r['result'][0]['color']), 6)

    def test_extract_collection_colors(self):
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg', metadata=metadata)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        
        # Collection, rgb
        r = self.request.extract_collection_colors()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 1) 
        self.assertTrue(isinstance(r['result'][0]['color'], list))

        # Filepath, rgb
        r = self.request.extract_collection_colors_filepath(['banana.jpg'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 1)  
        self.assertTrue(isinstance(r['result'][0]['color'], list))

        # Filepath, hex
        r = self.request.extract_collection_colors_filepath(['banana.jpg'], color_format='hex')
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 1)  
        self.assertEquals(len(r['result'][0]['color']), 6)

        # Metadata, rgb
        r = self.request.extract_collection_colors_metadata(search_metadata, color_format='hex')
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertTrue(len(r['result']) > 1)  
        self.assertEquals(len(r['result'][0]['color']), 6)

        # Colors, rgb
        r = self.request.extract_collection_colors_colors(colors=['123456'], color_format='hex')
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'extract_collection_colors')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], [])

    def test_get_metadata(self):
        # Add an image with metadata first and then get it back
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg', metadata=metadata)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')

        r = self.request.get_metadata(['banana.jpg'])
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'get_metadata')
        self.assertEquals(r['error'], [])
        r_metadata = r['result'][0]['metadata']['keywords']
        keywords = r_metadata['']
        self.assertTrue('whale' in keywords)
        self.assertTrue('octopus' in keywords)
        self.assertTrue('shark' in keywords)
        self.assertTrue(r_metadata['action'], 'search')
        self.assertTrue(r_metadata['type'], 'string')

    def test_get_search_metadata(self):
        # Try getting metadata when there are no images
        try:
            r = self.request.get_search_metadata()
        except TinEyeServiceWarning, e:
            self.assertEquals(e.args[0], [u'Failed to get the search metadata from index.'])
        
        # Add an image with metadata first then get data that can be searched for
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg', metadata=metadata)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        
        r = self.request.get_search_metadata()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'get_search_metadata')
        self.assertEquals(r['error'], [])
        self.assertTrue('keywords' in r['result'][0]['metadata'])
        keywords = r['result'][0]['metadata']['keywords']['']
        self.assertTrue('whale' in keywords)
        self.assertTrue('octopus' in keywords)
        self.assertTrue('shark' in keywords)
        
    def test_get_return_metadata(self):
        # Try getting metadata when there are no images
        try:
            r = self.request.get_return_metadata()
        except TinEyeServiceWarning, e:
            self.assertEquals(e.args[0], [u'Failed to get the return metadata from index.'])
        
        # Add an image with metadata first then get data that can be returned
        images = [Image(filepath='%s/banana.jpg' % imagepath, collection_filepath='banana.jpg', metadata=metadata)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        
        r = self.request.get_return_metadata()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'get_return_metadata')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], [{'metadata': {'id': {'count': '1', '': None, 'type': 'uint'}}}])
        
    def test_count(self):
        # No images
        r = self.request.count()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'][0], 0)

        images = [Image(filepath='%s/banana.png' % imagepath, collection_filepath='banana.png'),
                  Image(filepath='%s/banana_flip.jpg' % imagepath)]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        
        # Added two images
        r = self.request.count()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'][0], 2)
        
        r = self.request.delete(['banana.png'])
        self.assertEquals(r['status'], 'ok')
 
        # Deleted one image
        r = self.request.count()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'count')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'][0], 1)

    def test_list(self):
        # No images
        r = self.request.list()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'list')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], [])

        # Added one image
        images = [Image(filepath='%s/banana.png' % imagepath, collection_filepath='banana.png')]
        r = self.request.add_image(images)
        self.assertEquals(r['status'], 'ok')
        
        r = self.request.list()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'list')
        self.assertEquals(r['error'], [])
        self.assertEquals(r['result'], ['banana.png'])

    def test_ping(self):
        # Ping!
        r = self.request.ping()
        self.assertEquals(r['status'], 'ok')
        self.assertEquals(r['method'], 'ping')
