# -*- encoding: utf-8 -*-
'''
封装一套不同logging等级的Exception
等级对应logging的等级体系.
  1. CRITICAL: 出现无法再播放的致命错误, 程序会退出.
  2. ERROR: 出现错误, 但是任然能播放音乐, 程序不会退出.
  3. WARNING: 用户参与的操作出错, 一般附加功能无法使用, 不影响主功能.
  4. INFO: 给用户传递的信息
  5. DEBUG: 本程序没有使用
'''

import logging
import config
import sys
import os


# 调整logging配置
logging.basicConfig(
    filename=os.path.join(os.path.split(sys.argv[0])[0], config.logfile),
    level=logging.WARNING,
    filemode='a',
    format='%(levelname)s: %(asctime)s [%(lineno)s] : %(message)s',
)


class JingException(Exception):
    '''
    封装的Exception的基类.
    考虑到还存在logging等级, 所以新建一个Exception.
    '''
    def __init__(self, msg, e='', codec='UTF-8'):
        '''
        初始化JingException.
        @ msg: 自己的错误提示信息
        @ e: 底层一级传来的Exception
        '''
        self.msg = msg
        self.e = e
        self.__log_codec = codec

    def make_log(self):
        '''
        格式化log信息.
        '''
        content = "[%s] %s" % (self.msg.encode(self.__log_codec), str(self.e))
        content = content.rstrip()
        return content

    def log(self):
        '''
        保存log信息
        '''
        pass


class JingCritical(JingException):
    '''
    CRITICAL等级的Exception.
    '''
    def __init__(self, msg, e='', codec='UTF-8'):
        JingException.__init__(self, msg, e, codec)
        self.log()

    def log(self):
        content = self.make_log()
        logging.critical(content)


class JingError(JingException):
    '''
    ERROR等级的Exception.
    '''
    def __init__(self, msg, e='', codec='UTF-8'):
        JingException.__init__(self, msg, e, codec)
        self.log()

    def log(self):
        content = self.make_log()
        logging.error(content)


class JingWarning(JingException):
    '''
    WARNING等级的Exception.
    '''
    def __init__(self, msg, e='', codec='UTF-8'):
        JingException.__init__(self, msg, e, codec)
        self.log()

    def log(self):
        content = self.make_log()
        logging.warning(content)


class JingInfo(JingException):
    '''
    INFO等级的Exception.
    '''
    def __init__(self, msg, e='', codec='UTF-8'):
        JingException.__init__(self, msg, e, codec)
        self.log()

    def log(self):
        content = self.make_log()
        logging.info(content)


class JingDebug(JingException):
    '''
    DEBUG等级的Exception. 暂时没用上.
    '''
    def __init__(self, msg, e='', codec='UTF-8'):
        JingException.__init__(self, msg, e, codec)
        self.log()

    def log(self):
        content = self.make_log()
        logging.debug(content)
