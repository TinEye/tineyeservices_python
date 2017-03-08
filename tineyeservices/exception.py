# Copyright (c) 2017 TinEye. All rights reserved worldwide.


class TinEyeServiceException(Exception):
    """ Base class for all TinEye Services exceptions. """
    pass


class TinEyeServiceError(TinEyeServiceException):
    pass


class TinEyeServiceWarning(TinEyeServiceException):
    pass
