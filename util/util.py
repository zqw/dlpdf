# coding=utf-8
import os
import subprocess


def get_titles(in_file):

    in_file = "%s/%s" % (os.getcwd(), in_file)

    command1 = ('cat %s' % (in_file)).split(" ")
    command2 = ('grep ^\\#\\*').split(" ")
    command3 = ('sed s/\#\*//g').split(" ")

    child1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
    child2 = subprocess.Popen(command2, stdin=child1.stdout, stdout=subprocess.PIPE)
    child3 = subprocess.Popen(command3, stdin=child2.stdout, stdout=subprocess.PIPE)

    titles, error = child3.communicate()

    # trim 最后行的换行符
    while titles[-1]=="\n":
        titles = titles[:-1]

    return titles.split("\n")


def download(titles):
    print "hello download titles"
    pass


