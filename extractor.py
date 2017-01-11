# coding=utf-8
import os
import argparse
from subprocess import call


def parser_maker():
    parser = argparse.ArgumentParser(description='Extract C file from elearning homework pack.')
    parser.add_argument('--src', dest='src', default='/Users/SpaceQ/Desktop/hw13', type=str, help='input file path')
    parser.add_argument('--dst', dest='dst', default='/Users/SpaceQ/Desktop/hw13c', type=str, help='output file path')
    args = parser.parse_args()
    return args


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]


if __name__ == "__main__":
    args = parser_maker()
    cnt = 0

    tmp_dir = os.path.join(args.dst, "tmp")

    for stu in os.listdir(args.src):  # stu is like xxx(163xxxxxxxx)
        dir = os.path.join(args.src, stu, '提交作业的附件')
        if stu[0] in '.':
            continue
        call(["rm", "-rf", os.path.join(tmp_dir)])
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        for file in os.listdir(dir):
            extend = file.split(".", 1)[-1]
            full_path = os.path.join(dir, file)
            if extend in "zip":
                call(["unzip", full_path, "-d", tmp_dir])
            elif extend in "rar":
                call(["unrar", "e", full_path, tmp_dir, "u"])
            elif extend in "c":
                call(["mv", full_path, tmp_dir])
            else:
                print "unable to handle %s" % extend
        for file in os.listdir(tmp_dir):
            full_path = os.path.join(tmp_dir, file)
            if file[-1] in "c":
                print full_path
                call(["mv", full_path, os.path.join(args.dst, "%04d.c" % cnt)])
                cnt += 1
