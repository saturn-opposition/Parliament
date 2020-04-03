from util import myredis, request, request_decoreator, log, create_directory
from requests import session
from lxml import etree
from threading import Thread
import json
import os


# class EUspider(object):
#     def __init__(self):
#         self.data_path = 'E:/DATA/meeting/EU'
#         create_directory(self.data_path)
#         self.search_url = 'https://europarl.europa.eu/committees/en/search-in-documents.html'
#         self.header = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
#         self.s = session()
#         self.start_date = "01/01/1996"
#         self.end_date = "25/10/2022"
#         self.committee_dict = {}
#         self.type_dict = {}
#         r = request('https://europarl.europa.eu/committees/en/search-in-documents.html#sidesForm')
#         tree = etree.HTML(r.text)
#         self.get_committee_dict(tree)
#         self.get_type_dict(tree)
#         with open(f'{self.data_path}/dict.txt','w')as f:
#             dict_str=json.dumps([self.committee_dict,self.type_dict],ensure_ascii=False)
#             f.write(dict_str)
#
#     def get_committee_dict(self, tree):
#         options = tree.xpath('//*[@name="committee"]/option')[1:]
#         for option in options:
#             title = option.xpath('@title')[0]
#             value = option.xpath('@value')[0]
#             self.committee_dict[title] = value
#
#     def get_type_dict(self, tree):
#         options = tree.xpath('//*[@id="docType"]/option')[1:]
#         for option in options:
#             title = option.xpath('@title')[0]
#             value = option.xpath('@value')[0]
#             self.type_dict[title] = value
#
#     @request_decoreator
#     def search(self, doctype, committee):
#         print(doctype,committee)
#         if not os.path.isdir(f'{self.data_path}/{committee}/{doctype}'):
#             create_directory(f'{self.data_path}/{committee}/{doctype}')
#         search_data = {"source": "",
#                        "clean": "false",
#                        "leg": "9",
#                        "action": "0",
#                        "tabActif": "tabResult",
#                        "committee": committee,
#                        "docType": doctype,
#                        "author": "",
#                        "refPe": "",
#                        "refANum": "",
#                        "refAYear": "",
#                        "miType": "text",
#                        "miText": "",
#                        "sortResults": "",
#                        "documentType": "",
#                        "documentDateStart": self.start_date,
#                        "documentDateEnd": self.end_date,
#                        "meetingDateStart": "",
#                        "meetingDateEnd": "",
#                        "folderComCode": "",
#                        "folderLegId": "",
#                        "folderId": "",
#                        "refProcYear": "",
#                        "refProcNum": "",
#                        "refProcCode": ""}
#         r = self.s.post(self.search_url, headers=self.header, data=search_data, timeout=(10, 10))
#         tree = etree.HTML(r.text)
#         max_page = tree.xpath('//*[@class="paginate"]/li[last()]/a//text()')
#         if max_page:
#             max_page=max_page[-1].strip()
#             max_page = int(max_page)
#             self.parse_page(r,doctype,committee)
#             for i in range(1, max_page):
#                 self.search_by_page(i,doctype,committee)
#
#     @request_decoreator
#     def search_by_page(self, page,doctype,committee):
#         data = {"meetingDateEnd": "",
#                 "documentDateStart": self.start_date,
#                 "documentType": "",
#                 "docType": doctype,
#                 "folderComCode": "",
#                 "refAYear": "",
#                 "refProcYear": "",
#                 "folderId": "",
#                 "documentDateEnd": self.end_date,
#                 "author": "",
#                 "clean": "false",
#                 "tabActif": "tabResult",
#                 "real_form_name": "sidesForm",
#                 "meetingDateStart": "",
#                 "folderLegId": "",
#                 "refPe": "",
#                 "refProcCode": "",
#                 "miType": "text",
#                 "refProcNum": "",
#                 "refANum": "",
#                 "miText": "",
#                 "sortResults": "",
#                 "leg": "9",
#                 "committee": committee,
#                 "source": "",
#                 "action": page}
#         r = self.s.post(self.search_url, data=data, timeout=(10, 10))
#         self.parse_page(r,doctype,committee)
#
#     def parse_page(self, r,doctype,committee):
#         tree = etree.HTML(r.text)
#         results = tree.xpath('//*[@class="notice"]/ul/li[1]/a/@href')
#         for url in results:
#             myredis.sadd('EU', f'{url}<--->{doctype}<--->{committee}')
#             log.info(f'crawled pdf url {url}')
#
#     def download(self):
#         def do_download():
#             while True:
#                 f_info = myredis.spop('EU')
#                 if f_info:
#                     f_info = f_info.decode('utf-8')
#                     if not myredis.sismember('EU_s', f_info):  # 判断是否已经抓取过
#                         try:
#                             log.info(f'start downloading {f_info}')
#                             url,doctype,committee=f_info.split('<--->')
#                             filename = url.split('/')[-1]
#                             r = request(url, header=self.header, timeout=10)
#                             with open(f'{self.data_path}/{committee}/{doctype}/{filename}', 'wb')as f:
#                                 f.write(r.content)
#                             myredis.sadd('EU_s', f_info)
#                         except Exception as e:
#                             log.warning(e)
#                             myredis.sadd('EU', f_info)
#                 else:
#                     break
#         tasks = [Thread(target=do_download) for _ in range(50)]
#         for t in tasks:
#             t.start()
#         for t in tasks:
#             t.join()
#
#     def run(self):
#         for i in self.type_dict.values():
#             for k in self.committee_dict.values():
#                 self.search(i,k)
#         # self.download()

s = session()
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
}
data_path='E:/DATA/meeting/EU'
create_directory(data_path)
def crawl():
    search_url = 'https://europarl.europa.eu/committees/en/search-in-documents.html'
    data = {
        'source': '',
        'clean': 'false',
        'leg': 9,
        'action': 0,
        'tabActif': 'tabResult',
        'committee': '',
        'docType': '',
        'author': '',
        'refPe': '',
        'refANum': '',
        'refAYear': '',
        'miType': 'text',
        'miText': '',
        'sortResults': '',
        'documentType': '',
        'documentDateStart': '01/01/1996',
        'documentDateEnd': '07/11/2021',
        'meetingDateStart': '',
        'meetingDateEnd': '',
        'folderComCode': '',
        'folderLegId': '',
        'folderId': '',
        'refProcYear': '',
        'refProcNum': '',
        'refProcCode': ''
    }
    r=s.post(search_url,headers=header,data=data)
    tree=etree.HTML(r.text)
    get_urls(tree)
    max_page=tree.xpath('//*[@class="paginate"]/li[last()]/a//text()')[-1].strip() if tree.xpath('//*[@class="paginate"]/li[last()]/a//text()') else None
    if max_page:
        max_page=int(max_page)+1
        for i in range(1,max_page):
            crawl_by_page(i)

@request_decoreator
def crawl_by_page(page):
    url='https://europarl.europa.eu/committees/en/search-in-documents.html'
    data = {
        'source': '',
        'clean': 'false',
        'leg': 9,
        'tabActif': 'tabResult',
        'committee': '',
        'docType': '',
        'author': '',
        'refPe': '',
        'refANum': '',
        'refAYear': '',
        'miType': 'text',
        'miText': '',
        'sortResults': '',
        'documentType': '',
        'documentDateStart': '01/01/1996',
        'documentDateEnd': '07/11/2020',
        'meetingDateStart': '',
        'meetingDateEnd': '',
        'folderComCode': '',
        'folderLegId': '',
        'folderId': '',
        'refProcYear': '',
        'refProcNum': '',
        'refProcCode': '',
        'action': page
    }
    r=s.post(url,data=data)
    tree=etree.HTML(r.text)
    get_urls(tree)

def get_urls(tree):
    results = tree.xpath('//*[@class="notice"]/ul/li[1]/a/@href')
    for result in results:
        myredis.sadd('EU',result)

def download():
    while True:
        url=myredis.spop('EU')
        if url:
            url=url.decode('utf-8')
            try:
                filename=url.split('/')[-1]
                r=request(url,header=header)
                with open(f'{data_path}/{filename}','wb')as f:
                    f.write(r.content)
                myredis.sadd('EU_s',url)
            except Exception as e:
                print(e)
                myredis.sadd('EU',url)
        else:
            break

if __name__ == '__main__':
    # spider = EUspider()
    # spider.run()


    crawl()
    download()