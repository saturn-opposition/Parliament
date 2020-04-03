from util import myredis,request,request_decoreator,log,create_directory
from requests import session
from lxml import etree
from threading import Thread


class DeuSpider(object):
    def __init__(self):
        self.data_path='E:/DATA/meeting/DEU'
        create_directory(self.data_path)
        self.search_key='a'
        self.header= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        self.s=session()
        self.s.get('http://pdok.bundestag.de/index.php',headers=self.header)

    def search(self):
        search_url=f'https://pdok.bundestag.de/index.php?qsafe=a&aload=off&q={self.search_key}'
        self.s.get(search_url)
        r=self.s.get('https://pdok.bundestag.de/treffer.php?q=a&wp=&dart=&gtyp=&typ=&gkuname=&kurheber=&gpuname=&purheber=',timeout=(30,30))
        tree=etree.HTML(r.text)
        max_page=tree.xpath('//*[@id="trefferAnzahl"]/strong/text()')[0]
        # 改变每页元素个数为100
        self.s.post('https://pdok.bundestag.de/pushData.php',data={'sdata':'maxln:100'})

        max_pagei = int(int(max_page) / 100)
        for page in range(0,max_pagei):
            self.search_by_page(page)

    @request_decoreator
    def search_by_page(self,page):
        url=f'https://pdok.bundestag.de/treffer.php?h={page*100}&q=a'
        print(url)
        r=self.s.get(url)
        tree=etree.HTML(r.text)
        elements=tree.xpath('//*[@class="suchErgebnis"]/table/tbody/tr/td')
        for element in elements:
            pdf_url=element.xpath('div[1]/div[1]/a/@href')[0]
            nr=element.xpath('div[2]/strong[1]/text()')[0]
            date=element.xpath('div[2]/strong[2]/text()')[0]
            filename=f'DEU-{nr.replace("/","-")}-{date}.pdf'
            myredis.sadd('DEU',f'{filename}<--->{pdf_url}')
        log.info(myredis.scard('DEU'))

    @request_decoreator
    def download(self):
        while True:
            f_info=myredis.spop('DEU')
            if f_info:
                f_info=f_info.decode('utf-8')
                if not myredis.sismember('DEU_s',f_info):      # 判断是否已经抓取过
                    try:
                        log.info(f'start downloading {f_info}')
                        filename,url=f_info.split('<--->')
                        r=request(url,header=self.header,timeout=(10,10))
                        with open(f'{self.data_path}/{filename}','wb')as f:
                            f.write(r.content)
                        myredis.sadd('DEU_s',f_info)
                    except Exception as e:
                        log.warning(e)
                        myredis.sadd('DEU',f_info)
            else:
                break

    def mutix_download(self):
        tasks=[Thread(target=self.download) for _ in range(50)]
        for t in tasks:
            t.start()
        for t in tasks:
            t.join()

if __name__ == '__main__':
    spider=DeuSpider()
    spider.search()
    spider.mutix_download()

    # r = request('http://dipbt.bundestag.de/doc/btd/06/014/0601441.pdf', header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
    # with open('E:/DATA/meeting/DEU/DEU-06-1441-12.11.1970.pdf', 'wb')as f:
    #     f.write(r.content)