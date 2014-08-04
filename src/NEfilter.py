import rw, re, os

class NEfilter(object):
    def __init__(self, src_dir, res_dir, dic_dir):
        self.src_dir = src_dir
        self.res_dir = res_dir
        self.dic_dir = dic_dir
        self.dic = {}

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

    def filter(self):
        self.readDictionary()
        files = os.listdir(self.src_dir)
        for filename in files:
            self.find_NE(filename)
            
        
        
            
        
            
