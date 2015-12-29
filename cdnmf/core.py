#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np, time
from glb import logging
log = logging.getLogger(__name__)

def cdnmf(A, k):
    start = time.time()
    (num_nodes, num_nodes) = A.shape
    U = np.zeros((num_nodes, k)) # n by k
    H = np.zeros((k, k))
    X = np.asmatrix(np.random.rand(num_nodes, k))
    l = [2.0**32]
    cnt_iter = 300
    eps = 1e-6
    for i in range(cnt_iter):
        up = A * X
        down = 2 * X * X.T * X
        X = np.multiply(X, (0.5 + up / down))
        l.append(np.trace((A - X * X.T).T * (A - X * X.T)))
        if abs(l[i+1] - l[i]) <= eps:
            break
    log.info('num iters: %d' % (len(l) - 1))
    col_sum_x = np.squeeze(np.asarray(sum(X)))
    U = X * np.diag(1. / col_sum_x)
    H = np.diag(col_sum_x ** 2)
    
    log.info('cdnmf: {}'.format(time.time() - start))
    return U, H, l[1:], X

def cdnmf_dynamic(A, k, Xpre, lmd):
    start = time.time()
    num_nodes, num_nodes = A.shape
    U = np.zeros((num_nodes, k)) # n by k
    H = np.zeros((k, k))
    X = np.asmatrix(np.random.rand(num_nodes, k))
    l = [2.0**32]
    cnt_iter = 300
    eps = 1e-6
    for i in range(cnt_iter):
        up = (A + lmd * Xpre * Xpre.T) * X
        down = 2 * (1 + lmd) * X * X.T * X
        X = np.multiply(X, (0.5 + up / down))
        l.append(np.trace((A-X*X.T).T * (A-X*X.T)) + lmd*np.trace((X*X.T - Xpre*Xpre.T).T * (X*X.T-Xpre*Xpre.T)))
        if abs(l[i+1] - l[i]) <= eps:
            break
    log.info('num iters: %d' % (len(l) - 1))
    col_sum_x = np.squeeze(np.asarray(sum(X)))
    U = X * np.diag(1. / col_sum_x)
    H = np.diag(col_sum_x ** 2)
    
    log.info('cdnmf-dynamic: {}'.format(time.time() - start))
    return U, H, l[1:], X

def adjust_xpre(gpre, gnow, Xpre):
    row, col = Xpre.shape
    X = [[0.01]*col for _ in range(gnow.n())]
    nodename_pre = [x.name for x in gpre.nodes()]
    for i in range(gnow.n()):
        if gnow.nodes()[i].name in nodename_pre:
            idx = gpre.index.get_idx_by_key(gnow.nodes()[i].name)
            for j in range(col):
                X[i][j] = Xpre.item(idx, j)
    return np.asmatrix(X)
    
