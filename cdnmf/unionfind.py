#! /usr/bin/env python
# -*- coding: utf-8 -*-
class UnionFind:
    '''
    union find
    '''
    def __init__(self, n):
        self.__n = n
        self.__num_components = n
        self.__father = [i for i in range(n+1)]
        self.__rank = [1] * (n+1)

    def find(self, p):
        while p != self.__father[p]:
            self.__father[p] = self.__father[self.__father[p]]
            p = self.__father[p]
        return p

    def union(self, p, q):
        proot = self.find(p)
        qroot = self.find(q)
        if proot == qroot:
            return
        if self.__rank[proot] > self.__rank[qroot]:
            self.__father[qroot] = proot
            self.__rank[proot] += self.__rank[qroot]
        else:
            self.__father[proot] = qroot
            self.__rank[qroot] += self.__rank[proot]
        self.__num_components -= 1

    def gc_vertices(self):
        '''
        get all the vertices in the giant component
        '''
        idx_gc = 0
        num_gc = 0
        for i in range(1, self.__n + 1):
            root = self.find(i)
            if self.__rank[root] > num_gc:
                idx_gc = root
                num_gc = self.__rank[root]
        
        from glb import log, logging
        log = logging.getLogger(__name__)
        log.info('%d, giant_component/total: %d/%d.' % (self.__num_components, num_gc, self.__n))
        set_vtx = set()
        for i in range(1, self.__n + 1):
            if self.find(i) == idx_gc:
                set_vtx.add(i)
        return set_vtx

    def num_components(self):
        return self.__num_components

