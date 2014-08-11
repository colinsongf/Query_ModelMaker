# main.py
# Hongyu Li

import os, sys, re
import rw, pre, sort
import NEfilter, rank, model, parser, pick, remodel, analysis, sync, substitute
    

# pre-processing module
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

    
# filtering module
def filter():
    try:
        os.mkdir("../sorted")
    except:
        pass
    try:
        os.mkdir("../result")
    except:
        pass
    
    # Source directory name
    src_dir = "../pre"
    # The directory name you save the filtered query log
    tar_dir = "../sorted"
    # The path of the result report
    result_dir = "../result"
    # The minimum length of the query you expect
    min_char = 10
    # The list of keywords you want to check for frequency
    targets = []
    # The filename suffix of the files you want to filter
    suffix = 'querystat'
    
    print "********************"
    print "Sorting..."
    # Creating an instance of the 'Filter' class
    f = sort.Filter(src_dir,tar_dir,result_dir,min_char,targets,suffix)
    f.sort_files()
    print "Sorting complete!"

    
# Named entities filtering module
def NEF():
    try:
        os.mkdir("../NEfilter")
    except:
        pass
    try:
        os.mkdir("../total")
    except:
        pass

    # Source directory name
    src_dir = "../sorted"
    # The directory where you want to store the filtered query logs
    res_dir = "../NEfilter"
    # The path of the merged query log, one single file
    total_dir = "../total/total.txt"
    # The directory of the NE dictionary
    dic_dir = "../NE"
    
    print "********************"
    print "NE Fitering..."
    # Create an instance of the 'NEfilter' class
    f = NEfilter.NEfilter(src_dir,res_dir,total_dir,dic_dir)
    f.run()
    print "NEF complete!"
    return f

    
# Ranking module
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

    # Source directory name
    src_dir = "../total"
    # The path of the result report
    res_dir = "../result/rank_init.txt"
    # The directory to save categorized results
    class_dir = "../result/sqv"
    # The ranking mode, ordered by sqv
    mode = "sqv"
    # Create an instance of the 'ranker' class
    r1 = rank.ranker(src_dir,res_dir,class_dir,mode)
    # Ranking & Classification
    r1.rank()
    r1.classification(f)

    # Source directory name
    src_dir = "../total"
    # The path of the result report
    res_dir = "../result/rank_init_num.txt"
    # The directory to save categorized results
    class_dir = "../result/num"
    # The ranking mode, ordered by num
    mode = "num"
    # Create another instance of the 'ranker' class
    r2 = rank.ranker(src_dir,res_dir,class_dir,mode)
    # Ranking & Classification
    r2.rank()
    r2.classification(f)

    print "Total number: %d" % sum(r2.dic.values())
    print "Total frequency: %d" % sum(r1.dic.values())
    print "Length: %d <-> %d" % (len(r1.dic),len(r2.dic))
    print "Ranking complete!"
    return (r1,r2)

# Initial models generating module
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

    # The directory where you save the initial list of models
    res_dir = "../model"
    # The directory for results ordered by sqv
    fvq_dir = "../model/sqv"
    # The directory for results ordered by num
    num_dir = "../model/num"
    # The minimum ratio of (sqv / total sqv) you expect
    min_ratio1 = 0.00002
    # The minimum ratio of (num / total num) you expect
    min_ratio2 = 0.00015

    print "********************"
    print "Modeling..."
    # Create an instance of the 'Model' class
    m = model.Model(res_dir,fvq_dir,num_dir,r1,r2,min_ratio1,min_ratio2)
    # Filtering & Classification
    m.filter()
    m.classification()
    print "Modeling complete!"
    return m

# Pick high frequency words module
# No usage
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

# Remodeling module
def REMODEL(m):
    try:
        os.mkdir("../remodel")
    except:
        pass

    # Coefficient of the ratio (sqv / sqv_max)
    coeff_sqv = 5
    # Coefficient of the ratio (num / num_max)
    coeff_num = 12
    # Coefficient of the number of keywords
    coeff_key = 1
    # The directory where you want to save your results
    res_dir = "../remodel"
    # The path of the high frequency keywords dictionary
    dict_dir = "../word.txt"
    
    print "********************"
    print "Remodeling..."
    # Create an instance of the 'Remodel' class
    r = remodel.Remodel(m,coeff_sqv,coeff_num,coeff_key,res_dir,dict_dir)
    r.run()
    print "Remodeling complete!"
    return r

# Model testing module
# This module is for checking the quality of the models artificially
def STAT():
    try:
        os.mkdir("../stat")
    except:
        pass
    print "********************"
    print "Initiating statistics..."

    # Source directory name
    src_dir = "../final/General.txt"
    # The path of the result report
    res_dir = "../stat/result_final2.txt"
    
    # Create an instance of the 'Analysis' class
    s = analysis.Analysis(src_dir,res_dir)
    s.run()

# Model ranking sychronization module
def SYNC(m,r):
    try:
        os.mkdir("../final")
    except:
        pass

    # The directory where you save the final results
    res_dir = "../final"
    # The ratio of top models you want to fetch for both rankings
    ratio = 0.5

    print "********************"
    print "Synchronizing..."
    # Create an instance of the 'Sync' class
    syn = sync.Sync(m,r,res_dir,ratio)
    syn.run()
    print "Synchronizing complete!"
    return syn

# Parsing module
def PARSE(m):
    try:
        os.mkdir("../seg")
    except:
        pass

    # Source directory name
    src_dir = "../sorted/"
    # Result directory name
    res_dir = "../seg"
    # Number of queries you want to segment from each file
    num = 10000
    # The expected file suffix
    suffix = "querystat"
    
    print "********************"
    print "Matching..."
    # Create an instance of the 'Parser' class
    p = parser.Parser(m,src_dir,res_dir,num,suffix)
    

    # Uncomment this line to run the parsing function on a given file
    #p.segment("youku_20140719.all.querystat")

    # Uncomment this line to segment all files in src_dir
    #p.segmentation()

    # Uncomment this part to parse the input query
    """
    while True:
        query = raw_input("Enter a query: ")
        p.run(query)
    """
    return p

# Substituting module
def SUB(p):
    try:
        os.mkdir("../../test_result")
    except:
        pass

    # The path of the substitution dictionary
    dic_dir = "../substitution.txt.utf8"
    # Source directory name
    src_dir = "../../test"
    # Result directory name
    res_dir = "../../test_result"
    # The number of queries for segmentation in each file
    num = 20000
    # The expected file suffix
    suffix = "querystat"

    print "********************"
    print "Substituting..."
    # Create an instance of the 'Substitute' class
    sub = substitute.Substitute(p,dic_dir,src_dir,res_dir,num,suffix)
    # Substitution of all files in src_dir
    sub.sub_all()

    # Uncomment this part to parse & subsititue the input query
    """
    while True:
        query = raw_input("Enter a query: ")
        print sub.run(query)
    """



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
p = PARSE(syn)
SUB(p)
