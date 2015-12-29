#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from index import Index
from glb import logging
log = logging.getLogger(__name__)

class Node:
    '''node for graph'''
    def __init__(self, name):
        self.name = name
        self.actual = -1
        self.expected = -1
        self.extra = {'status': -1, 'visited': []}
        self.clusters = set()
        self.neighbor = set()
        self.__degree = 0

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbor:
            self.neighbor.add(neighbor)
            self.__degree += 1

    def get_degree(self):
        return self.__degree

class Graph:
    '''graph'''
    def __init__(self):
        self.__n = 0
        self.__nodes = []
        self.index = Index()

    def add(self, name):
        self.index.add(name)

    def indexing(self):
        if not self.index.index():
            return
        self.__n = self.index.num_indices()
        for i in range(self.__n):
            node = Node(self.index.get_key_by_idx(i))
            self.__nodes.append(node)
    
    def add_edge(self, a, b):
        a = self.index.get_idx_by_key(a)
        b = self.index.get_idx_by_key(b)
        self.__nodes[a].add_neighbor(b)
        self.__nodes[b].add_neighbor(a)

    def nodes(self):
        return self.__nodes

    def n(self):
        return self.__n
    
    def adjmatrix(self):
        m = [[0]*self.__n for _ in range(self.__n)]
        for i in range(self.__n):
            for j in self.__nodes[i].neighbor:
                m[i][j] = 1
        return np.asmatrix(m)
    
    def tryoutliers(self, cluster):
        import time
        from collections import deque
        start = time.time()
        q = deque()
        for i in range(self.__n):
            if self.__nodes[i].extra['status'] == 0:# and len(self.__nodes[i].clusters) == 1:
                q.append(i)
                #break
        while q:
            p = q.popleft()
            pclusters = self.__nodes[p].clusters
            for i in self.__nodes[p].neighbor:
                if self.__nodes[i].extra['status'] >= 0 or p in self.__nodes[i].extra['visited']:
                    continue
                self.__nodes[i].clusters |= pclusters
                self.__nodes[i].extra['visited'].append(p)
                if len(self.__nodes[i].extra['visited']) == self.__nodes[i].get_degree():
                    self.__nodes[i].extra['status'] = 1
                elif len(self.__nodes[i].clusters) == cluster:
                    self.__nodes[i].extra['status'] = 2
                else:
                    q.append(i)            
        log.info('try outliers: {}'.format(time.time() - start))
        
        list_multiple = []
        for i in range(self.__n):
            if len(self.__nodes[i].clusters) == 1:
                self.__nodes[i].actual = list(self.__nodes[i].clusters)[0]
            elif len(self.__nodes[i].clusters) > 1:
                list_multiple.append(i)
            else:
                self.__nodes[i].clusters |= set(range(cluster))
                list_multiple.append(i)
                #raise ValueError('node %d has no potential cluster!' % i)
        log.info('%d nodes have at least two clusters.' % len(list_multiple))
        return list_multiple

    def modularity(self):
        Q = 0.0
        M = 0.0
        for i in range(self.n()):
            M += self.__nodes[i].get_degree()
        for i in range(self.n()):
            visited = [True] * self.n()
            for j in self.__nodes[i].neighbor:
                visited[j] = False
                if self.__nodes[i].actual == self.__nodes[j].actual:
                    Q += 1 - self.__nodes[i].get_degree() * self.__nodes[j].get_degree() * 1.0 / M
            for j in range(self.n()):
                if visited[j] and self.__nodes[i].actual == self.__nodes[j].actual:
                    Q -= self.__nodes[i].get_degree() * self.__nodes[j].get_degree() * 1.0 / M
        return Q / M
        
    def dump(self, opt):
        def dft(obj):
            if isinstance(obj, set):
                return sorted(obj)
            elif isinstance(obj , (Index, Node)):
                return obj.__dict__
        import json
        json.dump(self.__dict__, open(opt, 'w'), default=dft, indent=4, sort_keys=True)
            
