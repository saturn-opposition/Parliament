from util import myredis, request, request_decoreator, log, create_directory
from lxml import etree
import re


class CAspider(object):

    def __init__(self):
        self.start_url='https://www.lipad.ca/full/?tdsourcetag=s_pctim_aiomsg'
        self.data_path = 'E:/DATA/meeting/CA'

    def search_meet(self):
        r=request(self.start_url)
        tree=etree.HTML(r.text)
        self.get_meet_csv_url(tree)

    @request_decoreator
    def get_meet_csv_url(self,tree):
        meet_urls=tree.xpath('//*[@class="cbp_tmtimeline"]/li/div[3]/ul/li/ul/li/ul/li/a/@href')
        for url in meet_urls:
            myredis.sadd('CA',f'https://www.lipad.ca/full/{url}exportcsv')

    def do_download(self,url):
        year,month,day=re.findall('/(\d+)/(\d+)/(\d+)/',url)[0]
        create_directory(f'{self.data_path}/{year}/{month}')
        r=request(url,timeout=15)
        with open(f'{self.data_path}/{year}/{month}/{day}.csv','wb')as f:
            f.write(r.content)


    def download_csv(self):
        while True:
            csv_url=myredis.spop('CA')
            if csv_url:
                url=csv_url.decode('utf-8')
                if not myredis.sismember('CA_s',url):
                    try:
                        self.do_download(url)
                        myredis.sadd('CA_s',url)
                    except:
                        myredis.sadd('CA',url)
            else:
                break




if __name__ == '__main__':
    spider=CAspider()
    spider.search_meet()

    spider.download_csv()