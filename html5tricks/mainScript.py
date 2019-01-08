# coding: utf-8

from getIndexHtml import page_spider
from analyse_spider import analyse_spider
from MysqlHelp import MysqlHelp

import time
import random
import os

class analyse_file:
    def __init__(self):
        pass

    # 保存文件
    @classmethod
    def save_file(self,file,file_link,id):
        id = id.split("-")[-1]
        filename = file_link.split("/")[-1]
        filetype = filename.split(".")[-1]
        if filetype=="rar" or filetype=="zip":
            filename = './HTML5/src/' + id + "-" + filename
        else:
            filename = './HTML5/img/' + id + "-" + filename
        with open(filename,"wb") as f:
            f.write(file)

    @classmethod
    def makedir(self,filepath):
        isExists = os.path.exists(filepath)
        if isExists:
            return False
        else:
            os.makedirs(filepath)
            return True

    @classmethod
    def save_to_mysql(self,content_list):
        picture_link = content_list['picture_link']
        title = content_list['title']
        title_id = content_list['title_id']
        src_link = content_list['src_link']
        title_link = content_list['title_link']
        params = [picture_link,title,title_id,src_link,title_link]
        mysql = MysqlHelp(db="html5stricks", host="localhost", port=3307)
        sql = "insert ignore into message(picture_link,title,title_id,src_link,title_link) values(%s,%s,%s,%s,%s)"
        mysql.cud(sql=sql,params=params)

    @classmethod
    def initconfig(self):
        # 创建文件必要文件夹
        analyse_file.makedir("./HTML5/img")
        analyse_file.makedir("./HTML5/src")

def mainSpider(url):
    num = 1
    while True:
        page = page_spider(url)
        page_dicts = page.get()
        # 爬取内容的xpath规则
        xpath_lists = {
            'root': '//div[@id="content"]/article',
            'title_id':'./@id',
            'title':'./header/h1/a/text()',
            'title_link':'./header/h1/a/@href',
            'picture_link':'./div[@class="entry-content"]/p//img/@src',
            'src_link':'./div[@class="entry-content"]/p[@class="tricksButtons"]/a[@class="download"]/@href',
        }
        # 当响应网页为200时才进行分析
        if page_dicts['status_code'] == 200:
            # 分析网页源码
            spider = analyse_spider(page_dicts['text'],xpath_lists)
            # 获取所需内容list格式
            content_lists = spider.get_content_lists()
            for content_list in content_lists:

                # 保存图片和源码到硬盘
                id = content_list["title_id"]
                # 下载文件和源码
                picfile = page_spider(content_list['picture_link']).bin_file()
                srcfile = page_spider(content_list['src_link']).bin_file()
                # 保存文件和源码
                analyse_file.save_file(picfile,content_list['picture_link'],id)
                analyse_file.save_file(srcfile,content_list['src_link'],id)
                # 结束

                # 保存数据到数据库
                analyse_file.save_to_mysql(content_list)
            break
        else:
            print u"状态码异常,重新请求第(" + str(num) +")次"
            time.sleep(random.randint(5))
            if num > 5:
                break


def main():
    analyse_file.initconfig()
    start = int(raw_input(u"请输如页码范围："))
    end = int(raw_input(u"请输入结束范围："))
    for page in range(start,end+1):
        print u"第" + str(page) + u"页开始"
        try:
            url = 'https://www.html5tricks.com/page/' + str(page)
            mainSpider(url)
        except:
            print u"第" + str(page) + u"页异常"
        print u"第" + str(page) + u"页结束"
        print ""


if __name__ == "__main__":
    main()


