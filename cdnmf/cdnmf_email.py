#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, copy as cp, scipy.io as sio, numpy as np
from graph import Graph
from glb import basepath, logging
import giantcomponent as gc, smooth as sm, core, coreExt as ce
log = logging.getLogger(__name__)

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

def run(lmd, interval, times):
    num_iter = 1
    dir_fmt = 'Interval_{}_mon'.format(interval)
    iptdir = os.path.join(basepath, 'data/emailtemp_perm/' + dir_fmt)
    optdir = os.path.join(basepath, bd + '/' + dir_fmt)
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    list_nmi = []
    list_err = []
    start = (2006, 9)
    end = (2010, 8)
    temp, fmt = gettime(start, end, interval)
    first = True
    list_errmat_expected = []
    list_errmat_actual = []
    while temp:
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
        log.info('num clusters: %d' % k)
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
        ce.get_hubs(g, k, U, path_hubs)
        '''
        getcluster_byx(g, X)
        nmi = sm.compute_nmi(g)
        list_nmi.append(nmi)
        e, a = sm.get_errmat(g, k)
        list_errmat_expected.append(e)
        list_errmat_actual.append(a)
        list_err.append(sm.compute_error(g, k))
        print '===NMI===\n', len(list_nmi), nmi
        temp, fmt = gettime(temp, end, interval)
    d = {}
    d['errmat_expected'] = sm.cell(list_errmat_expected)
    d['errmat_actual'] =  sm.cell(list_errmat_actual)
    sio.savemat(os.path.join(optdir, 'lmd{}_times{}.mat'.format(lmd, times)), d)
    print '===RESULT==='
    for e in enumerate(list_nmi):
        print '{}: {}'.format(e[0] + 1, e[1])
    return list_nmi, list_err

def dump_nmi(list_nmi, interval, lmd):
    optdir = bd + '/Interval_{}_mon/nmi/'.format(interval)
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    writer = open(os.path.join(basepath, optdir + 'lmd{}.txt'.format(lmd)), 'w')
    writer.writelines(map(lambda x: str(x) + '\n', list_nmi))
    
def dump_err(list_err, interval, lmd):
    optdir = bd + '/Interval_{}_mon/err/'.format(interval)
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
bd = 'data/result/emailtemp4'

if __name__ == '__main__':
    lmds = [x*0.2 for x in range(11)]
    ii = [2]
    n = 3
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