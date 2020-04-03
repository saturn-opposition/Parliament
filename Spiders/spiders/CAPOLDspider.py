from util import myredis, request, request_decoreator, log, create_directory
import pandas as pd
from lxml import etree


class CAPOLDspider(object):

    def __init__(self):
        self.start_url = 'https://openparliament.ca/politicians/former/'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        self.data_path = 'E:/DATA/meeting/CAPOLD'

    def get_member_list(self):
        r = request(self.start_url, header=self.header)
        tree = etree.HTML(r.text)
        members = tree.xpath('//*[@class="column column-block"]/a/@href')
        for member in members:
            member_name = member.split('/')[-2]
            create_directory(f'{self.data_path}/{member_name}')
            myredis.sadd('CAPOLD', f'https://openparliament.ca/politicians/{member_name}')
            print(member_name)

    def get_basic_info(self, tree, url):
        data_dict = {'href': url}
        data_dict['name'] = tree.xpath('//*[@class="pol_name"]/text()')[0]
        data_dict['terms'] = tree.xpath('//*[@class="main-col"]/h2/text()')[0] if tree.xpath(
            '//*[@class="main-col"]/h2/text()') else None
        data_dict['party'] = tree.xpath('//*[@class="main-col"]/h2/span[1]/span/text()')[0] if tree.xpath(
            '//*[@class="main-col"]/h2/span[1]/span/text()') else None
        data_dict['address'] = tree.xpath('//*[@class="main-col"]/h2/span[2]/text()')[0] if tree.xpath(
            '//*[@class="main-col"]/h2/span[2]/text()') else None
        data_dict['election'] = ''.join(tree.xpath('//*[@class="main-col"]/p[1]//text()'))
        data_dict['keypoint'] = tree.xpath('//*[@class="bulleted"][last()]/li/strong/text()')[0] if tree.xpath(
            '//*[@class="bulleted"][last()]/li/strong/text()') else None
        return [data_dict]

    def get_speech_info(self, tree, url):
        @request_decoreator
        def do_get_speech(page):
            _url = f'{url}?page={page}'
            r = request(_url, header=self.header)
            newtree = etree.HTML(r.text)
            data_list = self.parse_speech_info(newtree)
            return data_list

        max_page = tree.xpath('//*[@class="long-paginator pagination text-center"]/li[last()-1]/a/text()')[0] if tree.xpath('//*[@class="long-paginator pagination text-center"]/li[last()-1]/a/text()') else None
        if max_page:
            data_list = self.parse_speech_info(tree)
            for i in range(2, int(max_page) + 1):
                data_list.extend(do_get_speech(i))
            return data_list


    def parse_speech_info(self, tree):
        data_list = []
        speeches = tree.xpath('//*[@class="row statement_browser statement"]/div[1]')
        for speech in speeches:
            data_dict = {}
            data_dict['url'] = speech.xpath('p/a/@href')[0]
            data_dict['topic'] = speech.xpath('p/a/text()')[0] if speech.xpath('p/a/text()') else None
            data_dict['date'] = speech.xpath('p/span/text()')[0]
            data_dict['content'] = ''.join(speech.xpath('div/p/text()'))
            data_list.append(data_dict)
        return data_list

    @request_decoreator
    def get_info(self, url):
        name = url.split('/')[-1]
        r = request(url, header=self.header)
        tree = etree.HTML(r.text)
        basic_data = self.get_basic_info(tree, url)
        peech_info = self.get_speech_info(tree, url)
        basic_df = pd.DataFrame(basic_data)
        peech_df = pd.DataFrame(peech_info)
        basic_df.to_csv(f'{self.data_path}/{name}/1-基本信息.csv', index=False, encoding='utf_8_sig')
        peech_df.to_csv(f'{self.data_path}/{name}/2-发言信息.csv', index=False, encoding='utf_8_sig')

    def run(self):
        while True:
            url = myredis.spop('CAPOLD')
            if url:
                member = url.decode('utf-8')
                if not myredis.sismember('CAPOLD_s', member):
                    try:
                        self.get_info(member)
                        myredis.sadd('CAPOLD_s', member)
                    except:
                        myredis.sadd('CAPOLD', member)
            else:
                break


if __name__ == '__main__':
    spdier = CAPOLDspider()
    # spdier.get_info('https://openparliament.ca/politicians/diane-ablonczy/')
    spdier.get_member_list()
    spdier.run()

    # print(myredis.smembers('CAPOLD_s'))