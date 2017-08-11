# coding=utf-8

import urllib2
import util.util as util


def main():
    all_titles = util.get_all_titles("txt/sm.txt")
    print all_titles
    return
    for title in all_titles:
        encoded_title = urllib2.quote(title)

        tmp_file = "download/tmp.html"
        util.search_by_title(encoded_title, tmp_file)
        download_url = util.get_download_href(tmp_file)

        if download_url:
            print "begin to download %s" % (download_url,)
            util.download(download_url, ("download/%s.pdf" % (encoded_title,)).replace("%20", "_"))


if __name__ == "__main__":
    main()
