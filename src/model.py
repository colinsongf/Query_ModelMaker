import os, re, rw

class Model(object):
    def __init__(self, res_dir, fvq_dir, num_dir, r1, r2, min_ratio1, min_ratio2):
        self.res_dir = res_dir
        self.fvq_dir = fvq_dir
        self.num_dir = num_dir
        self.r1 = r1
        self.r2 = r2
        self.min_ratio1 = min_ratio1
        self.min_ratio2 = min_ratio2
        self.fvq = sum(self.r1.dic.values())
        self.num = sum(self.r2.dic.values())
        self.fvq_th = int(round(self.fvq * min_ratio1))
        self.num_th = int(round(self.num * min_ratio2))
        self.dic_fvq = self.r1.dic
        self.dic_num = self.r2.dic
        self.dic = {}
        self.dic_list = []
        self.type_dic = {}
        self.subtypes = r1.subtypes
        
    def filter(self):
        for key in self.dic_fvq:
            if (self.dic_fvq[key] >= self.fvq_th) and (self.dic_num[key] >= self.num_th):
                if key not in self.dic:
                    self.dic[key] = (self.dic_fvq[key],self.dic_num[key])
        content = ""
        result = sorted(self.dic.items(), key = lambda d: d[1][0])[::-1]
        path = self.res_dir + '/model_fvq.txt'
        for query,freq in result:
            line = (query + '\t' + str(freq) + '\n')
            content += line
        rw.writeFile(path,content)

        content = ""
        result = sorted(self.dic.items(), key = lambda d: d[1][1])[::-1]
        self.dic_list = result
        path = self.res_dir + '/model_num.txt'
        for query,freq in result:
            line = (query + '\t' + str(freq) + '\n')
            content += line
        rw.writeFile(path,content)

    def classification(self):
        for category in self.r1.type_dic:
            d = {}
            dic_fvq = self.r1.type_dic[category]
            dic_num = self.r2.type_dic[category]
            fvq = sum(self.r1.type_dic[category].values())
            num = sum(self.r2.type_dic[category].values())
            fvq_th = int(round(fvq * self.min_ratio1))
            num_th = int(round(num * self.min_ratio2))
            for key in dic_fvq:
                #if (dic_fvq[key] >= fvq_th) and (dic_num[key] >= num_th):
                if (key not in d) and (key in self.dic):
                    d[key] = (dic_fvq[key],dic_num[key])
            self.type_dic[category] = d

            content = ""
            result = sorted(d.items(), key = lambda d: d[1][0])[::-1]
            path = self.fvq_dir + '/' + category + '.txt'
            for query,freq in result:
                line = (query + '\t' + str(freq) + '\n')
                content += line
            rw.writeFile(path,content)
                
            content = ""
            result = sorted(d.items(), key = lambda d: d[1][1])[::-1]
            path = self.num_dir + '/' + category + '.txt'
            for query,freq in result:
                line = (query + '\t' + str(freq) + '\n')
                content += line
            rw.writeFile(path,content)
                

    
        
        
