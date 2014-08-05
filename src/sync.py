import rw, os

class Sync(object):
    def __init__(self,m,r,res_dir,ratio):
        self.m = m
        self.r = r
        self.res_dir = res_dir
        self.ratio = ratio
        self.count = int(round(len(m.dic) * ratio))
        self.dic_num = {}
        self.dic_score = {}

    def init_dic(self):
        dic_num_list = self.m.dic_list[0:self.count]
        dic_score_list = self.r.dic_list[0:self.count]
        for query in dic_num_list:
            self.dic_num[query[0]] = query[1][1]
        for query in dic_score_list:
            self.dic_score[query[0]] = query[1][1][1]
        return (dic_num_list,dic_score_list)

    def update(self):
        self.dic_num.update(self.dic_score)
        content = ""
        result = sorted(self.dic_num.items(), key = lambda d: d[1])[::-1]
        for query,num in result:
            line = (query + '\t' + str(num) + '\n')
            content += line
        rw.writeFile(self.res_dir,content)

    def run(self):
        self.init_dic()
        self.update()
