# coding=utf-8
import argparse
import os

from parser import parser
from rules import rules
import engine


def parser_maker():
    parser = argparse.ArgumentParser(description='Extract C file from elearning homework pack.')
    parser.add_argument('--src', dest='src', default='/Users/SpaceQ/Desktop/hw13c/0000.c', type=str,
                        help='input file path')
    parser.add_argument('--output_type', dest='output_type', default='all', type=str,
                        help='output type can be all, short, score')
    args = parser.parse_args()
    return args


def printer(glb_fct, facts, type):
    comments = {}
    err_counter = 0
    for line_num, this_line in enumerate(facts):
        if line_num == 0:
            continue
        else:
            previous_line = facts[line_num - 1]

        next_indent = int(previous_line["next indent should"]) if "next indent should" in previous_line else 0
        indent_type = glb_fct["indentation"]
        indent_fact = this_line['this line %s' % indent_type] - previous_line['this line %s' % indent_type]
        indent_should = int(this_line['indent should']) + next_indent
        if indent_fact != indent_should:
            indent_num = indent_should - indent_fact
            if indent_type in "space":
                indent_num *= 4
                indent_type = "空格"
            if indent_num > 0:
                print "[第%d行]少了%d个%s" % (line_num + 1, indent_num, indent_type)
            else:
                print "[第%d行]多了%d个%s" % (line_num + 1, -indent_num, indent_type)
            comments["检查缩进是否正确"] = True
            err_counter += 1
        if "this line indent wrong" in this_line and this_line["this line indent wrong"]:
            if type in "all":
                print "[第%d行]请不要混用缩进" % (line_num + 1)
            comments["检查Tab和空格有无混用现象"] = True
            err_counter += 1
        if "{ should follow in a line" in this_line:
            if type in "all":
                print "[第%d行]请保持大括号在行尾的习惯" % (line_num + 1)
            comments["固定左大括号位置"] = True
            err_counter += 1
        if "{ should in a new line" in this_line:
            if type in "all":
                print "[第%d行]请保持大括号在另起一行行首的习惯" % (line_num + 1)
            comments["固定左大括号位置"] = True
            err_counter += 1
        if "{ should take an entire line" in this_line:
            if type in "all":
                print "[第%d行]请保证行首大括号后不跟任何内容" % (line_num + 1)
            comments["注意行首大括号后不要跟任何内容"] = True
            err_counter += 1
        if "} should take an entire line" in this_line:
            if type in "all":
                print "[第%d行]请保证行尾大括号单独占一行" % (line_num + 1)
            comments["注意行尾大括号单独占一行"] = True
            err_counter += 1

    if (type in "score") or (type in "all") or (type in "short"):
        print "您的风格分为%d分(满分100分)" % (100 - int(err_counter * 100 / len(facts)))
    print "下面是给出的建议"
    if (type in "all") or (type in "short"):
        cnt = 0
        for comment, value in comments.iteritems():
            if value:
                cnt += 1
                print ("%d. 请" % cnt) + comment


if __name__ == '__main__':
    args = parser_maker()
    glb_fct, line_fct = parser(args.src)
    facts = engine.solver(glb_fct, line_fct, rules)
    printer(glb_fct, facts, args.output_type)
    # print comments
