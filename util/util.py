# coding=utf-8

import urllib2
from bs4 import BeautifulSoup
import sys
import os
import subprocess

# 重设置编码
reload(sys)
sys.setdefaultencoding('utf8')


def get_all_titles(file):
    abs_file = "%s/%s" % (os.getcwd(), file)

    command1 = ('cat %s' % (abs_file)).split(" ")
    command2 = ('grep ^\\#\\*').split(" ")
    command3 = ('sed s/^\#\*//g').split(" ")
    command4 = ('sed s/\.$//g').split(" ")  #删除结尾的句号

    child1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
    child2 = subprocess.Popen(command2, stdin=child1.stdout, stdout=subprocess.PIPE)
    child3 = subprocess.Popen(command3, stdin=child2.stdout, stdout=subprocess.PIPE)
    child4 = subprocess.Popen(command4, stdin=child3.stdout, stdout=subprocess.PIPE)

    titles, error = child4.communicate()

    # trim 最后行的换行符
    if titles and len(titles) >0:
        while titles[-1] == "\n":
            titles = titles[:-1]

    return titles.split("\n")


def search_by_title(title, ouput_file, proxy_ip_port=None):
    url = "https://scholar.google.com/scholar?q=%s" % (title,)
    user_agent = '--user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)"'
    if not proxy_ip_port:
        proxy = ""
    proxy = '-k -e "https_proxy=https://%s/"' % (proxy_ip_port)

    command1 = r'wget %s %s %s -O %s' % (proxy, user_agent, url, ouput_file)
    child1 = subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)
    child1.communicate()




def get_download_href(destFile):
    command1 = r'cat %s' % (destFile,)
    child1 = subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)
    html, error = child1.communicate()

    if html and len(html) > 0:
        soup = BeautifulSoup(html, "html.parser")
        pdf_a = soup.select("#gs_ccl_results .gs_ggsd a")
        if pdf_a and len(pdf_a) > 0 and pdf_a[0].attrs and pdf_a[0].attrs["href"]:
            pdf_href = pdf_a[0].attrs["href"]
            return pdf_href

    return None

def download(url, ouput_file):
    proxy = '' #下载pdf时不用开代理？？

    command1 = r'wget %s %s -O %s' % (proxy, url, ouput_file)
    child1 = subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)
    child1.communicate()



if __name__ == "__main__":
    pass


