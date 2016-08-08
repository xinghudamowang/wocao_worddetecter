#coding:utf-8
from operator import itemgetter
from prioritydictionary import priorityDictionary
class Graph(object):
    """docstring for Graph"""
    INFINITY = 100000
    UNDEFINED = None
    def __init__(self, n,default_prob):
        super(Graph, self).__init__()
        self._data = {}
        self.N = n
        for i in xrange(0,n-1):
            self._data[i] = {}
            self._data[i][i+1] = default_prob
        self._data[n-1] = {}

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return str(self._data)

    def __getitem__(self,node):
        try:
            data = self._data[node]
        except KeyError:
            data = None

        return data

    def iteritems(self):
        return self._data._iteritems()

    def add_edge(self, node_from,node_to,cost = None):
        if not cost:
            cost = self.INFINITY
        self._data[node_from][node_to] = cost

    def remove_edge(self, node_from, node_to,cost = None):
        try:
            r_value = self._data[node_from][node_to]
        except KeyError:
            r_value = -1
        if not cost and r_value !=-1:
            cost = r_value
            if cost == self.INFINITY:
                r_value = -1
            else:
                self._data[node_from][node_to] = self.INFINITY
                return cost
        elif r_value == cost:# elif r_value == cost and r_value != -1
            self._data[node_from][node_to] = self.INFINITY
            r_value = cost
        else:
            r_value = -1
        return r_value


def quick_shortest(graph):
    N = graph.N-1
    distances = {} 
    previous = {}
    
    previous[0] = None
    distances[N] = 0.0

    for idx in xrange(N-1,-1,-1):
        Q = priorityDictionary()
        for x in graph[idx]:
            Q[x] = graph[idx][x] + distances[x]
        
        small = Q.smallest()
        previous[idx] = small
        distances[idx] = Q[small]
    # get path from previous 21/08/13 09:10:14
    paths = []
    paths.append(0)
    start = 0
    while start < N:
        paths.append(previous[start])
        start = previous[start]
    return (distances, paths)
    


    