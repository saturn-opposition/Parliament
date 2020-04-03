from util import myredis, request, request_decoreator, log, create_directory
import pandas as pd
from lxml import etree




class EuPersonSpider(object):

    def __init__(self):
        self.start_url = 'https://europarl.europa.eu/meps/en/full-list/all'
        self.data_path='E:/DATA/meeting/EuPerson'
        create_directory(self.data_path)
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    def make_csv(self,pid,name,data):
        if data!='' and data!=[] and data is not None:
            data=[data]
            df=pd.DataFrame(data)
            df.to_csv(f'{self.data_path}/{pid}/{name}.csv',index=False,encoding='utf_8_sig')

    def crawl_person(self):
        r=request(self.start_url,header=self.header,timeout=50)
        tree=etree.HTML(r.text)
        persons=tree.xpath('//*[@class="ep_item europarl-expandable-item single-member-container"]/div/a/@href')
        for p_url in persons:
            myredis.sadd('EUP',f'https://europarl.europa.eu{p_url}')
            log.info(f'crawled person url{p_url}')

    def crawl_info(self):
        while True:
            _url=myredis.spop('EUP')
            if _url:
                url=_url.decode('utf-8')
                try:
                    if myredis.sismember('EUP_s',url) == False:
                        print(myredis.sismember('EUP_s',url))
                        print(url)
                        info_dict={}
                        p_id=url.split('/')[-1]
                        create_directory(f'{self.data_path}/{p_id}')
                        r=request(url,timeout=15)
                        tree=etree.HTML(r.text)
                        info_dict['1-基本信息']=self.get_main_info(tree)
                        info_dict['2-HOME']=self.get_home_info(tree)
                        info_dict['3-DEBATES']=self.get_debates_info(url)
                        self.get_files(url)
                        info_dict['5-Curriculum_vitae']=self.get_vitae(url)
                        info_dict['7-ASSISTANTS']=self.get_assistants(url)
                        info_dict['8-Meetings']=self.get_meetings(url)
                        for k,v in info_dict.items():
                            self.make_csv(p_id,k,v)
                        myredis.sadd('EUP_s',url)
                except Exception as e:
                    print(e)
                    myredis.sadd('EUP',url)

    def get_main_info(self,tree):
        person_dict={}  # 基本信息字典
        person_dict['name']=tree.xpath('//*[@class="ep_name erpl-member-card-full-member-name"]/text()')[0]
        person_dict['party']=tree.xpath('//*[@id="erpl-political-group-name"]/span[1]/text()')[0]
        person_dict['status']=tree.xpath('//*[@class="erpl-member-card-role"]/text()')[0]
        person_dict['country']=tree.xpath('//*[@id="erpl-member-country-name"]/text()')[0]
        return person_dict

    def get_home_info(self,tree):
        '''
            遍历元素序列中的每个元素，若此元素为key，则挨个遍历其后的元素，判断是否为value，直到不是，把k赋值给i，进行下一轮key判定
        '''
        home_dict = {}  # home信息
        element_list=tree.xpath('//*[@class="ep_gridrow-content erpl-meps-home-card"]/div')
        i=0
        while i <len(element_list)-1:
            key=element_list[i].xpath('div/h3/div/div/span[1]/text()')
            if key:
                home_dict[key[0]]=[]
                for k in range(i+1,len(element_list)):
                    value=element_list[k].xpath('div/div/div/div[2]/span[1]/text()')
                    if value:
                        home_dict[key[0]].append(value[0])
                    else:
                        i=k
                        break
                    if k==len(element_list)-1:
                        i=k
                        break
            i+=1
        return home_dict

    @request_decoreator
    def get_debates_info(self,_url):

        @request_decoreator
        def get_speech_info(meet_url):
            r=request(meet_url,timeout=15)
            tree=etree.HTML(r.text)
            text=''.join(i.strip() for i in tree.xpath('//*[@class="contents"]//text()'))
            return text

        debates_list=[]         # 发言集
        url=f'{_url}/GHEORGHE_FALCA/main-activities/plenary-speeches#mep-card-content'
        r=request(url,timeout=15)
        tree=etree.HTML(r.text)
        meets=tree.xpath('//*[@class="ep_gridcolumn ep-m_product erpl-activity-item"]/div/div')
        for meet in meets:
            debates_dict={}     # 发言字典
            debates_dict['meet_name']=meet.xpath('a/div/div/span[1]/text()')[0].strip()
            meet_url=meet.xpath('a/@href')[0]
            debates_dict['meet_date']=meet.xpath('div/div/span/time/@datetime')[0]
            debates_dict['speech']=get_speech_info(meet_url)
            debates_list.append(debates_dict)
        return debates_list

    @request_decoreator
    def get_files(self,_url):
        pid=_url.split('/')[-1]
        create_directory(f'{self.data_path}/{pid}/4-Motions_for_resolutions')

        @request_decoreator
        def download_file(file_url):
            filename=file_url.split('/')[-1]
            r=request(file_url,timeout=20)
            with open(f'{self.data_path}/{pid}/4-Motions_for_resolutions/{filename}','wb')as f:
                f.write(r.content)

        url=f'{_url}/MAGDALENA_ADAMOWICZ/main-activities/motions-instit'
        r=request(url,timeout=15)
        tree=etree.HTML(r.text)
        file_list=tree.xpath('//*[@title="Download the document"]/@href')
        if file_list:
            for file in file_list:
                download_file(file)

    @request_decoreator
    def get_vitae(self,_url):
        t_list=[]
        url=f'{_url}/NUNO_MELO/cv#mep-card-content'
        r=request(url,timeout=15)
        tree=etree.HTML(r.text)
        vitaes=tree.xpath('//article[@class="ep_gridcolumn ep-m_product"]/div/div/div/ul/li')
        for v in vitaes:
            if len(v):
                t_dict={}
                year=v.xpath('strong/text()')[0]
                text=v.xpath('text()')[0]
                t_dict[year]=text
                t_list.append(t_dict)
        return t_list

    @request_decoreator
    def get_declaration(self,_url):
        @request_decoreator
        def do_download(pdf_url):
            filename=pdf_url.split('/')[-1]
            r=request(pdf_url,timeout=15)
            with open(f'{self.data_path}/{pid}/6-Declarations/{filename}','wb')as f:
                f.write(r.content)

        pid=_url.split('/')[-1]
        create_directory(f'{self.data_path}/{pid}/6-Declarations')
        url=f'{_url}/NUNO_MELO/declarations#mep-card-content'
        r=request(url,timeout=15)
        tree=etree.HTML(r.text)
        pdfs=tree.xpath('//*[@title="Read the document"]/@href')
        for pdf in pdfs:
            do_download(pdf)

    @request_decoreator
    def get_assistants(self,_url):
        assistants_dict={}
        url=f'{_url}/SILVIA_SARDONE/assistants#mep-card-content'
        r=request(url,timeout=15)
        tree=etree.HTML(r.text)
        p_list=tree.xpath('//*[@class="ep_gridrow ep-o_productlist erpl-meps-asst-group-list"]')
        for p in p_list:
            type_str=p.xpath('div/div/div/h3/div/div/span[1]/text()')[0]
            names=p.xpath('div/article/div/div/div/ul/li/div/span[1]/text()')
            assistants_dict[type_str]=[n.strip() for n in names]
        return assistants_dict

    @request_decoreator
    def get_meetings(self,_url):
        meet_list=[]
        url=f'{_url}/MARTIN_HOJSIK/meetings/past#mep-card-content'
        r=request(url,timeout=15)
        tree=etree.HTML(r.text)
        meets=tree.xpath('//*[@class="ep_gridcolumn ep-m_product europarl-expandable-item"]')
        for meet in meets:
            meet_dict={}
            meet_dict['name']=meet.xpath('div/div[1]/div[1]/div/span[1]/text()')[0]
            meet_dict['date']=meet.xpath('div/div[1]/div[2]/div/span[1]/time/text()')[0]
            meet_dict['location']=meet.xpath('div/div[1]/div[2]/div/span[1]/text()')[0].strip()
            meet_dict['status']=meet.xpath('div/div[2]/div/div/span/text()')[0]
            meet_dict['institutions']=meet.xpath('div/div[3]/div/div/span/text()')[0].strip()
            meet_list.append(meet_dict)
        return meet_list






if __name__ == '__main__':

    spider=EuPersonSpider()
    spider.crawl_person()
    spider.crawl_info()


