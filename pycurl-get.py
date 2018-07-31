# -*- coding: utf-8 -*-
'''
This is an attempt to create a usable box api library based on the
pycurl module
'''

import pycurl
import certifi
import atexit
import os

from io import BytesIO

DEFAULT_OPTIONS = {pycurl.CAINFO : certifi.where(),
                   pycurl.FOLLOWLOCATION : 1,
                   pycurl.MAXREDIRS : 5,
                   pycurl.SSL_VERIFYPEER : 1,
                   pycurl.SSL_VERIFYHOST : 2}

# global inits
os.environ.update({'SSLKEYLOGFILE' : './sslkeys.log'})
atexit.register(pycurl.global_cleanup)
pycurl.global_init(pycurl.GLOBAL_SSL)



class Session:
    ''' Session class for api requests based on pycurl '''
    def __init__(self):
        self._session = pycurl.Curl()
        self._options = {}
        self.set_options(DEFAULT_OPTIONS)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def set_option(self, option, value):
        self._session.setopt(option, value)
        self._options.update({option : value})

    def get_option(self, option):
        try:
            return self._options[option]
        except ValueError:
            return None

    def unset_option(self, option):
            if self.get_option(option):
                self._session.unsetopt(option)
            
    def set_options(self, options):
        for option, value in options.items():
            self.set_option(option, value)

    def get_options(self):
        return self._options    

    def request(self, method, *args, **kwargs):
        methods = {'GET' : self.get,
                  }
        return methods[method](*args, **kwargs)

    def get(self, url, **kwargs):
        buffer = BytesIO()
        self.set_option(pycurl.URL, url)
        if kwargs:
            headers = [ option + ': ' + value for option, value in kwargs['headers'].items()]
            self.set_option(pycurl.HTTPHEADER, headers)
        self.set_option(pycurl.WRITEDATA, buffer)
        self._session.perform()
        return buffer.getvalue()

if __name__ == '__main__':
    options = {pycurl.VERBOSE : True}
    
    with Session() as ses:
        ses.set_options(options)
        
        ses.get('http://www.box.net/')
