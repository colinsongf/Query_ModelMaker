# rank.py
# Hongyu Li

# This module is for further filtering import keywords
# and ranking the queries in two orders: sqv and num
# (num is the number of appearances)

import re, os, rw

class ranker(object):
    # 'src_dir': string type, the source directory, should be one file
    # 'res_dir': string type, the directory where you want the store the results
    # 'class_dir': string type, the directory to save categorized results
    # 'mode': string type, 'sqv' or 'num'
    def __init__(self, src_dir, res_dir, class_dir, mode):
        self.src_dir = src_dir
        self.res_dir = res_dir
        self.class_dir = class_dir
        self.mode = mode
        self.dic = {}
        self.type_dic = {}
        self.subtypes = ['Season','Episode','yyyymmdd','yyyymm','yyyy','Part']

    # get the whole query log in the 
    def get_text(self):
        files = os.listdir(self.src_dir)
        content = ""
        for filename in files:
            if filename == 'total.txt':
                path = self.src_dir + '/' + filename
                txt = rw.readFile(path)
                content += txt
        return content

    # filter the 'season' number
    def check_season(self, query):
        p = re.compile('\xe7\xac\xac.+\xe5\xad\xa3')
        s = set(p.findall(query))
        for key in s:
            tag = '\xe7\xac\xac[Season]\xe5\xad\xa3'
            query = query.replace(key,tag)
        return query

    # filter the 'episode' number
    def check_episode(self,query):
        p = re.compile('\xe7\xac\xac.+\xe9\x9b\x86')
        s = set(p.findall(query))
        for key in s:
            tag = '\xe7\xac\xac[Episode]\xe9\x9b\x86'
            query = query.replace(key,tag)
        p = re.compile('\xe7\xac\xac.+\xe6\x9c\x9f')
        s = set(p.findall(query))
        for key in s:
            tag = '\xe7\xac\xac[Episode]\xe6\x9c\x9f'
            query = query.replace(key,tag)
        return query

    # filter the dates
    def check_date(self,query):
        p = re.compile('[1-2][0-9][0-9][0-9]\.?[0-1][0-9]\.?[0-3][0-9]')
        s = set(p.findall(query))
        for key in s:
            tag = '[yyyymmdd]'
            query = query.replace(key,tag)

        p = re.compile('[1-2][0-9][0-9][0-9]\.?[0-1][0-9]')
        s = set(p.findall(query))
        for key in s:
            tag = '[yyyymm]'
            query = query.replace(key,tag)

        p = re.compile('[1-2][0-9][0-9][0-9]')
        s = set(p.findall(query))
        for key in s:
            tag = '[yyyy]'
            query = query.replace(key,tag)
        return query

    # filter the 'part' number
    def check_part(self,query):
        p = re.compile('(\[TV\]\d+|\[Movie\]\d+|\[Show\]\d+|\[Animation\]\d+)')
        s = set(p.findall(query))
        for key in s:
            tag = '[Part]'
            if 'TV' in key:
                tag = '[TV][Part]'
            elif 'Movie' in key:
                tag = '[Movie][Part]'
            elif 'Show' in key:
                tag = '[Show][Part]'
            elif 'Animation' in key:
                tag = '[Animation][Part]'
            query = query.replace(key,tag)

        p = re.compile('\xe7\xac\xac.+\xe9\x83\xa8')
        s = set(p.findall(query))
        for key in s:
            tag = '\xe7\xac\xac[Part]\xe9\x83\xa8'
            query = query.replace(key,tag)
        return query
            

    # init the query dictionary with values of sqv
    def addToDict_fvq(self):
        lines = self.get_text().split('\n')[0:-1]
        for line in lines:
            query = ""
            temp = line.split('\t')
            p = re.compile('\S+')
            segs = p.findall(temp[0])
            for seg in segs:
                query += seg
            query = self.check_season(query)
            query = self.check_episode(query)
            query = self.check_date(query)
            query = self.check_part(query)
            if query in self.dic:
                self.dic[query] += int(temp[1])
            else:
                self.dic[query] = int(temp[1])
        return self.dic

    # init the query dictionary with values of num
    def addToDict_num(self):
        lines = self.get_text().split('\n')[0:-1]
        for line in lines:
            query = ""
            temp = line.split('\t')
            p = re.compile('\S+')
            segs = p.findall(temp[0])
            for seg in segs:
                query += seg
            query = self.check_season(query)
            query = self.check_episode(query)
            query = self.check_date(query)
            query = self.check_part(query)
            if query in self.dic:
                self.dic[query] += 1
            else:
                self.dic[query] = 1
        return self.dic

    # rank the filtered results and save as a file in the result directory
    def rank(self):
        content = ""
        if self.mode == "sqv":
            result = sorted(self.addToDict_fvq().items(), key = lambda d: d[1])[::-1]
        elif self.mode == "num":
            result = sorted(self.addToDict_num().items(), key = lambda d: d[1])[::-1]
        for query,freq in result:
            line = (query + '\t' + str(freq) + '\n')
            content += line
        rw.writeFile(self.res_dir,content)
        return content

    # make separate rankings in different categories
    def classification(self, nef):
        for category in nef.dic:
            path = self.class_dir + '/' + category + '.txt' 
            d = {}
            for key in self.dic:
                if category in key:
                    if key not in d:
                        d[key] = self.dic[key]
            if category not in self.type_dic:
                self.type_dic[category] = d
            content = ""
            result = sorted(d.items(),key = lambda d: d[1])[::-1]
            for query,freq in result:
                line = (query + '\t' + str(freq) + '\n')
                content += line
            rw.writeFile(path,content)
