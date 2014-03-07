# -*- encoding: utf-8 -*-
'''
封装一套简单的HTTP/HTTPS的GET/POST/HEAD请求
'''

import urllib, urllib2
import cookielib
import zlib
import os
import sys
import types


class Net(object):
  def __init__(self, cookies=".cookies.txt"):
    self.__init_cookie(cookies)
    self.__init_opener()


  def __init_cookie(self, cookies):
    '''
    初始化cookie
    @ cookies: cookie的存放位置
    '''
    cookies = os.path.join(os.path.dirname(__file__), cookies)
    self.__cj = cookielib.LWPCookieJar(cookies)


  def __init_opener(self):
    '''
    初始化opener, 并处理好常规头信息.
    '''
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cj))
    opener.addheaders = [
      ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
      ("Accept-Encoding", "gzip,deflate,sdch"), # gzip压缩
      ("Accept-Language", "zh-CN,zh;q=0.8"),
      ("Connection", "keep-alive"),
      ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36 OPR/18.0.1284.63"),
      ]
    urllib2.install_opener(opener)


  @staticmethod
  def encode_dict(unicode_dict, code_type="utf-8"):
    '''
    统一编码为utf-8, 用作URL的参数
    @ unicode_dict: 可能是unicode的dict
    @ code_type: 就应该是UTF-8
    @ return: 返回编码为UTF-8的dict
    '''
    des_dict = {}
    for key in unicode_dict:
      value = unicode_dict[key]
      if type(key) == types.UnicodeType:
        key = key.encode(code_type)
      if type(value) == types.UnicodeType:
        value = value.encode(code_type)
      des_dict[key] = value
    return des_dict


  def request(self, url, method, param_dict={}, header_dict={}):
    '''
    支持HEAD/GET/POST三种方式的HTTP/HTTPS请求
    @ url: 连接网址, 必须包含HTTP或HTTPS
    @ method: 连接方式，可选HEAD/GET/POST
    @ params: 附加参数
    @ header: 附加头信息
    @ return: 成功返回头信息和数据信息
    @ return: 失败返回None, None
    '''
    params = urllib.urlencode(self.encode_dict(param_dict))
    if method == "GET":
      request = urllib2.Request("%s?%s" % (url, params), None)
    elif method == "POST":
      request = urllib2.Request(url, params)
    elif method == "HEAD":
      request = urllib2.Request("%s?%s" % (url, params), None)
      request.get_method = lambda: "HEAD"

    for key in header_dict:
      request.add_header(key, header_dict[key])

    try:
      response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
      sys.stderr.write("[HTTP_ERROR] $ url=%s, code=%s\n" % (url, e.code))
    except urllib2.URLError as e:
      sys.stderr.write("[URL_ERROR] $ url=%s, reason=%s\n" % (url, e.reason))
    else:
      self.__cj.save()
      response_head = response.info().getheader('Last-Modified')
      info, result = self.unzip(response) if method != "HEAD" else True
      return info, result

  def __save_cookie(self):
    self.__cj.save()

  @staticmethod
  def unzip(response):
    '''
    解压gzip
    @ response: 通过request获取的反馈
    @ return: 返回头信息和数据信息
    '''
    info, result = response.info(), response.read()
    if "Content-Encoding" in info \
    and info["Content-Encoding"] == "gzip":
      try:
        result = zlib.decompress(result, 16+zlib.MAX_WBITS)
      except Exception:
        sys.stderr.write("[UNZIP_ERROR]\n")
    return info, result


if __name__ == "__main__":
  c = Net()
  print c.request("http://www.baidu.com", "GET")



