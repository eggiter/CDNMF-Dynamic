#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, copy as cp
from graph import Graph
from glb import basepath
import giantcomponent as gc, smooth as sm, core, coreExt as ce

def gettime(start, end, interval):
    sy, sm = start
    ey, em = end
    if sy > ey or (sy == ey and sm > em):
        return None, None
    tm = sm + interval - 1
    ty = sy
    if tm > 12:
        ty = sy + tm / 12
        tm = tm % 12
    fmt = '{}-{}~{}-{}'.format(sy, sm, ty, tm)

    tm = sm + interval
    ty = sy
    if tm > 12:
        ty = sy + tm / 12
        tm = tm % 12
    return (ty, tm), fmt

def run(lmd, i):
    dir_fmt = 'Interval_{}_mon'.format(i)
    iptdir = os.path.join(basepath, 'data/email/' + dir_fmt)
    optdir = os.path.join(basepath, 'data/result/email/' + dir_fmt)
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    list_nmi = []
    start = (2006, 9)
    end = (2010, 8)
    temp, fmt = gettime(start, end, i)
    first = True
    while temp:
        ipt_edges = os.path.join(iptdir, fmt + '.edges')
        path_gc = os.path.join(optdir, fmt+'.gc')
        ipt_comm1 = os.path.join(iptdir, fmt+'.comm1')
        path_hubs = os.path.join(optdir, fmt+'.hubs.csv')
        #gc.gen_gc(ipt_edges, path_gc)
        g = Graph()
        sm.create_graph(path_gc, g)
        idx_clst = sm.load_cluster_info(g, ipt_comm1)
        k = idx_clst.num_indices()
        if first:
            U, H, L, X = core.cdnmf(g.adjmatrix(), k)
            first = False
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
        temp, fmt = gettime(temp, end, i)
    print '===RESULT==='
    for e in enumerate(list_nmi):
        print '{}: {}'.format(e[0] + 1, e[1])
    writer = open(os.path.join(basepath, 'data/result/email/nmi/I{}lmd{}.txt'.format(i, lmd)), 'w')
    writer.writelines(map(lambda x: str(x) + '\n', list_nmi))

if __name__ == '__main__':
    lmds = [0, 0.5, 1, 5, 10]
    i = 2
    for lmd in lmds:
        run(lmd, i)

