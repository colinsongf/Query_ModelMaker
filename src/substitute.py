# substitute.py
# Hongyu Li

# This module is to further implement spelling correction / word substitution
# on the basis of the parsing module

import os, rw, pre

class Substitute(object):
    def __init__(self, p, dic_dir, src_dir, res_dir, num, suffix):
        self.p = p
        self.dic_dir = dic_dir
        self.src_dir = src_dir
        self.res_dir = res_dir
        self.num = num
        self.suffix = suffix
        self.dictionary = {}

    # init the spelling correction dictionary
    def init_dic(self):
        lines = rw.readFile(self.dic_dir).split('\n')[0:-1]
        for line in lines:
            temp = line.split('\t')
            self.dictionary[temp[0]] = temp[1]
        return self.dictionary

    # search in the dicitonary and substitute the given word
    def sub_word(self,word):
        if word in self.dictionary:
            word = self.dictionary[word]
        return word

    # subsititute the given query
    # returns a list of tuples containing segments and tags
    # or returns None if there is no substitution
    def sub_query(self,query):
        if self.p.dic == {}:
            self.p.generalize()
        pairs = self.p.parse(self.p.del_space(query))
        new_pairs = []
        count = 0
        for pair in pairs:
            if pair != "":
                word = pair[0]
                tags = pair[1]
                if tags[0] != 'model':
                    new = self.sub_word(word)
                    if new != word:
                        count += 1
                    word = new
                new_pairs.append((word,tags))
        if count != 0:
            return new_pairs
        else:
            return None

    # returns a long string containing the result of segmentation and
    # the corresponding categoires to each segment after substitution
    def run(self,query):
        if self.dictionary == {}:
            self.init_dic()
        words = self.sub_query(query)
        query = ""
        tags = ""
        line = ""
        if words != None and len(words) > 1:
            for word in words:
                if word != "":
                    if word[0] != "":
                        query += (word[0] + '/')
                        tag_str = "("
                        for tag in word[1]:
                            if tag not in tag_str:
                                tag_str += (tag + ',')
                        tag_str = tag_str[0:-1] + ')'
                        tags += (tag_str + '/')
            line = query + ' : ' + tags
            print line
        return line

    # substitution of the given file
    def sub(self,filename):
        print "********************"
        print "Substituting File: %s" % filename
        src_path = self.src_dir + '/' + filename
        res_path = self.res_dir + '/' + filename
        txt = pre.sort_txt(rw.readFile(src_path),[0,1],20)
        query_log = txt.split('\n')[0:self.num]
        content = ""
        for line in query_log:
            temp = line.split('\t')
            substituted = self.run(temp[0])
            if substituted != "":
                print "Substituting: %s" % temp[0]
                query = temp[0] + '\t' + substituted + '\t' + temp[1] + '\n'
                content += query
        rw.writeFile(res_path,content)

    # substitution of all files in the source directory
    def sub_all(self):
        files = os.listdir(self.src_dir)
        for filename in files:
            if filename.endswith(self.suffix):
                self.sub(filename)
            
