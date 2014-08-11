# pre.py
# Hongyu Li

# This file contains helper functions that help to pre-process the files or contents

import rw, os

# pre-process the given 'txt' according to 'cols' and 'min_f'
# 'txt': string type, the contents you want to pre-process
# 'cols': list type, the columns you want from the query log
# 'min_f': int type, the minimum sqv you want
def sort_txt(txt,cols,min_f):
    query_list = txt.split('\n')[0:-1]
    query_list_sorted = []
    content_sorted = ""

    for query in query_list:
        temp = query.split('\t')
        freq = int(temp[cols[-1]])
        if freq >= min_f:
            line = ""
            for i in xrange(len(cols)-1):
                line += (temp[cols[i]] + '\t')
            line += temp[cols[-1]]
            content_sorted += (line + '\n')
    return content_sorted

# pre-process the given file
# 'src_dir': the source directory
# 'res_dir': the result directory
# 'filename': the name of the given file
# 'cols': list type, the columns you want from the query log
# 'min_f': int type, the minimum sqv you want
def sort_file(src_dir, res_dir, filename, cols, min_f):
    print "Pre-processing file: %s" % filename
    src_path = src_dir + '/' + filename
    res_path = res_dir + '/' + filename
    content = rw.readFile(src_path)
    query_list = content.split('\n')[0:-1]

    #constants
    query_list_sorted = []
    content_sorted = ""

    for query in query_list:
        temp = query.split("\t")
        freq = int(temp[cols[-1]])
        if freq >= min_f:
            line = ""
            for i in xrange(len(cols)-1):
                line += (temp[cols[i]] + '\t')
            line += temp[cols[-1]]
            content_sorted += (line + '\n')
    rw.writeFile(res_path,content_sorted)
    return content_sorted

# pre-process all files in the source directory
# 'src_dir': the source directory
# 'res_dir': the result directory
# 'cols': list type, the columns you want from the query log
# 'min_f': int type, the minimum sqv you want
# 'suffix': the ending suffix of the files you want to pre-process
def sort(src_dir, res_dir, cols, min_f, suffix):
    query_log = os.listdir(src_dir)
    for filename in query_log:
        if filename.endswith(suffix):
            sort_file(src_dir, res_dir, filename, cols, min_f)


    
