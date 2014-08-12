Query ModelMaker

目录下包含3个文件 和 2 个文件夹
文件分别为：	readme.txt
		substitution.txt.utf8 --- 应用模板进行纠错替换的词典
		word.txt --- 模板中常出现的高频词词典

文件夹：	src --- 包含所有的代码，下面会详细说明
		NE --- 里面包含命名实体的词典，每项命名实体词典的txt文件的名称将会是对应类别的名称


以下是对于src地址下文件的说明
main.py --- 代码主程序，在终端中src目录下运行 python main.py 即可运行程序
	    其中对应不同的模块有不同的function做对应，在main.py中最下端是不同模块的运行
            第一次运行程序需要运行所有模块，再次运行时可以不用运行前两项，即pre_process() 与 filter()
	    不同模块的function中，具体保存文件的名称，源文件地址，系数等都可以进行适当修改

rw.py --- 包含关于文件读写的helper function

pre.py --- 这一模块是对于查询日志的预处理，可以选择原始日志中想获取的列，和设定最小sqv数量的设定
	   在main.py中对应的function为pre_process()，
	   其中cols是一个list，包含的数字为想获取的列，0即第一列，1即第二列，所以目前设定为[0,1]
	   min_f 是最小sqv数量，目前设定为20
           suffix指想进行预处理的查询日志文件的名称后缀，目前设定为'querystat'

sort.py --- 这一模块是在预处理的基础上再进行基于查询串长度的过滤
	    在main.py中对应的function为filter(),
	    其中min_char指所需最短字符串长度，目前设定为10，即两个中文字+4个英文或数字的长度
	    targets 不用管，与模板生成关系不大，目前设定为[]
	    suffix与之前相同

NEfilter.py --- 这一模块是对前两步处理后的结果进行命名实体词的定位并替换为对应类别的标签
                例如，变形金刚电影全集 --> [Movie]电影全集
		同时，所有被命名实体词命中的查询将会被挑出来，而其余未被命中的查询将被舍弃
		在main.py中对应的funciton为NEF()
		此模块与根目录的NE文件夹做对应，NE文件夹名称可做修改，但在NEF()中也需要做对应修改

rank.py --- 这一模块在上一步基础上过滤出一些具有特殊意义的数字
	    包括 第x季 / 第x部 / 第x集 / 第x期 / 日期 / 紧接在命名实体后面的数字被认定为电影的部数
	    这些数字将被替换为对应的标签
	    同时，模板的初步结果以及分类结果将会保存在设定的目录下
	    在main.py中对应的function为RANK()

model.py --- 这一模块是对于模板的初步挑选与处理
             在main.py中对应的function为MODEL()
   	     其中，min_ratio1为 (sqv / 总sqv) 的最小比例，即所选模板的sqv应大于(总sqv * min_ratio1)
	     min_ratio2为 (num / 总num) 的最小比例，即所选模板的num应大于(总num * min_ratio2)
 	     通过这一标准过滤出的模板会按照 sqv 大小 与 num 大小生成出两个排序
             其中关于num的排序更加重要，在之后的sync过程中会再使用到

remodel.py --- 这一模块是对于初步挑选后的模板进行一个再排序
	       在main.py中对应的function为REMODEL()
	       其中coeff_sqv是sqv的对应系数，目前设定为5
	       coeff_num是num的对应系数，目前设定为12
	       coeff_key是关键词出现次数的对应系数，目前设定为1
  	       对每一个模板，首先会计算两个比率，r1为(模板的sqv / 最大sqv)，0 < r1 < 1.0			       r2为(模板的num / 最大num), 0 < r2 < 1.0
	       然后会计算模板中高频词的出现个数c，此过程对应根目录中的word.txt
       	       最终会对每个模板计算出一个分数，score = r1 * coeff_sqv + r2 * coeff_num + c * coeff_key
               然后以这个分数从大到小有一个新的排序

sync.py --- 这一模块是将num排序和score排序两个不同的排序进行综合汇总
            方法是将两个排序的前50%的模板挑出来然后进行综合汇总，50%这个数值可以修改
            在main.py中对应的function为SYNC()
      	    其中ratio即两个排序中索取模板数量的比例
            例如，ratio = 0.3时，会从两个排序索取前30%的模板进行汇总
  	    运行完这一模块后会生成模板的最终结果

parse.py --- 这一模块是应用已生成的模板对查询进行分词
    	     在main.py中对应的function为PARSE()
	     其中num指对于每个文件所需要分词的查询的个数
   	     此模块中包含多个function，
   	     运行p.segment()可对于指定文件进行分词结果生成
	     运行p.segmentation()可对于制定目录下的所有文件进行分词结果生成
	     运行while循环内容，可循环进行对于手动输入的查询尽心分词结果生成

substitute.py --- 这一模块式应用已生成的模板，基于分词程序对查询进行纠错与替换
		  在main.py中对应的funciton为SUB()
		  其中num指对于每个文件所需要分词的查询的个数
		  运行sub.sub_all()可对于制定目录下的所有文件进行分词与纠错
		  运行while循环内容，可循环进行对于手动输入的查询尽心分词与纠错

pick.py --- 此模块已没有用处

analysis.py --- 此模块是应用于对生成的模板进行手动测定，并生成结果报告
		在main.py中对应的function是STAT()