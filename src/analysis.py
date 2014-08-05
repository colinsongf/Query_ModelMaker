import rw, os, sys

class Analysis(object):
    def __init__(self, src_dir, res_dir):
        #self.m = m
        self.src_dir = src_dir
        self.res_dir = res_dir
        self.models = []
        self.dic = {}
        self.success = 0
        self.failure = 0

    def init_model(self):
        lines = rw.readFile(self.src_dir).split('\n')[0:-1]
        for line in lines:
            temp = line.split('\t')
            self.models.append(temp[0])

    def filter(self):
        i = 0
        while i < len(self.models):
            model = self.models[i]
            ask = model + ': '
            ans = raw_input(ask)
            if ans == 'y':
                self.success += 1
                self.dic[model] = (i,1,self.success,self.failure)
                i += 1
            elif ans == 'n':
                self.failure += 1
                self.dic[model] = (i,0,self.success,self.failure)
                i += 1
            else:
                print "Not a valid response!"
        print "Filtering complete!"
        content = ""
        result = sorted(self.dic.items(), key = lambda d: d[1][0])
        for query,score in result:
            line = (query + '\t' + str(score) + '\n')
            content += line
        rw.writeFile(self.res_dir,content)

    def run(self):
        self.init_model()
        self.filter()
                
            
        
