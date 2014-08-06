import os, sys, re, rw, pre, sort, NEfilter, rank, model, parser, pick, remodel, analysis, sync

def make_dir():
    os.mkdir("../pre")
    os.mkdir("../sorted")
    os.mkdir("../result")
    os.mkdir("../NEfilter")
    os.mkdir("../result/num")
    os.mkdir("../result/fvq")
    os.mkdir("../model")
    os.mkdir("../model/fvq")
    os.mkdir("../model/num")
    

def pre_process():
    try:
        os.mkdir("../pre")
    except:
        pass
    src_dir = "../YKQueryLog" # The directory name of the query log
    res_dir = "../pre" # The result directory name of the pre-processed query log
    cols = [0,1] # The column number you want to keep from the query log
    min_f = 20 # The minimum number of frequency you want
    suffix = "querystat" # The suffix of the filename of the query logs
    print "********************"
    print "Pre-processing..."
    pre.sort(src_dir,res_dir,cols,min_f,suffix)
    print "Pre-processing complete!"

def filter():
    try:
        os.mkdir("../sorted")
    except:
        pass
    try:
        os.mkdir("../result")
    except:
        pass
    src_dir = "../pre"
    tar_dir = "../sorted"
    result_dir = "../result"
    min_char = 10
    targets = []
    suffix = 'querystat'
    print "********************"
    print "Sorting..."
    f = sort.Filter(src_dir,tar_dir,result_dir,min_char,targets,suffix)
    f.sort_files()
    print "Sorting complete!"

def NEF():
    try:
        os.mkdir("../NEfilter")
    except:
        pass
    try:
        os.mkdir("../total")
    except:
        pass
    src_dir = "../sorted"
    res_dir = "../NEfilter"
    total_dir = "../total/total.txt"
    dic_dir = "../NE"
    print "********************"
    print "NE Fitering..."
    f = NEfilter.NEfilter(src_dir,res_dir,total_dir,dic_dir)
    f.run()
    print "NEF complete!"
    return f

def RANK(f):
    try:
        os.mkdir("../result/num")
    except:
        pass
    try:
        os.mkdir("../result/sqv")
    except:
        pass
    print "********************"
    print "Ranking..."
    src_dir = "../total"
    res_dir = "../result/rank_init.txt"
    class_dir = "../result/sqv"
    mode = "sqv"
    r1 = rank.ranker(src_dir,res_dir,class_dir,mode)
    r1.rank()
    r1.classification(f)

    src_dir = "../total"
    res_dir = "../result/rank_init_num.txt"
    class_dir = "../result/num"
    mode = "num"
    r2 = rank.ranker(src_dir,res_dir,class_dir,mode)
    r2.rank()
    r2.classification(f)
    print
    print "Total number: %d" % sum(r2.dic.values())
    print "Total frequency: %d" % sum(r1.dic.values())
    print "Length: %d <-> %d" % (len(r1.dic),len(r2.dic))
    print "Ranking complete!"
    return (r1,r2)

def MODEL(r1,r2):
    try:
        os.mkdir("../model")
    except:
        pass
    try:
        os.mkdir("../model/sqv")
    except:
        pass
    try:
        os.mkdir("../model/num")
    except:
        pass
    
    print "********************"
    print "Modeling..."
    res_dir = "../model"
    fvq_dir = "../model/sqv"
    num_dir = "../model/num"
    min_ratio1 = 0.00002
    min_ratio2 = 0.00015
    m = model.Model(res_dir,fvq_dir,num_dir,r1,r2,min_ratio1,min_ratio2)
    m.filter()
    m.classification()
    print "Modeling complete!"
    return m

def PARSE(m):
    try:
        os.mkdir("../seg")
    except:
        pass
    print "********************"
    print "Matching..."
    src_dir = "../0719"
    res_dir = "../seg/0719"
    p = parser.Parser(m,src_dir,res_dir)
    #p.segmentation()
    while True:
        query = raw_input("Enter a query: ")
        p.run(query)
    print "********************"

def PICK():
    print "********************"
    print "Picking..."
    src_dir = "../model"
    res_dir = "../result/highsqv_nonword.txt"
    dict_dir = "../P+A.hash"
    rank_dir = "../result/highsqv_word.txt"
    min_num = 0
    ratio = 0.2
    p = pick.ranker(src_dir,res_dir,dict_dir,rank_dir,min_num,ratio)
    print "Initializing..."
    p.init_result()
    print "Sorting..."
    p.rank()
    return p

def REMODEL(m):
    try:
        os.mkdir("../remodel")
    except:
        pass
    print "********************"
    print "Remodeling..."
    coeff_fvq = 5
    coeff_num = 12
    coeff_key = 1
    res_dir = "../remodel"
    dict_dir = "../word.txt"
    r = remodel.Remodel(m,coeff_fvq,coeff_num,coeff_key,res_dir,dict_dir)
    r.run()
    print "Remodeling complete!"
    return r

def STAT():
    try:
        os.mkdir("../stat")
    except:
        pass
    print "********************"
    print "Initiating statistics..."
    src_dir = "../final/General.txt"
    res_dir = "../stat/result_final2.txt"
    s = analysis.Analysis(src_dir,res_dir)
    s.run()

def SYNC(m,r):
    try:
        os.mkdir("../final")
    except:
        pass
    print "********************"
    print "Synchronizing..."
    res_dir = "../final"
    ratio = 0.5
    syn = sync.Sync(m,r,res_dir,ratio)
    syn.run()
    print "Synchronizing complete!"
    return syn
    

reload(sys)
sys.setdefaultencoding('utf8')

#pre_process()

#filter()

f = NEF()

(r1,r2) = RANK(f)

m = MODEL(r1,r2)

#PARSE(m)

#p = PICK()

r = REMODEL(m)

syn = SYNC(m,r)

#STAT()

PARSE(syn)
