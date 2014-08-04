import rw, os

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

def sort(src_dir, res_dir, cols, min_f, suffix):
    query_log = os.listdir(src_dir)
    for filename in query_log:
        if filename.endswith(suffix):
            sort_file(src_dir, res_dir, filename, cols, min_f)


    
