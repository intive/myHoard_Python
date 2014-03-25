from abc import ABCMeta, abstractmethod


class BaseAuthenticator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def authenticate(self):
        pass