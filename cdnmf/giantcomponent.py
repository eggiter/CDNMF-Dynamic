#! /usr/bin/env python
# -*- coding: utf-8 -*-
from index import Index
from unionfind import UnionFind

def reindex(ipt, begin = 0):
    idx_vertex = Index(begin)
    lines = open(ipt, 'r').readlines()
    lines = map(lambda x : x.split(), lines)
    for line in filter(lambda x : len(x) >= 2, lines):
        idx_vertex.add(int(line[0]))
        idx_vertex.add(int(line[1]))

    idx_vertex.index()
    return idx_vertex

def gen_gc(ipt, opt):
    idx_orign =  reindex(ipt, 1)
    uf = UnionFind(idx_orign.num_indices())
    lines = open(ipt, 'r').readlines()
    lines = map(lambda x : x.split(), lines)
    lines = filter(lambda x : len(x) >= 2, lines)
    for line in lines: 
        a = idx_orign.get_idx_by_key(int(line[0]))
        b = idx_orign.get_idx_by_key(int(line[1]))
        if a != -1 and b != -1:
            uf.union(a, b)
    set_gc = uf.gc_vertices()
    writer = open(opt, 'w')
    for line in lines:
        a = idx_orign.get_idx_by_key(int(line[0]))
        b = idx_orign.get_idx_by_key(int(line[1]))
        if a in set_gc and b in set_gc:
            write = line
            writer.write(' '.join(map(lambda x:str(x), write)) + '\n')
            
    from glb import log, logging
    log = logging.getLogger(__name__)
    log.info('giant component has been written to file.')

if __name__ == '__main__':
    import os
    from glb import basepath
    ipt = os.path.join(basepath, 'data/test/2006-9~2006-9_edges.txt')
    opt = os.path.join(basepath, 'data/test/2006-9~2006-9_edges.gc')
    gen_gc(ipt, opt)

