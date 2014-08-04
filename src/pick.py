import sys, re, os, rw

class ranker(object):
    def __init__(self, src_dir, res_dir, dict_dir, rank_dir, min_num, ratio):
        self.src_dir = src_dir
        self.res_dir = res_dir
        self.dict_dir = dict_dir
        self.rank_dir = rank_dir
        self.min_num = min_num
        self.dictionary = {}
        self.ch = re.compile('[\x80-\xff]+')
        self.w1 = re.compile('[\x80-\xff]{3}')  
        self.w2 = re.compile('[\x80-\xff]{6}')  
        self.w3 = re.compile('[\x80-\xff]{9}')  
        self.w4 = re.compile('[\x80-\xff]{12}')
        self.w5 = re.compile('[\x80-\xff]{15}')
        self.wl = [self.w1,self.w2,self.w3,self.w4,self.w5]
        self.dic_word = {}
        self.ratio = ratio

    def get_words(self,seg):
        l = []
        #l += self.w1.findall(seg)
        l += self.w2.findall(seg)  
        l += self.w2.findall(seg[3:])  
        l += self.w3.findall(seg) 
        l += self.w3.findall(seg[3:])  
        l += self.w3.findall(seg[6:])  
        l += self.w4.findall(seg) 
        l += self.w4.findall(seg[3:])  
        l += self.w4.findall(seg[6:])  
        l += self.w4.findall(seg[9:])
        l += self.w5.findall(seg)
        l += self.w5.findall(seg[3:])
        l += self.w5.findall(seg[6:])
        l += self.w5.findall(seg[9:])
        l += self.w5.findall(seg[12:])
        return l
        
        
    def analyze(self):
        files = os.listdir(self.src_dir)
        for filename in files:
            path = self.src_dir + '/' + filename
            if os.path.isdir(path) == False:
                txt = rw.readFile(path)

                segs = self.ch.findall(txt)
                for seg in segs:
                    words = self.get_words(seg)
                    for word in words:
                        if (word in self.dictionary):
                            self.dictionary[word] += 1
                        else:
                            self.dictionary[word] = 1
        return self.dictionary

    def init_result(self):
        content = ""
        result = sorted(self.analyze().items(),key=lambda d: d[1])[::-1]
        for word,num in result:
            if num >= self.min_num:
                line = (word + ':' + str(num) + '\n')
                content += line
        rw.writeFile(self.res_dir,content)
        return content

    def rank(self):
        dictionary = rw.readFile(self.dict_dir).split("\n")[0:-1]
        dic = set()
        sample = rw.readFile(self.res_dir).split("\n")[0:-1]
        words = {}
        high_freq = []
        content = ""

        for line in dictionary:
            temp = line.split("\t")
            dic.add(temp[0])

        for line in sample:
            temp = line.split(":")
            if (temp[0] in dic):
                high_freq.append(line)

        limit = int(round(len(high_freq) * self.ratio))
        for line in high_freq[:limit]:
            #content += (line + "\n")
            temp = line.split(':')
            content += (temp[0] + '\n')
            self.dic_word[temp[0]] = int(temp[1])

        rw.writeFile(self.rank_dir,content)
