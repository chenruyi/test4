"""
能够实现百度新闻rss转换成GUI表格
"""
from urllib import request
from urllib.parse import quote
import xml.etree.ElementTree as ET
import re

from tkinter import ttk
from tkinter import Tk
from tkinter import *
from virscrollbarframe import VerticalScrolledFrame
from channel import *
"""
表示数据
"""


class FormateNewsItem:
    """
    包括标题和主体文本的简单新闻项目。
    """

    def __init__(self, items):
        self.items = items
        self.rules = {}

    def defaultRule(self):
        # def pubdateFormate(text):
        #    return re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}').findall(text)
        def descripFormate(text):
            text = re.sub(r'<br\W*>','',text)
            text = re.sub(r'<a.*?</a>', '',text)
            return text
        defaultRule = {#'pubDate': pubdateFormate,\
                        'description':descripFormate }
        self.updateRule(defaultRule)

    def updateRule(self, rules):
        self.rules.update(rules)

    def formate(self):
        for item in self.items:
            for key,value in self.rules.items():
                if(item[key] == None):
                    continue
                item[key] =value(item[key])



class RSSSource:
    """
    从RSS中获取新闻项目的新闻来源。
    """

    def __init__(self, rssurl):
        self.rssurl = rssurl
        data = None
     #   headers={"Host": "news.baidu.com",
     #       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
     #       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
     #       #"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
     #       "Accept-Encoding": "gzip, deflat",
     #       "Connection": "keep-alive"}
        req = request.Request(self.rssurl)
        response = request.urlopen(req)
        self.xmlcontents =response.read().decode('utf-8')

    def getItems(self):
        root = ET.fromstring(self.xmlcontents)
        items= []
        for itemElement in root.iter('item'):
            item = {}
            for child in itemElement:
                item[child.tag]=child.text
            items.append(item)
        return items



class Table:
    def __init__(self,  *args):
        #title:表格标题
        #*args:表格的列属性名

        self.column = args
        self.items = [[]]
        self.cells = [[]]

    def clear(self):
        for rowcell in self.cells:
            for cell in rowcell:
                cell.destroy()
        self.items.clear()

    def insert(self, index = 'end', obj = None):
        if type(index) == str:
            if index == 'start':
                self.items.insert(0, [e for e in obj])
            else:
                self.items.append([e for e in obj])

            return
        self.items.insert(int( index),[e for e in obj])


    def draw(self, parent = None, **kw):
        if parent == "":
            pass
        if ' ' in kw:
            pass
        c = 0
        w =0
        color=["#E6E6E6", "#C8C8C8"]
        widthlist =[45,25,10]

        for c in range(len(self.items)):
            for w in range(len(self.items[0])):
                cell = Label(parent,width=widthlist[w], text = self.items[c][w],bg=color[c%2])
                cell.grid(row=c,column=w,padx=2,pady=2)



class MianWindow:
    def __init__(self):
        self.urlstr = None
        self.items = None
        self.root = Tk()
        self.root.title('RSS 阅读')
        #  self.root.resizable(0, 0)

        self.tooltip = None

        #menu
        menubar = Menu(self.root)
        menubar.add_command(label='新建(N)',command =self.button_submitUrl )
        menubar.add_command(label='查看(V)')
        menubar.add_command(label='精彩推荐(R)')
        self.root.configure(menu=menubar)


        self.frame_top = ttk.Frame(self.root)
        self.UrlLabel = ttk.Label(self.frame_top, text='添加频道')
        self.urlentrystr = StringVar()
        self.urlentry = ttk.Entry(
            self.frame_top, textvariable=self.urlentrystr)
        self.SureBtn = ttk.Button(
            self.frame_top, text='添加', command=self.button_submitUrl)
        self.frame_center_north = ttk.Frame(self.root, width=70,height=100)
        self.frame_center_south = ttk.Frame(self.root, width=70,height=100)


        self.frame_center_left = ttk.Frame(
            self.root, height =50 ,width=200)
        self.frame_top.grid(row=0, column=0, columnspan=3, sticky="N")
        self.frame_center_north.grid(row=1, column=1, sticky="N" + "W")
        self.frame_center_left.grid(
            row=1, column=0, rowspan=2, sticky="N" +"S" +"W")
        self.frame_center_south.grid(row=2, column=1, sticky="N" + "E")
        self.UrlLabel.grid(row=0, column=0)
        self.urlentry.grid(row=0, column=1)
        self.SureBtn.grid(row=0, column=2)

        #tree view 布局
        #self.treeviewFrame = VerticalScrolledFrame(self.frame_center_left)
        self.treeviewFrame = ttk.Frame(self.frame_center_left)
        self.treeviewFrame.grid(row=0,column=0)
        tree = ttk.Treeview(self.treeviewFrame,height=25)
        vbar = ttk.Scrollbar(self.frame_center_left, orient=VERTICAL,command=tree.yview)
        channel = Channel('channel.xml')
        for (head,items) in channel.getchannels():
            mybroadhead = tree.insert('',0,text=head)
            for item in items:
                tree.insert(mybroadhead,'end',text=item['text'],values=(item['link']))

        # myid0 = tree.insert('',0,text='分类焦点新闻',value=('1'))
        # myid01 = tree.insert(myid0,0,text='国内焦点',value=('0'))
        # myid02 = tree.insert(myid0,1,text='国际焦点',value=('1'))



        tree.configure(yscrollcommand = vbar.set)
        tree.grid(row=0,column=0,sticky=NSEW)
        vbar.grid(row=0,column=1,sticky=NS)


        def treelabelDoubleButton(event):
            item = tree.item(tree.identify_row(event.y))
            self.urlstr = item['values'][0]
            runDefaultSetup()
        #tree.bind('<Enter>',treelabelEnter)
        #tree.bind('<Leave>',treelabelMove)
        #tree.bind('ButtonRelease-1',treelabelEnter)
        tree.bind('<Double-Button-1>',treelabelDoubleButton)
        #tabel布局
        self.tableFrame = VerticalScrolledFrame(self.frame_center_north)
        self.tableFrame.grid(row=0,column=0)
        self.table = Table(['题目','时间','作者'])

        #description布局
        self.descripFrame = VerticalScrolledFrame(self.frame_center_south)
        self.descripFrame.grid(row=0,column=0)
        self.descriplabel = Label(self.descripFrame.interior,font=('宋体',16,'bold'),bg='#E6E6E6',wraplength=300,text='description',justify='center')
        self.descriplabel.grid(row=0,column=0)



    def receiveDescription(self,context=None):
        if context == None:
            context=self.items[0]['description']
        self.descriplabel.configure(text=context)

    def receiveItems(self, items):
        self.items = items


    def drawTable(self):
        self.table.clear()
        for item in self.items:
            self.table.insert('end',\
            (item['title'],item['pubDate'],item['author']))
        self.table.draw(self.tableFrame.interior)

    def GetUrl(self):
        if self.urlstr:
            return self.urlstr
        else:
            return 'http://news.baidu.com/n?cmd=1&class=civilnews&tn=rss'

    def button_submitUrl(self):
        s = self.urlentrystr.get().strip()
        if re.match(r'^https?://\w.+$', s):
            self.urlstr = s
            runDefaultSetup()
        # elif not s is None:
        #     #  http://news.baidu.com/ns?word=123&tn=newsrss&sr=0&cl=2&rn=20&ct=0
        #     self.urlstr = "http://news.baidu.com/ns?word="+quote(s)+"&tn=newsrss&sr=0&cl=2&rn=20&ct=0"
        #     runDefaultSetup()
        else:
            self.urlstr = None


def runDefaultSetup():
    """
    来源和目标的默认设置
    """
    contents = RSSSource(win.GetUrl())
    items = contents.getItems()
    newsitem = FormateNewsItem(items)
    newsitem.defaultRule()
    newsitem.formate()
    items=newsitem.items
    win.receiveItems(items)

    win.drawTable()
    win.receiveDescription()
    win.root.mainloop()


if __name__ == '__main__':
    defaulturl = 'http://news.baidu.com/n?cmd=1&class=civilnews&tn=rss'
    win = MianWindow()
    runDefaultSetup()