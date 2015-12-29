#! /usr/bin/env python
# -*- coding: utf-8 -*-
import smooth as sm
from graph import Graph
import giantcomponent as gc, core, coreExt as ce

def test_first_phase():
    from glb import basepath
    import os
    k = 4
    ipt = os.path.join(basepath, 'data/z_5/synfix_5.t01.edges')
    ipt_gc = os.path.join(basepath, 'data/z_5_r/synfix_5.t01.gc')
    ipt_comm = os.path.join(basepath, 'data/z_5/synfix_5.t01.comm1')
    opt = os.path.join(basepath, 'data/z_5_r/s5t01.graph.json')
    opt_hubs = os.path.join(basepath, 'data/z_5_r/s5t01.hubs.csv')
    gc.gen_gc(ipt, ipt_gc)
    g = Graph()
    sm.create_graph(ipt_gc, g)
    sm.load_cluster_info(g, ipt_comm)
    U, H, L, X = core.cdnmf(g.adjmatrix(), k)
    ce.getcluster_bycore(g, k, U, H)
    ce.getcluster_rest(g, k)
    ce.get_hubs(g, k, U, opt_hubs)
    nmi = sm.compute_nmi(g)
    print '===NMI===\n', nmi
    g.dump(opt)
    a = g.adjmatrix()
    opt = 'data/z_5_r/test.adj'
    writer = open(opt, 'w')
    for i in range(128*128):
        writer.write(str(a.item(i)))
        if (i+1) % 128 ==0:
            writer.write('\n')
        else:
            writer.write(',')

if __name__ == '__main__':
    test_first_phase()
