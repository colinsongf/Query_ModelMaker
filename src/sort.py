# sort.py
# Hongyu Li

# This module aims to further filter the query log according to the
# expected length of the query

import rw, os

class Filter(object):
    # 'src_dir': string type, the source directory
    # 'tar_dir': string type, the directory you save the filtered query log
    # 'result_dir': string type, the path of the result report
    # 'min_char': int type, the minimum length of the query you expect
    # 'targets': list type, the list of keywords you want to check for frequency
    # 'suffix': string type, the filename suffix of the files you want to sort
    def __init__(self, src_dir, tar_dir, result_dir, min_char, targets, suffix):
        self.src_dir = src_dir
        self.tar_dir = tar_dir
        self.result_dir = result_dir
        self.min_char = min_char
        self.targets = targets
        self.suffix = suffix
        self.target_num_l = [0]*len(self.targets)
        self.target_freq_l = [0]*len(self.targets)

        self.total_num = 0
        self.total_num_sorted = 0
        self.total_freq = 0
        self.total_freq_sorted = 0

    def sort_file(self,filename):
        src_path = self.src_dir + "/" + filename
        tar_path = self.tar_dir + "/" + filename
        content = rw.readFile(src_path)
        query_list = content.split("\n")

        #constants
        num = len(query_list)
        num_sorted = 0
        freq = 0
        freq_sorted = 0
        query_list_sorted = []
        content_sorted = ""
        # sort the queries over min_char
        for query in query_list:
            temp = query.split("\t")
            if len(temp) > 1:
                freq += int(temp[-1])
            if len(temp[0]) >= self.min_char:
                query_list_sorted.append(temp[0] + "\t" + temp[-1])
                freq_sorted += int(temp[-1])
                for target in self.targets:
                    index = self.targets.index(target)
                    count = (temp[0].count(target) > 0) * 1
                    self.target_num_l[index] += count#temp[0].count(target)
                    self.target_freq_l[index] += count*int(temp[-1])

        num_sorted = len(query_list_sorted)
        self.total_num += num
        self.total_num_sorted += num_sorted
        self.total_freq += freq
        self.total_freq_sorted += freq_sorted

        result = ("Query Log: %s\n" % filename) \
               + ("Number of queries: %d\n" % num) \
               + ("Queries over %d bytes: %d\n" % (self.min_char,num_sorted)) \
               + ("Queries frequency: %d\n" % freq) \
               + ("Long queries frequency: %d\n" % freq_sorted) \
               + (("Long query ratio: %0.3f\n") % (float(num_sorted)/num)) \
               + (("Long query frequency ratio: %0.3f\n") % (float(freq_sorted)/freq))

        # recombine the sorted queries
        for query in query_list_sorted:
            content_sorted += (query + "\n")

        rw.writeFile(tar_path,content_sorted)
        return result

    def sort_files(self):
        query_log = os.listdir(self.src_dir)
        result = ""
        result_path = (self.result_dir + "/result.txt")
        for filename in query_log:
            if filename.endswith(self.suffix):
                result += (self.sort_file(filename) + "\n")

        report = ("Queries total number: %d\n" % self.total_num) \
               + ("Queries over %d bytes in total: %d\n" % (self.min_char,self.total_num_sorted)) \
               + ("Queries total frequency: %d\n" % self.total_freq) \
               + ("Long queries total frequency: %d\n" % self.total_freq_sorted) \
               + (("Long query ratio: %0.3f\n") % (float(self.total_num_sorted)/self.total_num)) \
               + (("Long query frequency ratio: %0.3f\n") % (float(self.total_freq_sorted)/self.total_freq))
               
        result += report
        result += "\n\n"
        for i in xrange(len(self.targets)):
            s = ("Long Queries: %d\n" % self.total_num_sorted) \
              + ("Number of '%s': %d\n" % (self.targets[i],self.target_num_l[i])) \
              + ("Long Queries frequency: %d\n" % self.total_freq_sorted) \
              + ("Frequency of '%s': %d\n" % (self.targets[i],self.target_freq_l[i])) \
              + ("Ratio: %0.3f\n" % (float(self.target_num_l[i])/self.total_num_sorted)) \
              + ("Frequency Ratio: %0.3f\n" % (float(self.target_freq_l[i])/self.total_freq_sorted)) \
              + "\n" 
            result += s
        rw.writeFile(result_path,result)
                
        
        
