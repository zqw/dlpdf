#-*- coding: utf-8 -*-

import urllib2
import sys
import os
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import *
import re


reload(sys)
sys.setdefaultencoding('utf8')


def getpdftotext(pdfpath, txtpath):
    pdf = open(pdfpath, "rb")
    txt = open(txtpath, "w")

    parser = PDFParser(pdf)
    document = PDFDocument(parser)

    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # 创建一个PDF资源管理器对象来存储共享资源
    # caching = False不缓存
    rsrcmgr = PDFResourceManager(caching=False)
    # 创建一个PDF设备对象
    laparams = LAParams()
    # 创建一个PDF页面聚合对象
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解析器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # 处理文档当中的每个页面

    # doc.get_pages() 获取page列表
    # for i, page in enumerate(document.get_pages()):
    # PDFPage.create_pages(document) 获取page列表的另一种方式
    # replace = re.compile(r'\s+');
    # 循环遍历列表，每次处理一个page的内容
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
        # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
        for x in layout:
            # 如果x是水平文本对象的话
            if (isinstance(x, LTTextBoxHorizontal)):
                # text = re.sub(replace, '', x.get_text())
                text= x.get_text()
                if len(text) != 0:
                    txt.write(text)
    if pdf:
        pdf.close()
    if txt:
        txt.close()


def analyze(pdfpath, txtpath, loop):
    pdffilename = os.path.basename(pdfpath)
    txt = open(txtpath)

    lines = txt.readlines()
    lines = "".join(lines)
    pos1 = lines.find('REFERENCES')
    pos2 = lines.find('References')
    pos3 = lines.find('ACKNOWLEDGEMENT')
    pos4 = lines.find('ACKNOWLEDGEMENTS')

    pos = pos1
    if pos2 > 0:
        pos = pos2
    if pos3 > 0:
        pos = pos3
    if pos4 > 0:
        pos = pos4

    lines1 = lines[:pos]
    lines2 = lines[pos:]


    #####################################################
    lines1 = "".join(lines1).replace("\n","").split(".")
    start1 = 1
    result1={}
    while start1 < loop:
        pattern1 = re.compile("\["+str(start1)+"|,"+str(start1)+",|"+str(start1)+"\]")
        def has_ref_content(line):
            return len(pattern1.findall(line)) > 0

        content = filter(has_ref_content, lines1)

        if content and len(content) > 0:
            # print "[" + str(start1) + "]" + content[0] + "."
            result1[start1] = content[0] + "."
            start1 = start1 + 1
        else:
            result1[start1] = "NaN"
            start1 = start1 + 1
            continue


    # print result1

    ####################################################
    title = "NaN"
    start2 = 1
    result2 = {}
    while start2 < loop:
        left = lines2.find('['+ str(start2)+']')
        right = lines2.find('['+ str(start2+1)+']')
        if left > 0 and right > 0:
            inner_str = lines2[left:right]
            pattern2 = re.compile("(?<=\xe2\x80\x9c)(.*)(?=\xe2\x80\x9d)")
            title = pattern2.findall(inner_str.replace("\n",""))
            if(title):
                # print "["+str(start2)+"]"+str(title[0])
                result2[start2] = str(title[0])
            else:
                result2[start2] = "NaN"
            start2 = start2 + 1
        else:
            result2[start2] = "NaN"
            start2 = start2 + 1
            continue

    # print result2
    if txt:
        txt.close()

    result3={}
    for i in range(1,loop):
        if(result1[i] == "NaN" and result2[i] == "NaN" ):
            continue
        result3[i] = pdffilename + "-----" +  "["+str(i)+"]" + "-----" +result2[i]  + "-----" +result1[i]
        # print result3[i]
    return result3

    # return "---------".join(["sm.pdf", refindex, title, ref_content])
    # sm.pdf [1] "论文题目" "word wrwowrw "