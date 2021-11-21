import os
from typing import Dict
import requests
import socket
import json

class Request(object):

    def __init__(self):
        self.__atrib__ = ['url', 
                          'headers',
                          'auth',
                          'stream',
                          'verify',
                          'proxies', 
                          'adapters', 
                          'cert', 
                          'cookies', 
                          'hooks', 
                          'redirect_cache']
    
    def is_connected(self):
        try:
            host = socket.gethostbyname("one.one.one.one")
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            pass
        return False
        
    def get(self, url, **kwargs):
        
        invalid_argument = [i for i in kwargs.keys() if i not in self.__atrib__]

        if len(invalid_argument) > 0:
            raise TypeError(f"Invalid arguments: {', '.join(invalid_argument)}")

        if self.is_connected():
            try:
                response = requests.get(url = url, 
                                        headers = kwargs.get('headers'),
                                        auth = kwargs.get('auth'),
                                        proxies = kwargs.get('proxies'), 
                                        cert = kwargs.get('cert'), 
                                        cookies = kwargs.get('cookies'), 
                                        hooks = kwargs.get('hooks'),
                                        stream = kwargs.get('stream'),
                                        verify = kwargs.get('verify'))

                if response.ok:
                    return response
                else:
                    response.raise_for_status()

            except Exception as exception:
                raise TypeError(exception)
        else:
            raise TypeError("No internet connect")

        
