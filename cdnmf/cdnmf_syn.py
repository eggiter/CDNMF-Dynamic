#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, copy as cp
from graph import Graph
from glb import basepath, logging
import giantcomponent as gc, smooth as sm, core, coreExt as ce
log = logging.getLogger(__name__)

def load_mat(ipt):
    import scipy.io as sio
    mat = sio.loadmat(ipt)
    list_clsts = []
    r, c = mat['GT_Matrix'].shape
    for j in range(c):
        list_clst = []
        for i in range(r):
            list_clst.append(mat['GT_Matrix'][i][j])
        list_clsts.append(list_clst)
    return mat['W_Cube'][0], list_clsts

def run(filename, lmd):
    num_iter = 1
    '''
    if filename != 'syn_T_10_z_4_nC_1_bS_128_aD_16.mat':
        return None
    '''
    ipt = os.path.join(basepath, 'data/syn/' + filename)
    optdir = os.path.join(basepath, 'data/result/syn/{}'.format(filename[:-4]))
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    list_nmi = []
    first = True
    As, list_clsts = load_mat(ipt)
    for idx in range(10):
        log.info('%d ...' % idx)
        A = As[idx]
        list_clst = list_clsts[idx]
        g = Graph()
        idx_clst = sm.load_graph(g, A, list_clst)
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
        
        ce.getcluster_bycore(g, k, U, H)
        ce.getcluster_rest(g, k)
        #ce.get_hubs(g, k, U, path_hubs)
        
        #getcluster_byx(g, X)
        nmi = sm.compute_nmi(g)
        list_nmi.append(nmi)
        print '===NMI===\n', len(list_nmi), nmi
    print '===RESULT==='
    for e in enumerate(list_nmi):
        print '{}: {}'.format(e[0] + 1, e[1])
    return list_nmi

def dump_nmi(list_nmi, filename, lmd):
    optdir = 'data/result/syn/{}/nmi/'.format(filename[:-4])
    if not os.path.isdir(optdir):
        os.makedirs(optdir)
    writer = open(os.path.join(basepath, optdir + 'lmd{}.txt'.format(lmd)), 'w')
    writer.writelines(map(lambda x: str(x) + '\n', list_nmi))
    
def getcluster_byx(g, X):
    r, c = X.shape
    for i in range(r):
        right = -1
        for j in range(c):
            if X.item(i, j) > right:
                right = X.item(i, j)
                g.nodes()[i].actual = j

if __name__ == '__main__':
    lmds = [x*0.2 for x in range(11)]
    n = 10
    iptdir = 'data/syn'
    for f in filter(lambda x: '.mat' in x, os.listdir(iptdir)):
        for lmd in lmds:
            list_nmi = []
            for _ in range(n):
                ret = run(f, lmd)
                if not ret:
                    break
                list_nmi.append(ret)
            if not ret:
                break
            list_avg = []
            for c in range(len(list_nmi[0])):
                s = 0.0
                for r in range(n):
                    s += list_nmi[r][c]
                list_avg.append(s/n)
            dump_nmi(list_avg, f, lmd)