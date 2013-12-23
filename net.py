# -*- encoding: utf-8 -*-
import urllib2
import urllib
import cookielib
import zlib
import os
import sys
import types


class Net(object):
  def __init__(self, cookies="temp/cookies.txt"):
    self.__init_cookie(cookies)
    self.__init_opener()

  def __init_cookie(self, cookies):
    cookies = os.path.join(os.path.dirname(__file__), cookies)
    self.__cj = cookielib.LWPCookieJar(cookies)

  def __init_opener(self):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cj))
    opener.addheaders = [
      ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
      ("Accept-Encoding", "gzip,deflate,sdch"),
      ("Accept-Language", "zh-CN,zh;q=0.8"),
      ("Connection", "keep-alive"),
      ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36 OPR/18.0.1284.63"),
      ]
    urllib2.install_opener(opener)

  @staticmethod
  def encode_dict(unicode_dict, code_type="utf-8"):
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
    """支持HEAD/GET/POST三种方式的HTTP请求
    参数：
      url：连接网址
      method：连接方式，可选HEAD/GET/POST
      params：附加参数
      header：附加头信息
    """

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
      result, info = self.unzip(response) if method != "HEAD" else True
      return info, result

  def __save_cookie(self):
    self.__cj.save()

  @staticmethod
  def unzip(response):
    info, result = response.info(), response.read()
    if "Content-Encoding" in info and info["Content-Encoding"] == "gzip":
      try:
        result = zlib.decompress(result, 16+zlib.MAX_WBITS)
      except Exception as e:
        sys.stderr.write("[UNZIP_ERROR]\n")
    return result, info


if __name__ == "__main__":
  c = Net()
  c.init_cookie()
  print c.request("http://jing.fm/api/v1/sessions/create", "POST", {"email":"xiaorx@live.com", "pwd":"411100"})



