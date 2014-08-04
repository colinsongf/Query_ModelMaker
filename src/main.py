import os, sys, re, rw, pre, sort, NEfilter, rank, model, parser, pick, remodel

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
    src_dir = "../sorted"
    res_dir = "../NEfilter"
    dic_dir = "../NE"
    print "********************"
    print "NE Fitering..."
    f = NEfilter.NEfilter(src_dir,res_dir,dic_dir)
    f.filter()
    print "NEF complete!"
    return f

def RANK(f):
    try:
        os.mkdir("../result/fvq")
        os.mkdir("../result/num")
    except:
        pass
    print "********************"
    print "Ranking..."
    src_dir = "../NEfilter"
    res_dir = "../result/rank_init.txt"
    class_dir = "../result/fvq"
    mode = "fvq"
    r1 = rank.ranker(src_dir,res_dir,class_dir,mode)
    r1.rank()
    r1.classification(f)

    src_dir = "../NEfilter"
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
        os.mkdir("../model/fvq")
        os.mkdir("../model/num")
    except:
        pass
    print "********************"
    print "Modeling..."
    res_dir = "../model"
    fvq_dir = "../model/fvq"
    num_dir = "../model/num"
    min_ratio1 = 0.00005
    min_ratio2 = 0.0001
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
    res_dir = "../result/highfvq_nonword.txt"
    dict_dir = "../P+A.hash"
    rank_dir = "../result/highfvq_word.txt"
    min_num = 0
    ratio = 0.2
    p = pick.ranker(src_dir,res_dir,dict_dir,rank_dir,min_num,ratio)
    print "Initializing..."
    p.init_result()
    print "Sorting..."
    p.rank()
    return p

def REMODEL(m,p):
    try:
        os.mkdir("../remodel")
    except:
        pass
    print "********************"
    print "Remodeling..."
    coeff_fvq = 20
    coeff_num = 20
    coeff_key = 1
    res_dir = "../remodel"
    dict_dir = "../word.txt"
    r = remodel.Remodel(m,p,coeff_fvq,coeff_num,coeff_key,res_dir,dict_dir)
    r.run()
    print "Remodeling complete!"
    print "********************"
    

reload(sys)
sys.setdefaultencoding('utf8')

#pre_process()

#filter()

f = NEF()

(r1,r2) = RANK(f)

m = MODEL(r1,r2)

#PARSE(m)

p = PICK()

REMODEL(m,p)

