
import sys
import importlib
importlib.reload(sys)
import os

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def parse(pdf_path,txt_path):
    fp = open(pdf_path, 'rb')  # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            num_page += 1  # 页面增一
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                if isinstance(x,LTImage):  # 图片对象
                    num_image += 1
                if isinstance(x,LTCurve):  # 曲线对象
                    num_curve += 1
                if isinstance(x,LTFigure):  # figure对象
                    num_figure += 1
                if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容
                    num_TextBoxHorizontal += 1  # 水平文本框对象增一
                    # 保存文本内容
                    with open(txt_path, 'a',encoding='utf-8') as f:
                        results = x.get_text()
                        f.write(results + '\n')



#
xml_files = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\file"):
   xml_files.append(files)

txt_files = []
for s in range(len(xml_files[0])):
    txt_str = "C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\file_txt\\" + xml_files[0][s][0:-4]+'.txt'
    xml_files[0][s] = "C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\file\\"+ xml_files[0][s]

    txt_files.append(txt_str)

xml_files = xml_files[0]
for i in range(len(xml_files)):
    parse(xml_files[i],txt_files[i])
    print("成功完成文件" + xml_files[i])
# parse(r"C:\Users\hjn\Documents\Tencent Files\2420080447\FileRecv\信息管理学院注册志愿者志愿服务时长统计表时长版（截止至2018年7月7日）.pdf",r"C:\Users\hjn\Documents\Tencent Files\2420080447\FileRecv\信息浏览行为是理论导向抑或生物驱动_基于眼动仪实验的实证分析_王琳.txt")