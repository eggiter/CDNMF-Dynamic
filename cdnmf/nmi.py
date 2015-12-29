#! /usr/bin/env python
# -*- coding: utf-8 -*-
#refence: Constant Communities in Complex Networks
import numpy as np
import math, json, logging, logging.config
from index import Index
import test
log = logging.getLogger(__name__)

def nmi_cm(cm):
    '''
    given confusion matrix, calculate nmi
    '''
    (ca, cb) = cm.shape
    N = cm.sum()
    up = 0.0
    Ni = np.squeeze(np.asarray(cm.sum(axis = 1)))
    Nj = np.squeeze(np.asarray(cm.sum(axis = 0)))
    for i in range(ca):
        for j in range(cb):
            if cm.item(i, j) > 0:
                up += cm.item(i, j)*math.log(cm.item(i, j)*N*1.0/(Ni[i]*Nj[j]))
    
    down = 0.0
    for i in range(ca):
        down += Ni[i]*math.log(Ni[i]*1.0/N)
    for j in range(cb):
        down += Nj[j]*math.log(Nj[j]*1.0/N)

    return up * -2.0 / down

def nmi_list(list_expected, list_actual):
    '''
    given two lists, tranfer to confusion matrix, then calculate nmi
    '''
    if len(list_expected) != len(list_actual):
        raise ValueError('two size not the same: {} != {}.'.format(len(list_expected), len(list_actual)))
    idx_expected = Index()
    idx_actual = Index()
    map(idx_expected.add, list_expected)
    map(idx_actual.add, list_actual)
    idx_expected.index()
    idx_actual.index()
    cm = [[0]*idx_actual.num_indices() for _ in range(idx_expected.num_indices())]
    for i in range(len(list_expected)):
        gt = idx_expected.get_idx_by_key(list_expected[i])
        pred = idx_actual.get_idx_by_key(list_actual[i])
        cm[gt][pred] += 1
    cm = np.asmatrix(cm)
    return nmi_cm(cm)

if __name__ == '__main__':
    list_expected = [0, 1, 1, 1]
    list_actual = [0, 0, 1, 1]
    #list_actual = [2, 3, 3, 3]
    print nmi_list(list_expected, list_actual)

