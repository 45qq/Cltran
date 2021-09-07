from progress.bar import Bar
from colorama import init, Fore, Back, Style
import lib.translation as tran
import sys
import re


init(autoreset=True)


def tran_text(bar, content_lines, relist, retu_relist=None):
    if not relist:
        return

    lines = []

    for line in content_lines:
        re_content = get_re_content(line, relist)
        if re_content:
            trs = tran.get_tran(re_content[0])
            new_line = ''
            try:
                new_line = "%s%s%s" % (re_content[1][:re_content[2]], trs, re_content[1][re_content[2]:])
            except Exception as e:
                print(e, re_content, trs)
            if retu_relist:
                re_contents = get_ret_re_content(new_line, retu_relist)
                if re_contents:
                    new_line = re_contents
            lines.append(new_line)
        else:
            lines.append(line)
        bar.next()
    bar.finish()
    return '\n'.join(lines)


def tran_texts(bar, content_lines, relist, retu_relist=None):
    if not relist:
        return

    lines = []
    re_content_lines = []
    tran_lines = []
    i = 0
    while i < len(content_lines):
        line = content_lines[i]
        re_content = get_re_content(line, relist)

        tran_len = 0
        re_content_len = 0

        if re_content:
            tran_len = len(''.join(tran_lines)) + len(tran_lines) * 2
            re_content_len = len(re_content[0]) + 5
            if tran_len + re_content_len < 2000:
                tran_len += re_content_len
                re_content_lines.append((i, re_content))
                tran_lines.append(re_content[0])

            if len(lines) == i:
                lines.append("[待定 <%d>]" % i)

        elif len(lines) == i:
            lines.append(line)
            bar.next()

        if tran_len + re_content_len > 2000 or i + 1 == len(content_lines):
            if tran_len + re_content_len > 2000:
                i -= 1
                bar.next(-1)

            trs = tran.get_tran_list(tran_lines)
            for tr, re_content_line in zip(trs, re_content_lines):
                re_content = re_content_line[1]

                new_line = "%s%s%s" % (re_content[1][:re_content[2]], tr, re_content[1][re_content[2]:])

                if retu_relist:
                    re_contents = get_ret_re_content(new_line, retu_relist)
                    if re_contents:
                        new_line = re_contents

                lines[re_content_line[0]] = new_line

            bar.next(len(tran_lines))
            tran_lines.clear()
            re_content_lines.clear()

        i += 1

    bar.finish()
    return '\n'.join(lines)


def get_re_content(line, relist):
    """

    :param line:
    :param relist:
    :return: 返回一个含有三个元素的数组 [待翻译的内容, 除去待翻译的内容的前后内容, 待翻译的内容所在位置]
    """

    for i, j in relist:
        try:
            re_obj = re.search(i, line)
            if re_obj:
                return re_obj.group(j), "%s%s" % (line[:re_obj.start(j)], line[re_obj.end(j):]), re_obj.start(j)
        except Exception:
            print(Fore.RED + Back.BLACK + Style.BRIGHT + "\n正则表达式错误！")
            sys.exit(0)


def get_ret_re_content(line, relist):
    for i, j, k in relist:
        re_obj = re.search(i, line)
        if re_obj:
            return line.replace(re_obj.group(j), k)


def run(content, relist, retu_relist=None):
    """
    用正则翻译文本。

    :param content: 要翻译的文本内容
    :param relist: 用于开始匹配的两个参数的元组列表 (正则, 组)
    :param retu_relist: 用于返回匹配的两个参数的元组列表 (正则, 组)
    :return: 翻译的内容
    """
    if not len(relist):
        return

    content_lines = content.split('\n')
    bar = Bar('已翻译', max=len(content_lines), fill='-', suffix='%(percent)d%%')
    bar.start()
    return tran_texts(bar, content_lines, relist, retu_relist)

# print(run(' content:\n  mean <word> meaning', [(r'  .{0,27} \b([a-zA-Z].*)', 1), (r' \b([a-zA-Z ].*):', 1)]))
