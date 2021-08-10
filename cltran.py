#! /usr/bin/env python
import sys
import subprocess
import configparser
from lib.run import run

config = configparser.ConfigParser()
config.read('config.ini', 'utf-8')


def tran(text):
    i = 1
    relist = []
    while True:
        re = 're_%d' % i
        group = 'group_%d' % i
        if config.has_option('regular', re):
            relist.append((config.get('regular', re)[1:-1],
                           config.getint('regular', group) if config.has_option('regular', group) else 0))
        else:
            break
        i += 1

    # relist = [('^ {0,6}\\b(.*):', 1), ('  .*?  \\b(.*)', 1), ('  .*?^[A-Z] \\b(.*)', 1), ('^ {3,30}\\b(.*)', 1),
    #           ('^ ?\\b(.*)', 1)]

    if config.getboolean('cmd', 'show_original_text'):
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
                                 timeout=config.getint('cmd', 'timeout'), universal_newlines=True)

            tran(cmd.stdout)
    else:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
            sys.stdin.close()

            tran(content)
