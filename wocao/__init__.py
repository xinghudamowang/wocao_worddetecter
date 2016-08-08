#coding:utf-8
from ksp_dijkstra import Graph,quick_shortest

class WordBase(object):
    """docstring for WordBase"""
    def __init__(self):
        super(WordBase, self).__init__()
        self.base_freq = 0
        self.base_ps = 0.0
        self.type = ''
       
def get_sentence_dict():
    cutlist = u" .[。，,！……!《》<>\"':：？\?、\|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:@“”＂'‘\n\r"
    # print type(cutlist)
    if not isinstance(cutlist, unicode):
        try:
            cutlist = cutlist.decode('utf-8')
        except UnicodeDecodeError:
            cutlist = cutlist.decode('gbk','ignore')
    cutlist_dict = {}
    for c in list(cutlist):
        word = WordBase()
        cutlist_dict[c] = word
    return cutlist_dict


class BaseCutter(object):
    """docstring for BaseCutter"""
    def __init__(self):
        super(BaseCutter, self).__init__()
        self.WORD_MAX = 6
        self.refer_prob = 15.0
        self.default_prob = 150.0
        self.stages = []
        self.stages.append([])
        self.stages.append([])
        self.stages.append([])
        self.stages.append([])
        self.fn_stage1 = self.__stage1_null
        self.sentence_dict = get_sentence_dict()
        self.__best_path = self.__cut_graph_simple
    def cut_to_sentence(self,line):
        if not isinstance(line,unicode):
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                line = line.decode('gbk','ignore')
        for s,need_cut in self.fn_stage1(line):
            if need_cut:
                if s!='':
                    string =''
                    for c in s:
                        try:
                            temp = self.sentence_dict[c]
                        except KeyError:
                            temp = None
                        if temp is not None:# try &except &if change has_key to O(1)
                            if string != '':
                                yield (string,True)
                            string = ''
                            yield (c,False)
                        else:
                            string += c
                    if string != '':
                        yield(string,True)
            else:
                yield(s,False)

    

    def __stage1_null(self,sentence):
        yield (sentence,True)

    def set_stage1_regex(self, rex):
        if type(rex) == str:
            self.stage1_regex = re.compile(rex, re.I|re.U)
        else:
            self.stage1_regex = rex
        self.fn_stage1 = self.__do_stage1

    def get_graph(self,sentence):
        n = len(sentence)
        i,j = 0,0
        graph = Graph(n+1 , self.default_prob)
        for stage in self.stages[1]:
            stage.cut_stage2(self,sentence,graph)
        while i< n:
            for j in xrange(i,min(n,i+self.WORD_MAX),1):
                if self.exist(sentence[i:j+1]):
                    graph.add_edge(i,j+1,0-self.get_prob(sentence[i:j+1]))
                else:
                    for stage in self.stages[2]:
                        stage.cut_stage3(self,sentence,graph,i,j+1)
            i += 1
            j = i

        return graph

    def __cut_graph(self,sentence):
        graph = self.get_graph(sentence)
        path = self.__best_path(sentence,graph)
        for i in xrange(1,len(path)):
            yield sentence[path[i-1]:path[i]]

    def __new_path(self,sentence,graph,contex = {}):
        path = contex['path']

        index = 1
        n_path = len(path)
        while index < path:
            i = index
            for stage in self.stages[3]:
                i = stage.cut_stage4(self,sentence,graph,contex)
                if i >= n_path:
                    break
                contex['index'] = i
            if i >= n_path:
                break

            if path[i] - path[i-1] == 1:
                contex['single'] += 1
            contex[ 'new_path'].append(path[i])
            index = i+1
            contex['index'] = index

    def __cut_graph_simple(self,sentence,graph):
        (_,path) = quick_shortest(graph)
        contex = {'path':path,'new_path':[0],'single':0,'index':1}
        self.__new_path(sentence,graph,contex = contex)
        return contex['new_path']


    def get_prob(self,item):
        pass
    def exist(self,item):
        pass
    def cut(self,sentence):
        for s,need_cut in self.cut_to_sentence(sentence):
            if s == '':
                continue
            elif need_cut:
                for word in self.__cut_graph(s):
                    # print 'cutting'
                    yield word
            else:
                yield s





