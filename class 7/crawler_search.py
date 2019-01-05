# coding=utf-8
from bs4 import BeautifulSoup
import urllib
import urllib.request as request
import re
import socket
import time
import random
import os

socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
header = {'User-Agent': 'Mozilla/5.0'}

class_src_url = "http://www.pcbbbs.com/forum.php?mod=forumdisplay&fid=80"

# src_url = ["http://www.pcbbbs.com/forum.php?mod=forumdisplay&fid=80&page=" + str(i+1) for i in range(10)]
# host_url = "http://www.pcbbbs.com"

def url_request(url):
    req = request.Request(url, headers=header)
    try:
        resp = request.urlopen(req)
        html = resp.read().decode("gbk", 'ignore')
        soup = BeautifulSoup(html, "html.parser")
        resp.close()
        return soup
    except urllib.error.URLError as e:
        print(e.reason)
        return []
    except:
        return []

def request_result(link_url):
    soup = url_request(link_url)
    tables = soup.find("table", id= "threadlisttableid")
    # if tables

class_link = {}
soup = url_request(class_src_url)
tbodys = soup.find('div', id="forumleftside")
dds = tbodys.find_all('dd')
for dd in dds:
    a = dd.find('a')
    title = a.attrs['title']
    link = a.attrs['href']
    class_link[title] = link

# for url in src_url
if not os.path.exists('result'):
    os.mkdirs('result')

for title, link in class_link.items():
    file_title = re.sub(r"[\/\\\:\*\?\<\>\|]","",title)
    # file_name = "crawler/" + file_title + ".txt"
    # if os.path.exists(file_name):
    #     continue
    title_link = {}
    for src_url in [link + "&page=" + str(i+1) for i in range(10)]:
        url_soup = []
        i = 0
        url_soup = url_request(src_url)
        while i < 10 and not url_soup:
            time.sleep(1000*random.random())
            i += 1
            url_soup = url_request(src_url)
        if not url_soup:
            print("connect failed...")
            print("{}".format(src_url))
            continue
        # if not url_soup: continue
    # tables = soup.find("table", id= "threadlisttableid")
        url_tbodys = url_soup.find_all("tbody", id=re.compile("normalthread"))
        if url_tbodys:
            for tbody in url_tbodys:
                th = tbody.find("th")
                if not th: continue
                href = th.find("a", href=re.compile(r"http://www.pcbbbs.com/.+"), attrs={"class":"s xst"})
                # print(href)
                tmp_link = href.attrs['href']
                tmp_title = href.text
                # print("{} url   {}:{}".format(title, tmp_title,tmp_link))
                # title = re.sub(r"[\/\\\:\*\?\<\>\|]","",title)
                title_link[tmp_title] = tmp_link

                tmp_title = re.sub(r"[\/\\\:\*\?\<\>\|]","",tmp_title)
                file_name = "result/" + tmp_title + ".txt"
                # if os.path.exists(file_name):
                #     continue
                try:
                    with open(file_name, 'w', encoding='utf-8') as f:
                        # for content_title, content_link in title_link.items():
                        content_title = tmp_title
                        content_link = tmp_link
                        print("{} content   {}:{}".format(title, content_title,content_link))

                        content_soup = []
                        i = 0
                        content_soup = url_request(content_link)
                        while i < 10 and not content_soup:
                            time.sleep(1000 * random.random())
                            i += 1
                            content_soup = url_request(content_link)
                        if not content_soup:
                            print("connect failed...")
                            print("{}".format(content_link))
                            continue
                        # content_soup = url_request(content_link)
                        content_td = content_soup.find('td', id=re.compile("postmessage"))
                        if not content_td: continue
                        f.write(content_td.text.strip() + "\n")

                except:
                    continue

        # print("{}:{}".format(title,link))
