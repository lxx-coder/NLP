#!/usr/bin/env python
# coding: utf-8

# In[13]:


import urllib.request as request
import re
from bs4 import BeautifulSoup
import xlwt
import csv
import networkx as nx


# In[17]:

def url_request(url):
    resp = request.urlopen(url)
    html = resp.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


# In[21]:


src_url = "https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485"
host = "https://baike.baidu.com"


# In[24]:



def request_result(link_url, stationset):
    soup = url_request(link_url)
    tables = soup.find("table")
    stationmaps = {}
    if tables:
        for div in tables.find_all('div'):
            if "开往" in div.text: continue
            link = div.find('a', href=re.compile(r"/item/.+"), string=re.compile(r"\w+站"))
            if not link: continue
            station = link.string
            # if station in stationset: continue
            href =link.attrs['href']
            stationmaps[station] = host + href
        
    return stationmaps


def write_to_xls(stationmaps, book):
    row = 0
    col = 0
    sheet = book.add_sheet('station', cell_overwrite_ok=True)
    for key in stationmaps.keys():
        col = 0
        tmp1 = ""
        sheet.write(row,col,tmp1.decode('utf-8'))
        for value in stationmaps[key]:
            col += 1
            tmp2 = ""
            sheet.write(row,col, tmp2.join(value).decode('utf-8'))

        row += 1

    book.save(r'e:\test1.xls')

# 功能：将一字典写入到csv文件中
# 输入：文件名称，数据字典

def createDictCSV(fileName="", dataDict={}):
    with open(fileName, "w") as csvFile:
        csvWriter = csv.writer(csvFile)
        for k,v in dataDict.items():
            csvWriter.writerow([k]+v)
        csvFile.close()

# In[28]:


stationsets = set()
station_hrefs = {}
station_links = {}

# request_result("https://baike.baidu.com/item/%E5%9B%BD%E5%B1%95%E7%AB%99",stationsets)

soup = url_request(src_url)
tables = soup.find('table')
stationmaps = {}
for link in tables.findAll('a', href=re.compile(r"/item/.+"), string=re.compile(r"\w+站")):
    station = link.string
    href = link.attrs['href']
    stationmaps[station] = host+href

while stationmaps:
    keys = list(stationmaps.keys())

    for key in keys:
        if key in stationsets: 
            del stationmaps[key]
            continue


        stationsets.add(key)
        url_link = stationmaps[key]
        stations = request_result(url_link, stationsets)
        if not stations:
            del stationmaps[key]
            continue
        print("{}:{}".format(key, stations.keys()))
        station_links[key] = list(stations.keys())
        stationmaps.update(stations)
        del stationmaps[key]
        # if k > 10:
        #     createDictCSV(r"E:\test.csv",station_links)
        # k += 1

createDictCSV(r"E:\test.csv",station_links)



# In[ ]:




