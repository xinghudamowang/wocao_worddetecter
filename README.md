# Wocao提词器

---



## 功能

---

* 通过输入大段文字，学习到此内容产生的新老词语。
* 由获得的新老词库作为字典对输入对大段文本进行切词，也可以对其它的输入文本进行切词。

## 算法

---

* 使用“最大熵”算法来实现对大文本的新词发现能力，很适合使用它来创建自定义词典，或在SNS等场合进行数据挖掘的工作。
* 使用贝叶斯平均思想实现对大文本的新词发现能力，可以作为基础特征词库的baseline使用。


## 用法

---

* ```>>> from wocao import detecter```


* ```>>> worddict = detecter.WorDict()```


* 详细用例请见test.py模块。


* 可以将save_to_file方法保存的字典作为其它分词器的用户自定义字典。

[这是github，欢迎fork欢迎star。](https://github.com/xinghudamowang/wocao_worddetecter.git)

* https://github.com/xinghudamowang/wocao_worddetecter.git



