# coding=utf-8

import util.util as util


def main():
    titles = util.get_titles("txt/big.txt")
    util.download(titles)
    print titles


if( __name__ == "__main__"):
    main()