import xml.etree.ElementTree as ET

class Channel:
    def __init__(self, filename="channel.xml"):
        self.filename = filename


    def getchannels(self):
        fin = open(self.filename,'r',encoding='utf-8').read()
        root = ET.fromstring(fin)
        
        for broadhead in root.iter('broadhead'):
            broadheadname = broadhead.get('text')
            channellist = []
            for child in broadhead.findall('./channel'):
                channel = {}           
                channel['title'] = child.find('title').text.strip()
                channel['text'] = child.find('text').text.strip()
                channel['link'] = child.find('link').text.strip()
                channel['type'] = child.get('type')
                channellist.insert(len(channellist),channel)         
            yield (broadheadname,channellist)





if __name__ == "__main__":
    pass