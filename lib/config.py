import configparser
import sys
from os import path


config_path = path.join(path.dirname(path.realpath(sys.argv[0])), 'cltran.ini')

config = configparser.ConfigParser()
config.read(config_path, 'utf-8')

# api
secretId = config.get('api', 'secretId')
secretKey = config.get('api', 'secretKey')

if secretId == '' or secretKey == '':
    print("请先在 cltan.ini 文件中填写 secretId 和 secretKey。")
    sys.exit(0)

# cmd
timeout = config.getint('cmd', 'timeout')
show_original_text = config.getboolean('cmd', 'show_original_text')


# regular
def get_relist():
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
    return relist
