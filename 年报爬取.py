# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 19:34:12 2020

@author: dell
"""
#抓取年报url
#从dta导入A股上市公司证券代码
import pandas as pd
import requests as req
from lxml import etree
import time,random
from fake_useragent import UserAgent
import re
import os

# cnstock_A = pd.read_stata(r'cnstock_A.dta')
# stkcd = cnstock_A['stkcd'].values.tolist()
# stkcd.sort()
# # 补足6位
# stkcd_A = []
# for s in stkcd:
#     s = str(s)
#     if len(s) == 1:
#         s = "00000" + s
#     elif len(s) == 2:
#         s = "0000" + s
#     elif len(s) == 3:
#         s = "000" + s
#     elif len(s) == 4:
#         s = "00" + s
#     elif len(s) == 5:
#         s = "0" + s
#     else:
#         pass
    
#     stkcd_A.append(s)

# #构造公告页面url
# # urls = [] 
# # for i in stkcd_A:
# #     i = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/%s/page_type/ndbg.phtml" %i
# #     urls.append(i)
# # http://quotes.money.163.com/f10/gsgg_000005,dqbg,5.html    
# #循环抓取每个公司的年报url
# logfile = open(r'logfile.csv','w')
# stkcds,titles,url_2s,dates,types = [],[],[],[],[]
# ua = UserAgent()  #useragent有时候不稳定
# for stk in stkcd_A:
#     print('正抓取%s的url，进度为%s/%s' %(stk,stkcd_A.index(stk),len(stkcd_A)))
#     for p in range(20):
#         url = "http://quotes.money.163.com/f10/gsgg_%s,dqbg,%s.html" %(stk,p)
#         headers = {'User-Agent': f'{ua.random}'}
#         #超时重试
#         i=True
#         while i:
#             try:
#                 notices = req.get(url,headers = headers,timeout = 5)
#                 if notices.status_code == 200:
#                     print("连接成功！")
#                     i = False
#             except:
#                 print("连接失败,try again")
#                 time.sleep(10)
#         if notices.status_code != 200:
#             logfile.write("代码为%s的公司第%s页的url抓取失败，跳过"%(stk,p) + '\n')
#             continue
#         notices = notices.content
#         notices = etree.HTML(notices)
#         if notices.xpath("//td[@class='align_c']/text()") == ['暂无数据']:
#             break
#         type = notices.xpath("//td[@class='td_text'][2]")
#         type = [ty.text for ty in type]
#         title = notices.xpath("//td[@class='td_text'][1]/a")
#         title = [ti.text for ti in title]
#         url_2 = notices.xpath("//td[@class='td_text'][1]/a/@href")
#         date = notices.xpath('''//td[@class="align_c"]''')
#         date = [d.text for d in date]
        
#         url_2 = ["http://quotes.money.163.com" + u for u in url_2]
#         stkcd = [stk]*len(url_2)
        
#         url_2s.extend(url_2)
#         titles.extend(title)
#         dates.extend(date)
#         types.extend(type)
#         stkcds.extend(stkcd)
        
#         time.sleep(random.random()*3)
    
# df =  pd.DataFrame([stkcds,titles,url_2s,dates,types]).T
# df.columns = ['stkcds','titles','url_2s','dates','types']
# df = df[df['types'].isin(['年度报告'])]
# df = df.dropna()
# #df = df[df['dates'].isin(['2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007'])]
# df.to_excel('重新爬取年度报告URL.xlsx', index=None)
# print("年报url重新爬取完成，请查看logfile.csv文件")
# logfile.close()


# 多篇循环爬取年报内容
import pandas as pd
import requests as req
from lxml import etree
import time,random
from fake_useragent import UserAgent
import re
import os

os.chdir(r'D:\Literature\盈余管理20210212\全部重做\年报原文')
# def drop_CS(df):
#     # 去掉补充版、更新版、已取消和英文版等年报
#     drop_list = df["titles"].tolist()
#     drop_list = [drop for drop in drop_list if re.search("补充|更新|英文版|取消",drop)]
#     for drop in drop_list:
#         df = df[~df["titles"].isin([drop])]
#     return df

ua = UserAgent()  #useragent有时候不稳定
df = pd.read_excel(r'重新爬取年度报告URL.xlsx')
# df = drop_CS(df) # 去掉补充版和更新版等年报
url_2s = df['url_2s'].values.tolist()
stkcds = df['stkcds'].values.tolist()
dates = df['dates'].values.tolist()
titles = df['titles'].values.tolist()

for url,stk,date,title in zip(url_2s[38553:],stkcds[38553:],dates[38553:],titles[38553:]):
    # if stk < 603378:
    #     continue
    title = re.sub(r'\*|:|\?|\n', "", title)
    TestPath = r'.//%s//%s_%s年报正文+%s.txt' %(stk,stk,date,title)  #r一定要加上
    if os.path.exists(TestPath):
        continue
    if int(date[:4])<2007:  #发布时间不早于2007年，即保留2007年及其之后的年报正文
        continue
    if not os.path.exists("%s" %stk):
        os.mkdir('%s' %stk)
    print("正在爬取%s的年报正文" %url)
    print("进度%s/%s" %(url_2s.index(url),len(url_2s)))
    headers = {'User-Agent': f'{ua.random}'}
    #超时重试
    i=True
    while i:
        try:
            response = req.get(url,headers = headers,timeout = 5)
            if response.status_code == 200:
                print("连接成功！")
                i = False
        except:
            print("连接失败，重新连接")
            time.sleep(10)

    tree = etree.HTML(response.content.decode())
    content = tree.xpath('''//div[@class='inner_box']/text()''') 
    # content = [c.text for c in content]
    # content = [re.sub(r'\u2002|\r',"",c) for c in content]
    content = "".join(content)
    content = url + "\n" + content 
    df1=pd.DataFrame([content])
    df1.to_csv(r'./%s/%s_%s年报正文+%s.txt' %(stk,stk,date,title), index = None)
    time.sleep(random.random()*3)

print("年报正文抓取完毕")


# 输出年报内容，使用stata进行清洗-删除目录、表格、数字、图片等非文本信息
# df.to_excel(r'./01-02年报内容（test).xlsx',index = None) #excel表格容量有限，不能储存完整的年报正文
# df.to_csv(r'./01-02年报内容（test).txt',index = None,sep = '#', encoding = 'utf-8')
# # DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None, header=True, index=True,
# #                  index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"',
# #                  line_terminator='\n', chunksize=None, tupleize_cols=None, date_format=None, doublequote=True,
# #                  escapechar=None, decimal='.')

# # stata清洗速度过慢，使用python进行清洗
# os.chdir(r'E:\论文ing\盈余管理与年报可读性\年报原文')

# # pd.read_csv(filepath_or_buffer, sep=',', delimiter=None, header='infer', 
# #             names=None, index_col=None, usecols=None, squeeze=False, 
# #             prefix=None, mangle_dupe_cols=True, dtype=None, engine=None, 
# #             converters=None, true_values=None, false_values=None, 
# #             skipinitialspace=False, skiprows=None, nrows=None, na_values=None,
# #             keep_default_na=True, na_filter=True, verbose=False, 
# #             skip_blank_lines=True, parse_dates=False, infer_datetime_format=False,
# #             keep_date_col=False, date_parser=None, dayfirst=False, iterator=False,
# #             chunksize=None, compression='infer', thousands=None, decimal=b'.', 
# #             lineterminator=None, quotechar='"', quoting=0, escapechar=None, 
# #             comment=None, encoding=None, dialect=None, tupleize_cols=False, 
# #             error_bad_lines=True, warn_bad_lines=True, skipfooter=0, 
# #             skip_footer=0, doublequote=True, delim_whitespace=False, 
# #             as_recarray=False, compact_ints=False, use_unsigned=False, 
# #             low_memory=True, buffer_lines=None, memory_map=False, 
# #             float_precision=None)
# df = pd.read_csv(r'01-02年报内容（test).txt',sep = '#', encoding = 'utf-8')
# contents = df['contents'].values.tolist()

# # 删除可能存在的目录
# contents_clean = []
# i=1
# with open(r'./python年报内容清洗.txt',"w",encoding = 'utf-8') as f:
#     for c in contents[:1]:
#         print('正在清洗第%s份年报' %i)
#         c = re.sub("\s{5,}目\s*?录[\d\D]*?[\r\n]\s{5,}","",c)
#         c = re.sub("[\r\n]\s*.*?…{5,}[\d\D]*?[\r\n]\s{5,}","",c)
#         contents_clean(c)
#         f.write(c)
        
#         i += 1
# f.close()

# 将清洗后的文本进行分词
    
    
    
    
    
    
    
    
    
    
