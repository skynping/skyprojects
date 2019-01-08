# coding: utf-8
from lxml import etree


# 分析网页源码，运用xpath筛选出需要的内容
class analyse_spider:
    def __init__(self,html,xpath_lists):
        self.html = html
        self.xpath_lists = xpath_lists

    # 获取筛选出的内容
    def get_content_lists(self):
        html_xpath = etree.HTML(self.html)
        contents = html_xpath.xpath(self.xpath_lists['root'])
        lists = []
        for content in contents:
            text = {}
            try:
                for key,value in self.xpath_lists.items():
                    if key != "root":
                        text[key] = content.xpath(value)[0].strip().encode("utf-8")
                        print key,text[key]
                lists.append(text)
                print "-"*100
            except:
                print u"分析出错！！"
        return lists

