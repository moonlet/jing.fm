# -*- encoding: utf-8 -*-
'''
一些配置数据
'''


# 多进程通信时socket用到的hostname
hostname = 'localhost'

# 多进程通信时socket用到的端口
port = 5840

# 多进程通信时用到的认证信息, 可随意调整.
authkey = '3.1415926'

# 记录log信息的文件 (会保存在程序目录)
logfile = '.jing.fm.log'

# 用来保证唯一server进程的文件.
lockfile = '/tmp/jing.fm.lock'

# 为避免乱码, 客户端反馈信息的编码格式.
client_code = 'utf-8'
