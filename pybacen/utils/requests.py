import os
import asyncio
import warnings
from typing import Dict, List
import codecs
import json
import re
import socket
import aiohttp
from io import StringIO, BytesIO
import nest_asyncio
import numpy as np

from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    FrozenSet,
    Generator,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

nest_asyncio.apply()

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
    
    @classmethod
    def is_connected(self) -> bool:
        try:
            host = socket.gethostbyname("one.one.one.one")
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            pass
        return False

    @classmethod
    def get_tasks(self, session, urls: list, *args, **kwargs) -> any:
        tasks = []

        for url in urls:
            tasks.append(session.get(url, *args, **kwargs))
        return tasks

    def get(self, urls: List, *args, **kwargs) -> any:

        _async_responses = []

        async def async_get(urls, **kwargs: Optional[Any]):

            async with aiohttp.ClientSession() as session:
                
                try:
                    tasks = self.get_tasks(session= session, urls=urls, **kwargs)
                except Exception as exception:
                    raise TypeError(exception)

                #responses = []
                #for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='Processing: '):
                #    responses.append(await f)
                
                responses = await asyncio.gather(*tasks)
                
                for _response in responses:

                    _result = []

                    _result.append(_response.url)

                    if 'application/json' in _response.headers['content-type']:
                        _result.append(await _response.text()) 
                    elif 'text/csv' in _response.headers['content-type'] \
                      or 'text/plain' in _response.headers['content-type'] \
                      or 'application/octet-stream' in _response.headers['content-type']:
                      _result.append(await _response.content.read())

                    _result.append(_response.status)
                    _result.append(_response.headers['content-type'])
                    
                    _async_responses.append(_result)
                          
        if self.is_connected():

            try:
                 
                asyncio.run(async_get(urls, **kwargs))

                return np.array(_async_responses)

            except Exception as exception:
                raise TypeError(exception)
        else:
            raise TypeError("No internet connect")