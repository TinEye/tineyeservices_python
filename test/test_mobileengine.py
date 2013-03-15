# Copyright (c) 2012-2013 Idee Inc. All rights reserved worldwide.

import sys
sys.path.append('../')

import contextlib
import os
import unittest

import TestMatchEngine

from tineyeservices import MobileEngineRequest
from tineyeservices import Image
from tineyeservices.exception import TinEyeServiceError, TinEyeServiceWarning

imagepath = os.path.abspath("test/images")

class TestMobileEngine(TestMatchEngine):
    """
    Test MobileEngineRequest class, which are the same tests
    as MatchEngine's for now.
    """
    
    def setUp(self):
        self.request = MobileEngineRequest(api_url='http://localhost:5000/rest/')
        r = self.request.list(limit=1000)
        if len(r['result']) > 0:
            r = self.request.delete(r['result'])

    def tearDown(self):
        r = self.request.list(limit=1000)
        if len(r['result']) > 0:
            r = self.request.delete(r['result'])
