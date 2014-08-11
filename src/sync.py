# sync.py
# Hongyu Li

# This module is for synchronizing the two sets of ranking into
# one final result

import rw, os

class Sync(object):
    # 'ratio': float type, the top ratio models we want from both rankings
    def __init__(self,m,r,res_dir,ratio):
        self.m = m
        self.r = r
        self.res_dir = res_dir
        self.ratio = ratio
        # The specific number of models we want
        self.count = int(round(len(m.dic) * ratio))
        self.dic_num = {}
        self.dic_score = {}
        self.type_dic = {}
        self.subtypes = m.subtypes
        self.dic = {}

    # init the query dic
    # only fetch the top ratio models
    def init_dic(self):
        dic_num_list = self.m.dic_list[0:self.count]
        dic_score_list = self.r.dic_list[0:self.count]
        for query in dic_num_list:
            self.dic_num[query[0]] = query[1][1]
        for query in dic_score_list:
            self.dic_score[query[0]] = query[1][1][1]
        return (dic_num_list,dic_score_list)

    # merge the two rankings together
    # write the result into the corresponding directory
    def update(self):
        self.dic_num.update(self.dic_score)
        self.dic = self.dic_num
        content = ""
        path = self.res_dir + '/General.txt'
        result = sorted(self.dic_num.items(), key = lambda d: d[1])[::-1]
        for query,num in result:
            line = (query + '\t' + str(num) + '\n')
            content += line
        rw.writeFile(path,content)

    # categorize the final result
    def classification(self):
        for category in self.m.type_dic:
            d = {}
            for key in self.dic_num:
                if (key not in d) and (category in key):
                    d[key] = self.dic_num[key]
            self.type_dic[category] = d

            content = ""
            result = sorted(d.items(), key = lambda d: d[1])[::-1]
            path = self.res_dir + '/' + category + '.txt'
            for query,num in result:
                line = (query + '\t' + str(num) + '\n')
                content += line
            rw.writeFile(path,content)

    # the main function
    def run(self):
        self.init_dic()
        self.update()
        self.classification()
