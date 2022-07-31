# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。
"""
# 每家公司所有年份的合并dict
# 去除停用词后的所有年报的全路径
import os,pprint
import re
os.chdir(r'D:\Literature\盈余管理20210212\分词')

AnnualReports_path = r"D:\Literature\盈余管理20210212\年报原文"
stkcd_path = os.listdir(AnnualReports_path)
stkcd_path = [stk for stk in stkcd_path if re.match("\d",stk)]
# stkcd_path = [stk for stk in stkcd_path if float(stk)==601668]
for stk in stkcd_path:
    dropstopword_path = r".\\text_stop"+"\\" + stk + "\\" #去除停用词后分类语料库路径
    
    file_list = os.listdir(dropstopword_path)# 获取dropstopword目录下的所有文件，一个公司的所有年份的年报
    original_corpus = []
    print("正在合并%s的年报" %stk)
    for file_path in file_list: 
        file_name = dropstopword_path + file_path  #得到文件的全路径
        # print("正在打开%s" %file_name)
        file_read = open(file_name, 'r')  #打开一个文件
    
        # 对每个文件输出操作
        str_corpus = file_read.readlines()
        text_corpus = []
        for s in str_corpus:
            s = s.replace('\n','') #去掉换行符
            text_corpus.append(s)
        original_corpus.extend(text_corpus)
    
        file_read.close() #关闭打开的文件   
    # print(original_corpus)
    # print(len(original_corpus))
    
    # 导入字典    
    dict_path = r".\text_dict\%s\dict" %stk
    dict_file = open(dict_path,"r")
    dict_content = dict_file.read()
    dict_content = eval(dict_content)
    dict_file.close()
     
    dict_stkcd = dict()
    print("正在计算%s词频" %stk)
    for word in dict_content.keys():
        word_num = original_corpus.count(word)
        dict_stkcd[word] = word_num
    file_write = open(r'.\text_dict\%s\dict_stkcd' %stk,"w")
    file_write.write(str(dict_stkcd))
    file_write.close() 
      
    
# 每家公司各个年份的dicts
import os,pprint
import re
os.chdir(r'D:\Literature\盈余管理20210212\分词')

AnnualReports_path = r"D:\Literature\盈余管理20210212\年报原文"
stkcd_path = os.listdir(AnnualReports_path)
stkcd_path = [stk for stk in stkcd_path if re.match("\d",stk)]
# stkcd_path = [stk for stk in stkcd_path if 2500< float(stk) <300531]
for stk in stkcd_path:
    dropstopword_path = r".\\text_stop"+"\\" + stk + "\\" #去除停用词后分类语料库路径
    
    file_list = os.listdir(dropstopword_path)# 获取dropstopword目录下的所有文件，一个公司的所有年份的年报
    for file_path in file_list: 
        print("正在处理%s" %file_path)
        file_name = dropstopword_path + file_path  #得到文件的全路径
        # print("正在打开%s" %file_name)
        file_read = open(file_name, 'r')  #打开一个文件
    
        # 对每个文件输出操作
        str_corpus = file_read.readlines()
        text_corpus = []
        for s in str_corpus:
            s = s.replace('\n','') #去掉换行符
            text_corpus.append(s)
    
        file_read.close() #关闭打开的文件   
    # print(original_corpus)
    # print(len(original_corpus))
    
        # 导入字典    
        dict_path = r".\text_dict\%s\dict" %stk
        dict_file = open(dict_path,"r")
        dict_content = dict_file.read()
        dict_content = eval(dict_content)
        dict_file.close()
         
        dict_stkcd = dict()
        print("正在计算%s词频" %stk)
        for word in dict_content.keys():
            word_num = text_corpus.count(word)
            dict_stkcd[word] = word_num
        file_write = open(r'.\text_dict\%s\%s' %(stk,file_path),"w")
        file_write.write(str(dict_stkcd))
        file_write.close() 


###################################################
#  TFIDF
##################################################
# 计算tfidf平均值

import os
import numpy as np
import pandas as pd
# from openpyxl import workbook
# import openpyxl
# 获得每个txt的路径
os.chdir(r'D:\Literature\盈余管理20210212\分词')
root_path = '.\\text_tfidf\\'
stk_code = os.listdir(root_path)

# stk_path = [root_path + path + "\\" for path in stk_code]
# 列表生成式多层循环
# txt_path = [stk + path + "\\" for stk in stk_path for path in os.listdir(stk)]
'''读取每个txt,每个txt是一个列表，列表的元素是一个个的元组，每个元组由2个元素组成，tfidf值是元组的第2个元素'''
# [()，（），...,（）]
'''每个元素代表per 公司 per 年份,从000001-60xxxx，从2007-2019.'''
# tfidf_mean_list = []  
code_list = []
txt_list = []
mean_list = []
for code in stk_code:
    stk_path = root_path + code + "\\"
    txt_path = [stk_path + txt for txt in os.listdir(stk_path)]
    for txt in txt_path:
        f = open(txt,"r",encoding = 'utf-8')
        txt_content = f.readlines() 
        f.close()
        '''readlines() 方法用于读取所有行(直到结束符 EOF)并返回列表，
        该列表可以由 Python 的 for... in ... 结构进行处理。
        如果碰到结束符 EOF 则返回空字符串。'''
        txt_tfidf = txt_content[0]
        '''eval() 函数用来执行一个字符串表达式，并返回表达式的值'''
        tfidf_list = eval(txt_tfidf)  
        tfidf_value= [tf[1] for tf in tfidf_list]
#         print(tfidf_value)
        '''对每个txt（代表一个年度）的tfidf值进行算数平均，
        每个代码每个年度的年报的可读性由一个tdidf值来代表'''
        tfidf_mean = np.mean(tfidf_value)
        code_list.append(code)
        txt_list.append(txt)
        mean_list.append(tfidf_mean)
    print("已处理%s" %code)

df = pd.DataFrame([code_list,txt_list,mean_list]).T
df.columns = ["code","year","mean"]
df.to_excel(r'tfidf_mean.xlsx',index = False,encoding = 'utf-8')

# 向工作表添加数据,openpyxl can not handle .csv file.
#             workbook = openpyxl.load_workbook('.\\tfidf_values.xlsx')
#             sheet = workbook['Sheet1']
#             sheet = workbook.active
#             sheet.append([code,txt,tfidf_mean])
#             workbook.save('.\\tfidf_values.xlsx')
# print(tfidf_mean_list)









