#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, copy as cp, scipy.io as sio
from graph import Graph
import giantcomponent as gc, smooth as sm, core, coreExt as ce
from glb import logging, basepath
log = logging.getLogger(__name__)

def run(lmd, which, times):
    num_iter = 1
    iptdir = os.path.join(basepath, 'data/MinSoo_datasets/synvar/z_{}'.format(which))
    optdir = os.path.join(basepath, bd + '/z_{}'.format(which))
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    list_nmi = []
    list_err = []
    first = True
    list_errmat_expected = []
    list_errmat_actual = []
    for i in range(1, 11):
        fmt = 'synvar_%d.t%02d' % (which, i)
        log.info(fmt + '...')
        ipt_edges = os.path.join(iptdir, fmt + '.edges')
        path_gc = os.path.join(optdir, fmt+'.gc')
        ipt_comm1 = os.path.join(iptdir, fmt+'.comm1')
        path_hubs = os.path.join(optdir, fmt+'.hubs.csv')
        #gc.gen_gc(ipt_edges, path_gc)
        g = Graph()
        #sm.create_graph(path_gc, g)
        sm.create_graph(ipt_edges, g)
        idx_clst = sm.load_cluster_info(g, ipt_comm1)
        k = idx_clst.num_indices()
        if first:
            lpre = 2.0 ** 32
            for i in range(num_iter):
                UU, HH, LL, XX = core.cdnmf(g.adjmatrix(), k)
                if LL[-1] < lpre:
                    lpre = LL[-1]
                    U, H, X = UU, HH, XX               
                    log.info('%02d --  %.4f %.4f CHANGED!' % (i+1, LL[-1], lpre))
                else:
                    log.info('%02d --  %.4f %.4f' % (i+1, LL[-1], lpre))
            first = False
        else:
            X = core.adjust_xpre(gpre, g, X)
            lpre = 2.0 ** 32
            for i in range(num_iter):
                UU, HH, LL, XX = core.cdnmf_dynamic(g.adjmatrix(), k, X, lmd)
                if LL[-1] < lpre:
                    lpre = LL[-1]
                    U, H, X = UU, HH, XX
                    log.info('%02d --  %.4f %.4f CHANGED!' % (i+1, LL[-1], lpre))
                else:
                    log.info('%02d --  %.4f %.4f' % (i+1, LL[-1], lpre)) 
        gpre = cp.deepcopy(g)
        '''
        ce.getcluster_bycore(g, k, U, H)
        ce.getcluster_rest(g, k)
        #ce.get_hubs(g, k, U, path_hubs)
        '''
        getcluster_byx(g, X)
        nmi = sm.compute_nmi(g)
        list_nmi.append(nmi)
        e, a = sm.get_errmat(g, k)
        list_errmat_expected.append(e)
        list_errmat_actual.append(a)
        list_err.append(sm.compute_error(g, k))
        print '===NMI===\n', len(list_nmi), nmi
    d = {}
    d['errmat_expected'] = sm.cell(list_errmat_expected)
    d['errmat_actual'] =  sm.cell(list_errmat_actual)
    sio.savemat(os.path.join(optdir, 'lmd{}_times{}.mat'.format(lmd, times)), d)
    print '===RESULT==='
    for e in enumerate(list_nmi):
        print '{}: {}'.format(e[0] + 1, e[1])
    return list_nmi, list_err

def dump_nmi(list_nmi, which, lmd):
    optdir = bd + '/z_{}/nmi/'.format(which)
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    writer = open(os.path.join(basepath, optdir + 'lmd{}.txt'.format(lmd)), 'w')
    writer.writelines(map(lambda x: str(x) + '\n', list_nmi))
    
def dump_err(list_err, which, lmd):
    optdir = bd + '/z_{}/err/'.format(which)
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    writer = open(os.path.join(basepath, optdir + 'lmd{}.txt'.format(lmd)), 'w')
    writer.writelines(map(lambda x: str(x) + '\n', list_err))

def get_avg(lst, n):
    list_avg = []
    for c in range(len(lst[0])):
        s = 0.0
        for r in range(n):
            s += lst[r][c]
        list_avg.append(s/n)
    return list_avg
    
def getcluster_byx(g, X):
    r, c = X.shape
    for i in range(r):
        right = -1
        for j in range(c):
            if X.item(i, j) > right:
                right = X.item(i, j)
                g.nodes()[i].actual = j

global bd
bd = 'data/result/MinSoo_datasets/synvar'

if __name__ == '__main__':
    lmds = [0.0, 1.0, 2.0]
    lmds = [x*0.2 for x in range(11)]
    ii = [5, 3]
    n = 1
    for i in ii:
        for lmd in lmds:
            list_nmi = []
            list_err = []
            for _ in range(n):
                nmis, errs = run(lmd, i, _)
                list_nmi.append(nmis)
                list_err.append(errs)
            list_avg = get_avg(list_nmi, n)
            dump_nmi(list_avg, i, lmd)
            list_avg = get_avg(list_err, n)
            dump_err(list_avg, i, lmd)
