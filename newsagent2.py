"""
能够实现百度新闻rss转换成GUI表格
"""
from urllib import request
import xml.etree.ElementTree as ET
import re

from tkinter import ttk
from tkinter import Tk
from tkinter import StringVar, VERTICAL, NSEW, NS
"""
表示数据
"""


class NewsItem:
    """
    包括标题和主体文本的简单新闻项目。
    """

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.Format()

    def Format(self):
        self.body['pubDate'] = re.compile(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}').findall(self.body['pubDate'])
        self.body['description'] = re.sub(r'<a.*?</a>', '',
                                          self.body['description'])
        self.body['description'] = re.sub(r'<br\W{0,1}>', '',
                                          self.body['description'])


class RSSSource:
    """
    从RSS中获取新闻项目的新闻来源。
    """

    def __init__(self, rssurl):
        self.rssurl = rssurl

    def getItems(self):
        xmlcontents = request.urlopen(self.rssurl).read().decode("utf-8")
        root = ET.fromstring(xmlcontents)
        for itemElement in root.iter("item"):
            title = itemElement.find("title").text
            body = {}
            for child in itemElement:
                if child.tag != "title":
                    body[child.tag] = child.text

            yield NewsItem(title, body)


class MianWindow:
    def __init__(self):
        self.urlstr = None
        self.items = None
        self.frame = Tk()
        self.frame.title('RSS 阅读')
        self.frame_top = ttk.Frame(self.frame)
        self.UrlLabel = ttk.Label(self.frame_top, text='RSS来源：')
        self.urlentrystr = StringVar()
        self.urlentry = ttk.Entry(
            self.frame_top, textvariable=self.urlentrystr)
        self.SureBtn = ttk.Button(
            self.frame_top, text='确定', command=self.button_submitUrl)
        self.frame_center = ttk.Frame(
            self.frame, width=self.frame.winfo_screenwidth())
        self.frame_center_left = ttk.Frame(self.frame, height=self.frame.winfo_height(), width=200)
        self.frame_top.grid(row=0, column = 0)
        self.frame_center.grid(row=1, column=1)
        self.frame_center_left.grid(row=1, column=0)
        self.UrlLabel.grid(row=0, column=0)
        self.urlentry.grid(row=0, column=1)
        self.SureBtn.grid(row = 0, column = 2)
        self.tree = ttk.Treeview(
            self.frame_center,
            show='headings',
            height=18,
            columns=('时间', '作者', '题目'))
        self.vbar = ttk.Scrollbar(
            self.frame_center, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vbar.set)

        #表格标题
        # if self.tree.children[0]['时间']:
        #     w1 = len(self.tree.children['时间'])
        # else:
        w1 = 100
        # if self.tree.children[0]['题目']:
        #     w2 = len(self.tree.children[0]['题目'])
        # else:
        w2 = 100
        # if self.tree.children[0]['内容']:
        #     w3 = len(self.tree.children[0]['内容'])
        # else:
        w3 = 300
        self.tree.column('时间', width=w1, anchor='center')
        self.tree.column('作者', width=w2, anchor='center')
        self.tree.column('题目', width=w3, anchor='center')
        self.tree.heading('时间', text='时间')
        self.tree.heading('作者', text='作者')
        self.tree.heading('题目', text='题目')

        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

    def receiveItems(self, items):
        self.items = items

    def getItems(self):
        #map(self.tree.delete, self.tree.get_children())
        #self.tree.delete(self.tree.children)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.items:
            self.tree.insert('','end',\
            values=(item.body['pubDate'],item.body['author'],item.title))

    def GetUrl(self):
        if self.urlstr:
            return self.urlstr
        else:
            return 'http://news.baidu.com/n?cmd=1&class=civilnews&tn=rss'

    def button_submitUrl(self):
        s = self.urlentrystr.get()
        if re.match(r'^https?://\w.+$', s):
            self.urlstr = s
            runDefaultSetup()
        else:
            self.urlstr = None


def runDefaultSetup():
    """
    来源和目标的默认设置
    """
    contents = RSSSource(win.GetUrl())
    items = contents.getItems()
    win.receiveItems(items)
    win.getItems()
    win.frame.mainloop()


if __name__ == '__main__':
    defaulturl = 'http://news.baidu.com/n?cmd=1&class=civilnews&tn=rss'
    win = MianWindow()
    runDefaultSetup()