#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, copy as cp
from graph import Graph
import giantcomponent as gc, smooth as sm, core, coreExt as ce
from glb import logging
log = logging.getLogger(__name__)
def run(lmd):
    from glb import basepath
    iptdir = os.path.join(basepath, 'data/blog')
    optdir = os.path.join(basepath, 'data/result/blog')
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    list_nmi = []
    for i in range(1, 15):
        fmt = 'blog_timeSlice_%02d' % i
        log.info(fmt + '...')
        ipt_edges = os.path.join(iptdir, fmt + '.edges')
        path_gc = os.path.join(optdir, fmt+'.gc')
        ipt_comm1 = os.path.join(iptdir, fmt+'.comm1')
        path_hubs = os.path.join(optdir, fmt+'.hubs.csv')
        #gc.gen_gc(ipt_edges, path_gc)
        g = Graph()
        sm.create_graph(path_gc, g)
        idx_clst = sm.load_cluster_info(g, ipt_comm1)
        g.dump(os.path.join(optdir,'graph.json'))
        k = idx_clst.num_indices()
        if i==1:
            U, H, L, X = core.cdnmf(g.adjmatrix(), k)
        else:
            X = core.adjust_xpre(gpre, g, X)
            U, H, L, X = core.cdnmf_dynamic(g.adjmatrix(), k, X, lmd)
        gpre = cp.deepcopy(g)
        ce.getcluster_bycore(g, k, U, H)
        ce.getcluster_rest(g, k)
        ce.get_hubs(g, k, U, path_hubs)
        nmi = sm.compute_nmi(g)
        list_nmi.append(nmi)
        print '===NMI===\n',nmi
    print '===RESULT==='
    for e in enumerate(list_nmi):
        print '{}: {}'.format(e[0] + 1, e[1])

if __name__ == '__main__':
    lmd = 1
    run(lmd)

