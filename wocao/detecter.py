#coding:utf-8
import collections,math,threading
import codecs
from wocao import *

max_word_len = 5
entropy_threshold = 1.0
max_to_flush = 10000
Bayes_threshold = 100

def info_entropy(words, total):
    result = 0 
    for word, cnt in words.iteritems():
        p = float(cnt) / total
        result -= p * math.log(p)
    return result

MODIFY_LOCK = threading.RLock()
MODIFY_INIT = False


def get_modified_dict():
    global MODIFY_INIT
    dict = get_dict(DICTS.MAIN)
    if MODIFY_INIT:
        return dict
    with MODIFY_LOCK:
        if MODIFY_INIT:
            return dict
        for word in dict:
            modify_wordbase(word)
        MODIFY_INIT = True
    return dict
class Process(object):
    """docstring for Process"""
    def __init__(self, id_):
        super(Process, self).__init__()
        self.id_ = id_
        self.words = []
        self.cacge_lines = []
    def add_words(self,word):
        self.words.append(word)

    def do_sentence(self,sentence,word_dict):
        l = len(sentence)
        word_l = min(l, max_word_len)
        for i in xrange(1,word_l +1):
            for j in xrange(0,l - i + 1):
                if j == 0:
                    if j <l-i:
                        word_dict.add_right(sentence[j:j+i],sentence[j+i])#
                    else:
                        word_dict.add_word(sentence[j:j+i])#i >= l in fact because of min(l,max_word_len) i == l
                else:
                    if j<l-i:
                        word_dict.add_rig_left(sentence[j:j+i],sentence[j-1],sentence[j+i])
                    else:
                        word_dict.add_left(sentence[j:j+i],sentence[j-1])


    def calc(self,word_dict):
        for word in self.words:
            this_word = word_dict.get_word(word)
            this_word.process_ps = float(this_word.process_freq) / word_dict.process_total
        for word in self.words:
            this_word = word_dict.get_word(word)
            if len(word) > 1:
                p = 0
                for i in xrange(1,len(word)):
                    t = word_dict.ps(word[:i]) * word_dict.ps(word[i:])
                    p = max(p,t)
                if p > 0 and this_word.process_freq >= 3 and this_word.process_ps / p >= Bayes_threshold:
                    if this_word.l_len > 0 and info_entropy(this_word.l,this_word.l_len) < entropy_threshold:
                        continue
                    if this_word.r_len > 0 and info_entropy(this_word.r,this_word.r_len) < entropy_threshold:
                        continue
                    this_word.valid += 1
                    this_word.curr_ps = math.log(float(this_word.total_freq + this_word.base_freq) / float(word_dict.base_total + word_dict.total / word_dict.id_))

class WordDict(BaseCutter):
    """docstring for WordDict"""
    def __init__(self, new_dict = True):
        super(WordDict, self).__init__()
        self.dict = {}
        self.total = 0
        self.base_total = 0
        self.id_ = 0
        self.proces_total = 0
        self.current_line = 0
        self.WORD_MAX = 5

        if not new_dict:
            self.dict = get_modified_dict()
        self.new_process() 
    def exist(self,word):
        if word not in self.dict:
            return False
        this_word = self.dict[word]
        return (this_word.curr_ps < 0.0) or (this_word.valid > self.id_/2)

    def get_prob(self,word):
        if word in self.dict:
            return self.dict[word].curr_ps
        else:
            return 0.0

    def new_process(self):
        self.id_ += 1
        self.process = Process(self.id_)
        self.process_total = 0
        return self.process

    def add_word(self,word):
        this_word = None
        if word in self.dict:
            this_word = self.dict[word]
            if self.id_ == this_word.id_:
                this_word.add()
            else:
                this_word.reset(self.id_)
                self.process.add_words(word)
        else:
            this_word = Word(self.id_)
            self.dict[word] = this_word
            self.process.add_words(word)
        self.process_total += 1
        self.total += 1
        return this_word

    # def learn_not_cut(self,sentence):
        # self.process.do_sentence(sentence,self)
        # self.current_line += 1
        # if self.current_line > max_to_flush:
            
        #     self.process.calc(self)
        #     self.new_process()
        #     self.current_line = 0

    def learn_chinese(self,sentence):
        for s,need_cut in self.cut_to_sentence(sentence):
            if not need_cut:
                continue
            # print s
            self.process.do_sentence(s,self)
            self.current_line += 1
            if self.current_line > max_to_flush:
                print '<<<<<<<flushing>>>>>>>>'
                self.process.calc(self)
                self.new_process()
                self.current_line = 0
    def learn_pinyin(self,sentence):
        self.process.do_sentence(sentence,self)
        self.current_line+=1
        if self.current_line > max_to_flush:

            self.process.calc(self)
            self.new_process()
            self.current_line = 0


    def learn_flush(self):
        self.process.calc(self)
        self.new_process()
        self.current_line = 0

    def cut_and_learn_chinese(self,sentence):
        self.learn_chinese(sentence)
        return self.cut(sentence)

    def cut_and_learn_pinyin(self,sentence):
        self.learn_pinyin(sentence)
        print 'cutting'
        return self.cut(sentence)

    def add_right(self,word,l):
        w = self.add_word(word)
        w.add_l(l)
    def add_left(self,word,r):
        w = self.add_word(word)
        w.add_r(r)
    def add_rig_left(self,word,l,r):
        w = self.add_word(word)
        w.add_l(l)
        w.add_r(r)

    def ps(self,word):
        if word in self.dict and self.dict[word].id_ == self.id_:
            return self.dict[word].process_ps
        else:
            return 0.0

    def get_word(self,word):
        return self.dict[word]

    def save_to_file(self, filename, sorted=False):
        word_dict = self
        if sorted:
            final_words = []
            for word, term in word_dict.dict.iteritems():
                #if term.valid > word_dict.id/2 and term.base_freq == 0:
                # Use this to save more word
                if term.valid > 0 and term.base_freq == 0:
                    final_words.append(word)

            final_words.sort(cmp = lambda x, y: cmp(word_dict.get_word(y).total_freq, word_dict.get_word(x).total_freq))
            
            with codecs.open(filename, 'w', 'utf-8') as file:
                for word in final_words:
                    v = word_dict.get_word(word).total_freq
                    file.write("%s %d\n" % (word,v))
        else:
            with codecs.open(filename,'w','utf-8') as file:
                for word, term in word_dict.dict.iteritems():
                    if term.valid > 0 and term.base_freq == 0:
                        file.write("%s %d\n" % (word,term.total_freq))




class Word(WordBase):
    """docstring for Word"""
    def __init__(self, id_):
        super(Word, self).__init__()
        self.process_freq = 1
        self.total_freq = 1
        self.valid = 0
        self.process_ps = 0.0
        self.id_ = id_
        self.l_len = 0
        self.r_len = 0
        self.l = collections.Counter()
        self.r = collections.Counter()
        self.base_freq = 0
        self.base_ps = 0.0
        self.curr_ps = 0.0

    # def __repr__(self):
    #     return str(self.__dict__)

    def add(self):
        self.process_freq += 1
        self.total_freq += 1

    def add_l(self,word):
        if word in self.l:
            self.l[word] += 1
        else:
            self.l[word] = 1
        self.l_len += 1

    def add_r(self,word):
        if word in self.r:
            self.r[word] += 1
        else:
            self.r[word] = 1
        self.r_len += 1

    def reset(self,id_):
        self.processfreq = 1
        self.id_ = id_
        self.l_len = 0
        self.r_len = 0
        self.l = collections.Counter()
        self.r = collections.Counter()


        