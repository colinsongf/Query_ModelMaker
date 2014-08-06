import rw, re, os

class NEfilter(object):
    def __init__(self, src_dir, res_dir, total_dir, dic_dir):
        self.src_dir = src_dir
        self.res_dir = res_dir
        self.total_dir = total_dir
        self.dic_dir = dic_dir
        self.dic = {}
        self.query_dic = {}

    def readDictionary(self):
        files = os.listdir(self.dic_dir)
        for filename in files:
            if filename.endswith('.txt'):
                key = filename[0:-4]
                if (key not in self.dic):
                    path = self.dic_dir + '/' + filename
                    self.dic[key] = rw.readFile(path).split('\r\n')[0:-1]

    def find_word(self, word, key, txt):
        tag = '[' + key + ']'
        content = txt.replace(word,tag)
        return content

    def find_key(self, key, txt):
        content = txt
        for word in self.dic[key]:
            content = self.find_word(word,key,content)
        return content

    def find_NE(self, filename):
        src_path = self.src_dir + '/' + filename
        res_path = self.res_dir + '/' + filename
        txt = rw.readFile(src_path)
        content = ""
        for key in self.dic:
            txt = self.find_key(key,txt)
        p = re.compile('.*\[.+\].*')
        lines = p.findall(txt)
        for line in lines:
            content += (line + '\n')
        rw.writeFile(res_path,content)
        return content

    def addToDic(self, filename):
        src_path = self.src_dir + '/' + filename
        lines = rw.readFile(src_path).split('\n')[0:-1]
        for line in lines:
            temp = line.split('\t')
            if temp[0] in self.query_dic:
                self.query_dic[temp[0]] += int(temp[1])
            else:
                self.query_dic[temp[0]] = int(temp[1])

    def filter(self):
        self.readDictionary()
        files = os.listdir(self.src_dir)
        for filename in files:
            self.addToDic(filename)
            self.find_NE(filename)

    def sync(self):
        content = ""
        result = sorted(self.query_dic.items(),key = lambda d: d[1])[::-1]
        for query,freq in result:
            line = (query + '\t' + str(freq) + '\n')
            content += line
        for key in self.dic:
            content = self.find_key(key,content)
        txt = ""
        p = re.compile('.*\[.+\].*')
        lines = p.findall(content)
        for line in lines:
            txt += (line + '\n')
        rw.writeFile(self.total_dir,txt)
        return txt

    def run(self):
        self.filter()
        self.sync()
        
        
            
        
            
