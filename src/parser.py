import os, re, rw

class Parser(object):
    def __init__(self, m, src_dir, res_dir):
        self.m = m
        self.src_dir = src_dir
        self.res_dir = res_dir
        self.types = m.type_dic.keys()
        self.subtypes = m.subtypes
        self.dic = {}

    def permutations(self,a):
        # returns a list of all permutations of the list a
        if (len(a) == 0):
            return [[]]
        else:
            allPerms = [ ]
            for subPermutation in self.permutations(a[1:]):
                for i in xrange(len(subPermutation)+1):
                    allPerms += [subPermutation[:i] + [a[0]] + subPermutation[i:]]
            return allPerms

    def partition(self,query):
        query = query.replace('[','%')
        query = query.replace(']','%')
        segs = query.split('%')
        new_segs = []
        for seg in segs:
            if seg != '':
                if seg.isalpha() == False:
                    new_segs.append("model")
                else:
                    new_segs.append(seg)
        return new_segs
    
    def generalize(self):
        dic = self.m.dic
        for key in dic:
            tag_list = self.partition(key)
            k = key
            for t in self.types:
                tag = '[' + t + ']'
                k = k.replace(tag,'%.+%')
            for sub_t in self.subtypes:
                tag = '[' + sub_t + ']'
                if sub_t == 'yyyymmdd':
                    k = k.replace(tag,'%[1-2][0-9][0-9][0-9]\.?[0-1][0-9]\.?[0-3][0-9]%')
                elif sub_t == 'yyyymm':
                    k = k.replace(tag,'%[1-2][0-9][0-9][0-9]\.?[0-1][0-9]%')
                elif sub_t == 'yyyy':
                    k = k.replace(tag,'%[1-2][0-9][0-9][0-9]%')
                else:
                    k = k.replace(tag,'%.+%')
            segs = k.split('%')
            l = []
            for seg in segs:
                if seg != '':
                    l.append(seg)
            segs = l
            new_segs = []
            new_tags = []
            for i in xrange(len(segs)):
                seg = segs[i]
                tag = tag_list[i]
                if seg != '':
                    if seg != '.+':
                        new_segs.append(seg)
                        new_tags.append(tag)
                    else:
                        if new_segs != []:
                            if new_segs[-1] != '.+':
                                new_segs.append(seg)
                                new_tags.append(tag)
                            else:
                                new_tags[-1] += ('+' + tag)
                        else:
                            new_segs.append(seg)
                            new_tags.append(tag)

            k = ""
            for seg in new_segs:
                k += ('(' + seg + ')')
            k = ('^' + k + '$')
            if k not in self.dic:
                self.dic[k] = {key:new_tags}
            else:
                self.dic[k][key] = new_tags
            """
            pair_list = zip(new_segs,tag_list)
                    
            all_perms = self.permutations(pair_list)
            for perm in all_perms:
                segs,tags = zip(*perm)
                k = ""
                for seg in segs:
                    k += ('(' + seg + ')')

                k = ('^' + k + '$')
            
                if k not in self.dic:
                    self.dic[k] = {key:tags}
                else:
                    self.dic[k][key] = tags
            """
        return self.dic

    def matcher(self,query):
        dic = self.dic
        max_length = 0
        max_exp = ""
        for exp in dic:
            p = re.compile(exp)
            if re.match(p,query) != None:
                #print "Exp: %s" % exp
                if len(exp) > max_length:
                    max_length = len(exp)
                    max_exp = exp
        return max_exp

    def max_matcher(self,query):
        dic = self.dic
        max_length = 0
        max_exp = ""
        for exp in dic:
            exp = exp[1:-1]
            p = re.compile(exp)
            result = p.findall(query)
            if result != []:
                if len(exp) > max_length:
                    max_length = len(exp)
                    max_exp = exp
        return max_exp
            

    def check_group(self,query):
        exp = self.matcher(query)
        p = re.compile(exp)

    def parse(self,query,tag=None):
        print "********************"
        print 'Segmenting: %s' % query
        exp = self.matcher(query)
        print "With expression: %s" % exp
        if tag == None:
            print "With tag: None"
        else:
            print "With tag: %s" % str(tag)
        print "********************"
        if exp == None:
            return [(query,('None',))]
        elif (query == "") or (query.isspace()):
            return []
        else:
            p = re.compile(exp)
            a = re.compile('\^(\(\.\+\))+\$')
            b = re.compile('^(\(\.\+\))+$')
            if query.isdigit():
                if tag != None and tag[0] in self.subtypes:
                    word = (query, tag)
                    return [word]
                else:
                    word = (query, ('num',))
                    return [word]
                    
                """
                if len(query) == 8:
                    word = (query, ('yyyymmdd',))
                    return [word]
                elif len(query) == 6:
                    word = (query, ('yyyymm',))
                    return [word]
                elif len(query) == 4:
                    word = (query, ('yyyy',))
                    return [word]
                else:
                    word = (query, ('num',))
                    return [word]
                """
            elif re.match(a,exp) != None:
                max_exp = self.max_matcher(query)
                result = re.compile(max_exp).findall(query)
                #print "Max_exp: %s" % max_exp
                if re.match(b,max_exp) != None:
                    if tag == None:
                        word = (query,('word',))
                    else:
                        word = (query,tag)
                    return [word]
                else:
                    query_seg = ""
                    for seg in result[0]:
                        query_seg += seg
                    unknown = query.split(query_seg)
                    for i in xrange(len(unknown)):
                        if unknown[i] != "":
                            unknown[i] = (unknown[i], ('word',))
                    words = self.parse(query_seg,tag)
                    return [unknown[0]] + words + [unknown[1]]
            else:
                m = re.match(p,query)
                segs = m.groups()
                words = []
                tags = zip(*self.dic[exp].values())
                for i in xrange(len(segs)):
                    seg = segs[i]
                    if (seg in exp):
                        if (seg != ""):
                            word = (seg,('model',))
                            words += [word]
                    else:
                        words += self.parse(seg,tags[i])
                return words

    def del_space(self,query):
        new = ""
        p = re.compile('\S+')
        segs = p.findall(query)
        for seg in segs:
            new += seg
        return new
    
    def run(self,query):
        if self.dic == {}:
            self.generalize()
        words = self.parse(self.del_space(query))
        for word in words:
            if word != "":
                if word[0] != "":
                    line = (word[0] + '\t')
                    for tag in word[1]:
                        line += (tag + ' | ')
                    print line
        return line

    def segmentation(self):
        files = os.listdir(self.src_dir)
        for filename in files:
            print "********************"
            print "Segmenting File: %s" % filename
            src_path = self.src_dir + '/' + filename
            res_path = self.res_dir + '/' + filename
            query_log = rw.readFile(src_path).split('\n')[0:-1]
            content = ""
            for line in query_log:
                temp = line.split('\t')
                print "Segmenting: %s" % temp[0]
                query = temp[0] + '\t' + self.run(temp[0]) + '\t' + temp[1] + '\n'
                content += query
            rw.writeFile(res_path,content)
            
                
            
            
                    
