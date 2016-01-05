#! /usr/bin/env python
# -*- coding: utf-8 -*-
from graph import Graph
import scipy.io as sio
import smooth as sm
import os
import pylab as pl

def create_graph(g, list_expected, list_actual):
    n = len(list_expected)
    for i in range(n):
        g.add(i)
    g.indexing()
    for i in range(n):
        exp = list_expected[i]
        act = list_actual[i]
        g.nodes()[i].expected = exp
        g.nodes()[i].actual = act

def load_mat(ipt):
    mat = sio.loadmat(ipt)
    lists_exp = []
    lists_act = []
    r, c = mat['GT_Matrix'].shape
    for j in range(c):
        list_clst = []
        for i in range(r):
            list_clst.append(mat['GT_Matrix'][i][j])
        lists_exp.append(list_clst)
        list_clst = []
        for i in range(r):
            list_clst.append(mat['Z4'][i][j])
        lists_act.append(list_clst)
    return lists_exp, lists_act

def get_nmi(ipt):
    lists_exp, lists_act = load_mat(ipt)
    list_nmi = []
    for i in range(len(lists_exp)):
        g = Graph()
        create_graph(g, lists_exp[i], lists_act[i])
        nmi = sm.compute_nmi(g)
        list_nmi.append(nmi)
    return list_nmi

def loadlist(ipt):
    lines = open(ipt, 'r')
    lines = map(lambda x: float(x.strip()), lines)
    return lines
    
def plot(list_data, list_label, cnt):
    pl.figure(cnt)
    list_print = range(len(list_data))
    x = range(1, len(list_data[0])+1)
    filename = 'data/nmi/syn/nmi_' + list_label[-1]
    for p in list_print:
        pl.plot(x, list_data[p], label = list_label[p])
    
    pl.xlabel('Time Slice')
    pl.ylabel('NMI')
    pl.legend(loc='lower right')
    pl.ylim(0,1)
    pl.savefig(filename+'.png', format='png')

def run():
    iptdir = 'data/cmp/syn'
    cnt = 0
    for f in filter(lambda x:'.mat' in x, os.listdir(iptdir)):
        ipt = os.path.join(iptdir, f)
        list_nmi = get_nmi(ipt)
        list_data = []
        list_data.append(list_nmi)
        list_file = [
            'lmd0.0.txt',\
            'lmd1.0.txt'
        ]
        list_label = ['facetnet','lmd=0.0','lmd=1.0', 'syn_'+f[12:-14]]
        for i in range(len(list_file)):
            list_file[i] = 'data/result/syn/syn_{}/nmi/{}'.format(f[7:-14], list_file[i])
        for f in list_file:
            list_data.append(loadlist(f))
        cnt += 1
        plot(list_data, list_label, cnt)
    
if __name__ == '__main__':
    run()
    
