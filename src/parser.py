# parser.py
# Hongyu Li

# This module is for segmentating the queries according to the models

import os, re, rw

class Parser(object):
    def __init__(self, m, src_dir, res_dir, num, suffix):
        self.m = m
        self.src_dir = src_dir
        self.res_dir = res_dir
        self.types = m.type_dic.keys()
        self.subtypes = m.subtypes
        self.dic = {}
        self.num = num
        self.suffix = suffix

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

    # partition the given query by tags
    # return a list of segments
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

    # transform the models into regular expression strings
    # and init the regexp dic
    def generalize(self):
        dic = self.m.dic
        for key in dic:
            tag_list = self.partition(key)
            k = key
            # '%' sign is for segmentation
            # change the category tags into '%.+%'
            for t in self.types:
                tag = '[' + t + ']'
                k = k.replace(tag,'%.+%')
            # transformation of the sub-types
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
            # segmentate the regexp into groups
            segs = k.split('%')
            l = []
            for seg in segs:
                if seg != '':
                    l.append(seg)
            segs = l
            new_segs = []
            new_tags = []
            # This part is for merging the '.+'
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
            # wrap each segment with '()'
            # aiming for separating in groups
            for seg in new_segs:
                k += ('(' + seg + ')')
            k = ('^' + k + '$')

            # initialize the dic
            if k not in self.dic:
                self.dic[k] = {key:new_tags}
            else:
                self.dic[k][key] = new_tags

            # add the permutation part
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

    # return the longest regexp that matches the query perfectly
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

    # returns the longest regexp that matches the query partially
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


    # the parse function
    # 'tag': a tuple of possible tags that describe the given query
    #        'tag' can be 'None'
    # returns a list of tuples
    # in each tuple, the first element is a segment of the query
    # the second element is a tuple of corresponding tags to the segment
    def parse(self,query,tag=None):
        #print "********************"
        #print 'Segmenting: %s' % query
        exp = self.matcher(query)
        #print "With expression: %s" % exp
        #if tag == None:
        #    print "With tag: None"
        #else:
        #    print "With tag: %s" % str(tag)
        #print "********************"
        if exp == None:
            return [(query,('None',))]
        elif (query == "") or (query.isspace()):
            return []
        else:
            p = re.compile(exp)
            a = re.compile('\^(\(\.\+\))+\$')
            b = re.compile('^(\(\.\+\))+$')
            # if query is all number, stop recursing
            # return the query with corresponding tag
            if query.isdigit():
                if tag != None and tag[0] in self.subtypes:
                    word = (query, tag)
                    return [word]
                else:
                    word = (query, ('num',))
                    return [word]
            # if the result of the total matching is only '.+'
            # use the partial matcher
            elif re.match(a,exp) != None:
                max_exp = self.max_matcher(query)
                result = re.compile(max_exp).findall(query)
                #print "Max_exp: %s" % max_exp
                if re.match(b,max_exp) != None:
                    # if the partial matching result is only '.+'
                    # stop recursing, return the query with tags
                    # tag the non-recognizable part as 'word'
                    if tag == None:
                        word = (query,('word',))
                    else:
                        word = (query,tag)
                    return [word]
                else:
                    # keep recursing otherwise
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
                # parse the query recursively
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

    # a helper function that deletes the spaces in the given query
    def del_space(self,query):
        new = ""
        p = re.compile('\S+')
        segs = p.findall(query)
        for seg in segs:
            new += seg
        return new

    # returns a long string containing the result of segmentation and
    # the corresponding categoires to each segment
    def run(self,query):
        if self.dic == {}:
            self.generalize()
        words = self.parse(self.del_space(query))
        query = ""
        tags = ""
        line = ""
        if len(words) > 1:
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
                        #print line
            line = query + ' : ' + tags
        return line

    # segmentation of the queries in the given file
    def segment(self,filename):
        print "********************"
        print "Segmenting File: %s" % filename
        src_path = self.src_dir + '/' + filename
        res_path = self.res_dir + '/' + filename
        query_log = rw.readFile(src_path).split('\n')[0:self.num]
        content = ""
        for line in query_log:
            temp = line.split('\t')
            #print "Segmenting: %s" % temp[0]
            segmented = self.run(temp[0])
            if segmented != "":
                print "Segmenting: %s" % temp[0]
                query = temp[0] + '\t' + segmented + '\t' + temp[1] + '\n'
                content += query
        rw.writeFile(res_path,content)

    # segmentation of all files in the source directory
    def segmentation(self):
        files = os.listdir(self.src_dir)
        for filename in files:
            if filename.endswith(self.suffix):
                self.segment(filename)
            
                
            
            
                    
