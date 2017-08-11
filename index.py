# coding=utf-8

import urllib2
import util.util as util
import sys


def main():

    srcfile = "txt/sm.txt"
    if len(sys.argv) >= 2:
        srcfile = sys.argv[1]

    all_titles = util.get_all_titles(srcfile)
    for title in all_titles:
        encoded_title = urllib2.quote(title)

        tmp_file = "download/tmp.html"

        proxy_ip_port = "127.0.0.1:39721"
        if len(sys.argv) >=3:
            proxy_ip_port = sys.argv[2]

        util.search_by_title(encoded_title, tmp_file, proxy_ip_port)
        download_url = util.get_download_href(tmp_file)

        if download_url:
            print "begin to download %s" % (download_url,)
            util.download(download_url, ("download/%s.pdf" % (encoded_title,)).replace("%20", "_"))


if __name__ == "__main__":
    main()
