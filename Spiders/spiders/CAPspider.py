from util import myredis, request, request_decoreator, log, create_directory
import pandas as pd
from lxml import etree


class CAPSpider(object):

    def __init__(self):
        self.start_url='https://openparliament.ca/politicians/'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        self.data_path='E:/DATA/meeting/CAP'

    def get_member_list(self):
        r=request(self.start_url,header=self.header)
        tree=etree.HTML(r.text)
        members=tree.xpath('//*[@class="column column-block"]/a/@href')
        for member in members:
            member_name=member.split('/')[-2]
            create_directory(f'{self.data_path}/{member_name}')
            myredis.sadd('CAP',f'https://openparliament.ca{member}')
            print(member_name)

    @request_decoreator
    def get_basic_info(self,url):
        data_dict={'href':url}
        r=request(url,header=self.header)
        tree=etree.HTML(r.text)
        data_dict['name']=tree.xpath('//*[@class="pol_name"]/text()')[0]
        data_dict['party']=tree.xpath('//*[@itemprop="affiliation"]/span/text()')[0] if tree.xpath('//*[@itemprop="affiliation"]/span/text()') else None
        data_dict['address']=tree.xpath('//*[@itemprop="jobTitle"]/text()')[0] if tree.xpath('//*[@itemprop="jobTitle"]/text()') else None
        data_dict['election']=''.join(tree.xpath('//*[@class="main-col"]/p[1]//text()'))
        data_dict['keypoint']=tree.xpath('//*[@class="bulleted"][last()]/li/strong/text()')[0] if tree.xpath('//*[@class="bulleted"][last()]/li/strong/text()') else None
        return data_dict

    @request_decoreator
    def get_speech_by_page(self,member_name,page):
        data_list=[]
        url=f'https://openparliament.ca/search/?q=MP%3A+%22{member_name}%22+Type%3A+%22debate%22&sort=date+desc&page={page}'
        r=request(url,header=self.header,timeout=15)
        tree=etree.HTML(r.text)
        speeches=tree.xpath('//*[@class="row result"]')
        for speech in speeches:
            data_dict = {}
            data_dict['topic']=speech.xpath('div[1]/p/a/text()')[0]
            data_dict['content']=speech.xpath('div[1]/p/text()')[0].strip()
            data_dict['date']=speech.xpath('div[2]/p/text()')[0]
            data_dict['type']=speech.xpath('div[2]/p/text()')[1]
            data_list.append(data_dict)
        return data_list


    def get_speech_info(self,member_name):
        data_list=[]
        url=f'https://openparliament.ca/search/?q=MP%3A+%22{member_name}%22+Type%3A+%22debate%22&sort=date+desc'
        r=request(url,header=self.header,timeout=15)
        tree=etree.HTML(r.text)
        max_page=tree.xpath('//*[@class="long-paginator pagination text-center"]/li[last()-1]/a/text()')[0] if tree.xpath('//*[@class="long-paginator pagination text-center"]/li[last()-1]/a/text()') else None
        speeches=tree.xpath('//*[@class="row result"]')
        if max_page:
            for speech in speeches:
                data_dict = {}
                data_dict['topic']=speech.xpath('div[1]/p/a/text()')[0]
                data_dict['content']=speech.xpath('div[1]/p/text()')[0].strip()
                data_dict['date']=speech.xpath('div[2]/p/text()')[0]
                data_dict['type']=speech.xpath('div[2]/p/text()')[1]
                data_list.append(data_dict)
            for page in range(2,int(max_page)+1):
                p_data_list=self.get_speech_by_page(member_name,page)
                data_list.extend(p_data_list)
            return data_list


    def download(self):
        while True:
            url=myredis.spop('CAP')
            if url:
                member=url.decode('utf-8')
                member_name=member.split('/')[-2]
                if not myredis.sismember('CAP_s',member):
                    try:
                        basic_data=self.get_basic_info(member)
                        speech_data=self.get_speech_info(member_name)
                        basic_df=pd.DataFrame([basic_data])
                        speech_df=pd.DataFrame(speech_data)
                        basic_df.to_csv(f'{self.data_path}/{member_name}/1-基本信息.csv',index=False,encoding='utf_8_sig')
                        speech_df.to_csv(f'{self.data_path}/{member_name}/2-会议发言.csv',index=False,encoding='utf_8_sig')
                        myredis.sadd('CAP_s',member)
                        log.info(f'donwload {member_name} 基本信息  successful')
                    except Exception as e:
                        log.warning(e)
                        myredis.sadd('CAP',member)
            else:
                break


if __name__ == '__main__':
    spider=CAPSpider()
    spider.get_member_list()
    spider.download()
    # r=request('https://openparliament.ca/politicians/ziad-aboultaif/')
    # tree=etree.HTML(r.text)
    # spider.get_basic_info(tree)
    # data=spider.get_speech_info('jagmeet-singh')
    # df=pd.DataFrame(data)
    # df.to_csv('a.csv')

