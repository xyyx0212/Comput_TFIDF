# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 21:46:12 2021

@author: xyyx
"""

# 制作CSMAR_Var词典
'''连接csmar数据库'''
from csmarapi.CsmarService import CsmarService   
from csmarapi.ReportUtil import ReportUtil # 以表格形式展示数据

csmar = CsmarService()
csmar.login('znufe', 'znufe')
database = csmar.getListDbs()   # 查看已购买的数据库名称
ReportUtil(database)

tables = csmar.getListTables('股票市场交易') # 查看已购买的数据库内的数据表名称
ReportUtil(tables)

fields = csmar.getListFields('Trd_Co')  #查看已购买的数据表下的字段名称
ReportUtil(fields)

data = csmar.preview('TRD_Co') # 预览数据表
ReportUtil(data)

csmar.queryCount(['Cuntrycd','Stkcd','Stknme','Conme'], "Stkcd like'3%'", 'TRD_Co')   #查询已购买的数据表记录条数  
#csmar.queryCount(['Cuntrycd','Stkcd','Stknme','Conme'], "Stkcd like'3%'", 'TRD_Co' ,'2010-01-01','2019-12-31')
# columns：字段的列表，如： ['Cuntrycd','Stkcd','Stknme','Conme']
# condition：条件，类似SQL条件语句，如："Stkcd='000001'"， 但不支持order by(该函数已有默认的排序方式)
# tableName：表名称，可通过getListTables(databaseName)查看
# startTime和endTime：时间关键字参数(非必填，如需填写格式为：YYYY-MM-DD):下载数据时间区间的开始时间和结束时间

data = csmar.query(['Cuntrycd','Stkcd','Stknme','Conme'], "Stkcd like'3%'", 'TRD_Co')  # 查询已购买的数据表数据   
#data = csmar.query(['Cuntrycd','Stkcd','Stknme','Conme'], "Stkcd like'3%'", 'TRD_Co','2010-01-01','2019-12-31')    ReportUtil(data)

# 一次最多只能加载200,000条记录
# columns：字段的列表，如： ['Cuntrycd','Stkcd','Stknme','Conme']
# condition：条件，类似SQL条件语句，如："Stkcd='000001'"， 但不支持order by(该函数已有默认的排序方式)
# 如超过20万记录的数据可使用limit进行分页查询,假设是40万条，需分两次进行条件设置

# 如：第一次："Stkcd like'3%' limit 0,200000"， 第二次："Stkcd like'3%' limit 200000,200000"

# tableName：表名称，可通过getListTables(databaseName)查看
# startTime和endTime：时间关键字参数(非必填，如需填写格式为：YYYY-MM-DD):下载数据时间区间的开始时间和结束时间

csmar.getPackResultExt(['Cuntrycd','Stkcd','Stknme','Conme'], "Stkcd like'3%'", 'TRD_Co')   # 下载数据函数并获取打包结果函数
#csmar.getPackResultExt(['Cuntrycd','Stkcd','Stknme','Conme'], "Stkcd like'3%'", 'TRD_Co' ,'2010-01-01','2019-12-31')
# columns：字段的列表，如： ['Cuntrycd','Stkcd','Stknme','Conme']
# condition：条件，类似SQL条件语句，如："Stkcd='000001'"， 但不支持order by(该函数已有默认的排序方式)
# tableName：表名称，可通过getListTables(databaseName)查看
# startTime和endTime：时间关键字参数(非必填，如需填写格式为：YYYY-MM-DD):下载数据时间区间的开始时间和结束时间

csmar.unzipSingle('c:\\csmardata\\zip\\778639194952077312.zip')  # 解压下载的数据包函数
csmar.loadData('c:\\csmardata\\778639194952077312\\TRD_Co.csv') # 加载文件数据函数
