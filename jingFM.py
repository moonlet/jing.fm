#!/usr/bin/env  python
# -*- encoding: utf-8 -*-
'''
为了方便, 将boot, help放在了外围的Command类中
'''

import util
import os
import multiprocessing
import sys

USAGE = u'\
使用帮助:\n\
命令分为2部分: 命令对象 [命令参数]. 所有的命令包括:\n\
    0. boot: 用来开启服务程序, 如果已经开启了再输入会报错.\n\
    1. help: 显示当前内容.\n\
    2. cmbt: 关键词. 更换关键词, 例如: cmbt 刘德华.\n\
    3. next: 下一曲.\n\
    4. love: 桃心标记当前曲目.\n\
    5. hate: 当前歌曲扔垃圾桶.\n\
    6. info: 显示当前播放歌曲的信息.\n\
    7. exit: 退出, 因为程序包含多个线程, 所以 CTRL+C 效果不会好哦!\n\
例如: jingFM.py login your-email your-password.\
'


class Command(object):
    def __init__(self):
        # 命令->操作的映射词典
        self.cmd_dict = {
            'boot': self.cmd_boot,
            'help': self.cmd_help,
        }

    def run(self):
        '''
        当前类的运行总函数
        '''
        if len(sys.argv) < 2:
            # 如果输入格式不正确自动展示 "帮助"
            self.cmd_help()
            sys.exit(1)

        cmd_list = sys.argv[1:]
        cmd = "\t".join(cmd_list)

        # 命令->操作的映射
        op = self.cmd_dict.get(cmd_list[0], self.cmd_client)
        # 运行操作
        op(cmd)

    def cmd_boot(self, cmd=None):
        '''
        启动服务端的进程
        '''
        try:
            # fork 进程
            pid = os.fork()
            # pid > 0: 父进程, pid == 0: 子进程
            if pid > 0:  # 父进程不要
                sys.exit(0)
        except OSError:
            sys.exit(1)

        try:
            server = util.Server()
        except util.JC as e:
            # 此处用来告知用户 "已经开启了服务进程"
            print "! %s" % (e.msg.encode(util.config.client_code))
            return
        else:
            # 正确开启第一个服务进程
            print (u"> 开启成功").encode(util.config.client_code)
            server.run()

    def cmd_help(self, cmd=None):
        '''
        输入help和格式错误时的USAGE展示
        '''
        print USAGE.encode(util.config.client_code)

    def cmd_client(self, cmd):
        '''
        将命令交付给client进程, 传递给server.
        '''
        client = util.Client()
        client.run(cmd)

if __name__ == '__main__':
    cmd = Command()
    cmd.run()
