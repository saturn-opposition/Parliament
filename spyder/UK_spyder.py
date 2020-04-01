
from util import request, myredis, request_decoreator, log, create_directory
from lxml import etree

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}


class UKspider(object):

    def __init__(self):
        self.start_urls = ['https://www.theyworkforyou.com/pwdata/scrapedxml/debates',
                           'https://www.theyworkforyou.com/pwdata/scrapedxml/lordspages']
        self.data_path='E:/DATA/meeting/UK'
        create_directory(f'{self.data_path}/debates')
        create_directory(f'{self.data_path}/lordspages')

    def get_url_2_redis(self, url):
        r = request(url, header=header)
        tree = etree.HTML(r.text)
        url_list = tree.xpath('//table/tr/td[2]/a/@href')
        for url_ in url_list:
            if '2019' in url_:
                myredis.sadd(f'UK_{url.split("/")[-1]}',f'https://www.theyworkforyou.com/pwdata/scrapedxml/lordspages/{url_}')

    def crawl_data(self):
        for redis_key in['UK_debates','UK_lordspages']:
            while True:
                url_=myredis.spop(redis_key)
                if url_:
                    url=url_.decode('utf-8')
                    print(f'start crawling {url}')
                    try:
                        filename=url.split('/')[-1]
                        r=request(url,header=header,timeout=20)
                        with open(f'{self.data_path}/{redis_key.split("_")[-1]}/{filename}','w',encoding='utf-8')as f:
                            f.write(r.text)
                    except Exception as e:
                        myredis.sadd(redis_key,url)
                        print(e)
                else:
                    break

    def run(self):
        for url in self.start_urls:
            self.get_url_2_redis(url)
        self.crawl_data()

if __name__ == '__main__':
    spider = UKspider()
    spider.run()
