#-*- coding: utf-8 -*-

import urllib2
import util.dlpdf as dlpdf
import util.analyzepdf as analyzepdf

import os
import sys
import re

#---------------------------------------------------------------------------------------
# 根据CJJ提供的txt/sm.txt文件去谷歌学术进行搜索并下载对应的PDF文件到outdir-->即pdf文件夹中
#---------------------------------------------------------------------------------------
def dlpdf_main():
    srcfile = "txt/sm.txt"
    if len(sys.argv) >= 2:
        srcfile = sys.argv[1]
    outdir = "pdf"

    all_titles = dlpdf.get_all_titles(srcfile)
    for title in all_titles:
        encoded_title = urllib2.quote(title)

        google_search_result_file = "google/google_search_result_file.html"
        proxy_ip_port = "127.0.0.1:39721"
        if len(sys.argv) >=3:
            proxy_ip_port = sys.argv[2]

        dlpdf.search_by_title(encoded_title, google_search_result_file, proxy_ip_port)
        download_url = dlpdf.get_download_href(google_search_result_file)

        if download_url:
            print "begin to download %s" % (download_url,)
            dlpdf.download(download_url, ("%s/%s.pdf" % (outdir, encoded_title,)).replace("%20", "_"))

#---------------------------------------------------------------------------------------
# analyzepdf_main会将pdf文件夹中的所有pdf文件进行分析，最后分析结果放到summary/summary.txt中
#---------------------------------------------------------------------------------------
def analyzepdf_main():

    srcdir = "pdf"
    outdir = "summary"

    result = []
    result2 = []
    pdf_pattern = re.compile("\.pdf$")
    for root_dir, dirs, files in os.walk(os.path.realpath("./%s/" % (srcdir))):
        for file in files:
            abs_file = os.path.realpath(os.path.join(root_dir, file))
            if pdf_pattern.findall(abs_file):
                abs_pdf = abs_file
                abs_txt = abs_file.replace(".pdf", ".txt")
                analyzepdf.getpdftotext(abs_pdf, abs_txt)
                analyze_result = analyzepdf.analyze(abs_pdf, abs_txt, 70)
                result.append(analyze_result)

    def sort_dict(adict):
        items = adict.items()
        items.sort()
        return [value for key, value in items]

    for item in result:
        for value in sort_dict(item):
            # print value
            result2.append(value)

    summary = open(os.path.realpath("./%s/summary.txt" % (outdir)),"w");
    try:
        summary.write("\n".join(result2))
    except:
        pass
    finally:
        summary.close()


if __name__ == "__main__":
    # dlpdf_main()
    analyzepdf_main()


#请确保已经创建了pdf文件夹，download文件夹，txt文件夹，summary文件夹