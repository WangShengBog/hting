# -*-coding: UTF-8 -*-

import logging


logger = logging.getLogger(__name__)

__author__ = 'bog'


def get_url():
    pass
    return 200, {'url': "www.baidu.com"}


def test():
    print('starttest-------')
    inner()
    print('endtest---------')



def inner():
    try:
        print('inner--------')
        raise Exception('innerException')
    except Exception as e:
        print('inner excep try ')
        raise
        print('inner after raise')


if __name__ == '__main__':
    try:
        test()
    except Exception as e:
        print('test: except')