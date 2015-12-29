#! /usr/bin/env python
# -*- coding: utf-8 -*-
class Index:
    '''
    generate ordered indices for given keys
    '''
    def __init__(self, begin = 0):
        self.__dict_key_idx = {}
        self.__dict_idx_key = {}
        self.__begin = begin
        self.__idx = begin
        self.__set = set()
    
    def add(self, key):
        self.__set.add(key)

    def index(self):
        if not self.__set:
            print 'already indexed!'
            return False
        for key in sorted(self.__set):
            self.__dict_key_idx[key] = self.__idx
            self.__dict_idx_key[self.__idx] = key
            self.__idx += 1
        self.__set = None
        return True

    def num_indices(self):
        return self.__idx - self.__begin

    def get_key_by_idx(self, idx):
        return self.__dict_idx_key.get(idx, None)

    def get_idx_by_key(self, key):
        return self.__dict_key_idx.get(key, -1)

