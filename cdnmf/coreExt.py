#! /usr/bin/env python
# -*- coding: utf-8 -*-
import copy as cp
from glb import logging
log = logging.getLogger(__name__)

def getcluster_bycore(g, k, U, H):
    for i in range(k):
        list_tuple = []
        for j in range(g.n()):
            list_tuple.append((j, U.item(j, i)))
        list_tuple = sorted(list_tuple, key=lambda x: x[1], reverse = True)
        tot_degree = 0
        for j in range(g.n()):
            degree = g.nodes()[list_tuple[j][0]].get_degree()
            if abs(tot_degree + degree - H.item(i ,i)) <= abs (tot_degree - H.item(i, i)):
                g.nodes()[list_tuple[j][0]].clusters.add(i)
                g.nodes()[list_tuple[j][0]].extra['status'] = 0
                tot_degree += degree
    
    list_outlier = []
    list_overlap = []
    for i in range(g.n()):
        if not g.nodes()[i].clusters:
            list_outlier.append(i)
        elif len(g.nodes()[i].clusters)>1:
            list_overlap.append('{}: {}'.format(i, ', '.join(map(lambda x:str(x), sorted(g.nodes()[i].clusters)))))
    #log.info('\noutliers: {}\n{}\noverlap: {}\n{}'.format(len(list_outlier), list_outlier, len(list_overlap), '\n'.join(list_overlap)))

def getcluster_rest(g, k):
    list_multiple = g.tryoutliers(k)
    for i in list_multiple:
        clst = allocate_cluster(cp.deepcopy(g), i)
        g.nodes()[i].actual = clst

def allocate_cluster(g, nodeidx):
    for i in range(g.n()):
        if i == nodeidx:
            continue
        elif g.nodes()[i].actual == -1:
            g.nodes()[i].actual = list(g.nodes()[i].clusters)[0]
    list_tuple = []
    log.debug('allocate cluster for node %d' % nodeidx)
    for i in g.nodes()[nodeidx].clusters:
        g.nodes()[nodeidx].actual = i
        q = g.modularity()
        list_tuple.append((i, q))
        log.debug('\tcluster: {};\tQ: {}'.format(i, q))
    list_tuple = sorted(list_tuple, key = lambda x: x[1], reverse = True)
    clst = list_tuple[0][0]
    log.debug('finally, cluster %d' % clst)
    return clst

def get_hubs(g, k, U, opt):
    import csv
    writer = csv.writer(open(opt, 'w'))
    for i in range(k):
        sums = 0.0
        list_tuple = []
        for j in range(g.n()):
            list_tuple.append((j, U.item(j, i)))
            sums += U.item(j, i)
        list_tuple = sorted(list_tuple, key=lambda x:x[1], reverse=True)
        writer.writerow(['community %d' % i])
        writer.writerow(['order', 'index', 'name', 'u_value', 'percetage(%)'])
        for j in range(g.n()):
            list_write = []
            list_write.append(j+1)
            list_write.append(list_tuple[j][0])
            list_write.append(g.nodes()[list_tuple[j][0]].name)
            list_write.append(list_tuple[j][1])
            list_write.append(list_tuple[j][1] / sums * 100)
            writer.writerow(map(lambda x:str(x), list_write))

