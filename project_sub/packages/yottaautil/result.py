#!/user/bin/env python
# -*- coding:utf-8 -*- 

'''
Created on 2014.11.25

@author: chao.han@yottaa.com
'''

class Result(object):
    '''
    the base class for checker steps and case
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._result = False  # every case init status false
        self._result_message = ""  # record result message give more information than result
        
    def get_result(self):
        return self._result
    
    def set_result(self, result):
        self._result = result
    
    def get_result_message(self):
        return self._result_message
    
    def set_result_message(self, result_message):
        self._result_message = result_message
