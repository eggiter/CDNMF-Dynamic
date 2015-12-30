#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

def create_graph(ipt, g):
    lines = open(ipt, 'r').readlines()
    lines = map(lambda x:x.split(), lines)
    lines = filter(lambda x:len(x)>=2, lines)
    for line in lines:
        g.add(int(line[0]))
        g.add(int(line[1]))
    g.indexing()
    for line in lines:
        g.add_edge(int(line[0]), int(line[1]))

def load_cluster_info(g, ipt):
    from index import Index
    idx_clst = Index()
    lines = open(ipt, 'r').readlines()
    lines = map(lambda x:x.split(), lines)
    set_vtx = set()
    for i in range(g.n()):
        set_vtx.add(g.nodes()[i].name)
    lines = filter(lambda x: int(x[0]) in set_vtx, lines)
    for line in lines:
        clst = int(line[1])
        idx_clst.add(clst)
    idx_clst.index()
    for line in lines:
        nodeidx = g.index.get_idx_by_key(int(line[0]))
        clst = idx_clst.get_idx_by_key(int(line[1]))
        g.nodes()[nodeidx].expected = clst
    return idx_clst

def compute_nmi(g):
    from nmi import nmi_list
    list_expected = []
    list_actual = []
    for i in range(g.n()):
        list_expected.append(g.nodes()[i].expected)
        list_actual.append(g.nodes()[i].actual)
    return nmi_list(list_expected, list_actual)

def dump_matrix(X, opt):
    r, c = X.shape
    writer = open(opt, 'w')
    for i in range(r):
        list_write = []
        for j in range(c):
            list_write.append(str(X.item(i, j)))
        writer.write(' '.join(list_write) + '\n')

def load_matrix(ipt):
    mat = []
    lines = open(ipt, 'r')
    lines = map(lambda x:x.strip().split(), lines)
    for line in lines:
        mat.append(map(lambda x:float(x), line))
    return np.asmatrix(mat)
    
if __name__ == '__main__':
    from glb import basepath
    import os, json
    ipt = os.path.join(basepath, 'data/test/2006-9~2006-9_edges.gc')    
    #ipt = os.path.join(basepath, 'data/test/test.graph')    
    opt = os.path.join(basepath, 'data/test/graph.json')
    g = Graph()
    create_graph(ipt, g)
    print g.adjmatrix()
    g.dump(opt)
