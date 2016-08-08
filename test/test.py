#coding:utf-8
import codecs
from wocao import detecter

symbol = re.compile('[\uD800-\uDBFF][\uDC00-\uDFFF]')

def testWordDict(from_path,save_path):
	worddict = detecter.WordDict()
    with open(path,'rb') as f:
        for line in f:
            line_without_symbol = symbol.sub('',line.split('\t')[-1].strip('\n'))
            # line_without_symbol = num_lett.sub('',line_without_symbol)
            if len(line_without_symbol) ==0:
                # print 'skip'
                continue
            else:
                # yield line_without_symbol
                # t.append(line_without_symbol)
                worddict.learn_chinese(line_without_symbol)
    worddict.learn_flush()

    str = '我们的读书会也顺利举办了四期'
    seg_list = word_dict.cut(str)
    print ', '.join(seg_list)

    word_dict.save_to_file(str = '我们的读书会也顺利举办了四期'
    seg_list = word_dict.cut(str)
    print ', '.join(seg_list)

    word_dict.save_to_file(file_save))

    return worddict