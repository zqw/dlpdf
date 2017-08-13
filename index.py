#-*- coding: utf-8 -*-

import urllib2
import util.dlpdf as dlpdf
import util.analyzepdf as analyzepdf

import os
import sys


def dlpdf_main():

    srcfile = "txt/sm.txt"
    if len(sys.argv) >= 2:
        srcfile = sys.argv[1]

    all_titles = dlpdf.get_all_titles(srcfile)
    for title in all_titles:
        encoded_title = urllib2.quote(title)

        tmp_file = "download/tmp.html"

        proxy_ip_port = "127.0.0.1:39721"
        if len(sys.argv) >=3:
            proxy_ip_port = sys.argv[2]

        dlpdf.search_by_title(encoded_title, tmp_file, proxy_ip_port)
        download_url = dlpdf.get_download_href(tmp_file)

        if download_url:
            print "begin to download %s" % (download_url,)
            dlpdf.download(download_url, ("download/%s.pdf" % (encoded_title,)).replace("%20", "_"))


def analyzepdf_main():
    pdfpath = os.path.join(os.getcwd(), "pdf/sm.pdf")
    txtpath = os.path.join(os.getcwd(), "pdf/sm.txt")

    analyzepdf.getpdftotext(pdfpath, txtpath)
    analyze_result = analyzepdf.analyze(pdfpath, txtpath, 100)

    for i in analyze_result.keys():
        print analyze_result[i]



if __name__ == "__main__":
    analyzepdf_main()