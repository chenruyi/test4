"""
从必应学术中获得主要的学术论文信息
"""
from urllib import request
import re
from bs4 import BeautifulSoup
#import codecs
URL = "https://www.bing.com/academic/"
html = request.urlopen(URL).read().decode("utf-8")
htmlfile = open("temp.html", "w", encoding="utf-8")
htmlfile.write("<html><head>......</head><body>")
soup = BeautifulSoup(html, "html.parser")
dic = {"title": "", "desc": "", "source": ""}
for new in soup.find_all("div", {"class": "acalp_news_item"}):
    dic["title"] = new.find(
        "div", {"class": "acalp_card_title"}).get_text()
    dic["desc"] = new.find(
        "div", {"class": "acalp_card_desc"}).get_text()
    dic["source"] = new.find(
        "div", {"class": "acalp_card_source"}).get_text()
    htmlfile.write("<h3>%s</h3>" %dic["title"])
    htmlfile.write("<p>%s</p>" %dic["desc"])
    htmlfile.write("<span>%s</span>" %dic["source"])
htmlfile.write("</body></html>")

