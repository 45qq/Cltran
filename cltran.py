#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import subprocess
import lib.config as cg
from lib.run import run


def tran(text):
    relist = cg.get_relist()

    # relist = [('^ {0,6}\\b(.*):', 1), ('  .*?  \\b(.*)', 1), ('  .*?^[A-Z] \\b(.*)', 1), ('^ {3,30}\\b(.*)', 1),
    #           ('^ ?\\b(.*)', 1)]

    if cg.show_original_text:
        print(text)
    result = run(text, relist)
    print(result)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '-help':
            print("usage: cltran <cmd>\t", end='')
            print("cmd为'-h'或'-hlep'显示帮助信息，为其它命令则执行命令并翻译, \n\t\t\t也可以直接通过“ | ”连接符进行管道翻译")
        else:
            cmd = subprocess.run(sys.argv[1:], shell=True, stdout=subprocess.PIPE, encoding="utf-8",
                                 timeout=cg.timeout, universal_newlines=True)

            tran(cmd.stdout)
    else:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
            sys.stdin.close()

            tran(content)
