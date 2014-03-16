# -*- encoding: utf-8 -*-
'''
用来和服务端交互的客户端.
主要功能:
  1. 传递命令给服务端.
  2. 展示服务端传回的反馈信息.
'''

from multiprocessing.connection import Client as MultiClient
import config


class Client():
  def run(self, cmd):
    '''
    传递命令给server, 同时展示传回信息.
    @ cmd: 命令, 以tab分割.
    '''
    conn = MultiClient(
        (config.hostname, config.port),
        authkey=config.authkey,
    )
    # 传送命令
    conn.send(cmd)
    try:
      # 收取信息
      recv_data = conn.recv_bytes()
    except EOFError:
      pass
    else:
      # 传回的数据是unicode编码的
      unicode_recv_data = eval(recv_data)
      # 按照设定编码print反馈数据
      print unicode_recv_data.encode(config.client_code)
    finally:
      conn.close()


if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2:
    sys.exit(1)

  cmd_list = sys.argv[1:]
  cmd = "\t".join(cmd_list)
  client = Client()
  client.run(cmd)
