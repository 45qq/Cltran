# cltran
一款 cmd 命令行翻译器<br />​

用于 cmd 各种帮助命令的文本翻译，使用腾讯云批量文本翻译，一次请求翻译 2000 字符。<br />​<br />
## 安装
**要求：python 3.x**
```
pip3 install -r requirement.txt
```


## 准备
在 cltran.ini 中填写腾讯云翻译 api 的 secretId 和 secretKey。<br />​

在[腾讯云控制台](https://console.cloud.tencent.com/) ->云产品->访问管理->访问密钥->API密钥管理中申请。<br />每月免费 500 万字符额度。<br />​<br />
## 使用
```
> cltran -h
usage: cltran <cmd>     cmd为'-h'或'-hlep'显示帮助信息，为其它命令则执行命令并翻译, 
                        也可以直接通过“ | ”连接符进行管道翻译
```

<br />翻译效果：<br />![example1.PNG](https://github.com/45qq/Cltran/blob/master/doc/example1.PNG)<br />
<br />Cltran 使用的是正则匹配翻译，cltran.ini 中已经有一套自带的翻译规则，如有需要请自行在 cltran.ini 中修改。<br />​

cltran.ini：
```
# 这里填写你的腾讯云secretId和secretKey
[api]
secretId=
secretKey=

[cmd]
# 执行命令时的等待时长（s）
timeout=2
# 是否显示原文
show_original_text=0

# 这里填写匹配正则，支持多个正则；
# 当前一个正则不匹配时，则匹配下一个正则。
# re 正则，group 正则匹配组，编号相同的构成一对，可以随意增加。
# re 和 group 一般成对出现，当只有re 时 group 默认为1。
[regular]
re_1='^ {0,6}\b(.*):'
group_1=1
re_2='  .*?  \b(.*)'
group_2=1
re_3='  .*?^[A-Z] \b(.*)'
group_3=1
re_4='^ {3,30}\b(.*)'
group_4=1
re_5='^ ?\b(.*)'
group_5=1
```
