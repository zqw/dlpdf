#-*- coding: utf-8 -*-

import urllib2
import util.dlpdf as dlpdf
import util.analyzepdf as analyzepdf

import os
import sys
import re


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

    result = []
    result2 = []
    pdf_pattern = re.compile("\.pdf$")
    for root_dir, dirs, files in os.walk(os.path.realpath("./pdf/")):
        for file in files:
            abs_file = os.path.realpath(os.path.join(root_dir, file))
            if pdf_pattern.findall(abs_file):
                abs_pdf = abs_file
                abs_txt = abs_file.replace(".pdf", ".txt")
                analyzepdf.getpdftotext(abs_pdf, abs_txt)
                analyze_result = analyzepdf.analyze(abs_pdf, abs_txt, 70)
                result.append(analyze_result)
    for item in result:
        for key,value in item.items():
            # print value
            result2.append(value)

    summary = open(os.path.realpath("./summary/summary.txt"),"w");
    try:
        summary.write("\n".join(result2))
    except:
        pass
    finally:
        summary.close()


if __name__ == "__main__":
    analyzepdf_main()


#请确保已经创建了pdf文件夹，download文件夹，txt文件夹，summary文件夹