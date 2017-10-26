import xml.etree.ElementTree as ET

import sys
'''
将xml(str) 转换成为 html(str)
'''
class Handler:
    
    def __init__(self, xml_str):
        sys.out = open('temp.html','w', encoding='utf-8')
        self.xml = xml_str
    
    def XML2HTML(self):
        self.startPage()
        self.startHead()
        self.endHead()
        self.startBody()
        root = ET.fromstring(self.xml)  
        for item in root.iter('item'):
            for child in item:
                mname = 'start'+child.tag.capitalize()
                mathod = getattr(self, mname)
                if callable(mathod):
                    mathod()
                    doc = child.text
                    sys.out.write(doc)
                    mname = 'end' + child.tag.capitalize()
                    mathod = getattr(self, mname)
                    mathod()
        self.endBody()
        self.endPage()

    def addDoc(self, docs):
        sys.out.write(docs)

    def startPage(self):
        sys.out.write('<!DOCTYPE html><html>')
        sys.out.write('<meta http-equiv="content-type" content="text/html; charset=utf-8">')

    def endPage(self):
        sys.out.write('</html>')

    def startHead(self):
        sys.out.write('<head>')

    def endHead(self):
        sys.out.write('</head>')
    def startBody(self):
        sys.out.write('<body>')

    def endBody(self):
        sys.out.write('</body>')
    def startItem(self):
        sys.out.write('<div>')
    def endItem(self):
        sys.out.write('</div>')

    def startTitle(self):
        sys.out.write('<h3>')

    def endTitle(self):
        sys.out.write('</h3>')

    def startLink(self):
        pass
        # sys.out.write('<a href="%s">%s' % linkurl, linkurl)
    def endLink(self):
        sys.out.write('</a>')

    def startSource(self):
        sys.out.write('<span>')
    def endSource(self):
        sys.out.write('</span>')

    def startDescription(self):
        pass
        #sys.out.write('')
    def endDescription(self):
        pass
        # sys.out.write()
    def startPubdate(self):
        pass
    def endPubdate(self):
        pass
    def startAuthor(self):
        sys.out.write('<i>')
    def endAuthor(self):
        sys.out.write('</i>')
