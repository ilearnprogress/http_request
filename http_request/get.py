#!/usr/bin/python
#coding:gbk
import httplib
import urlparse
import time  
import urllib
import sys

def req(method, url, data, cookie='' ):
    ret = urlparse.urlparse(url)    # Parse input URL
    if ret.scheme == 'http':
        conn = httplib.HTTPConnection(ret.netloc)
    elif ret.scheme == 'https':
        conn = httplib.HTTPSConnection(ret.netloc)
        
    url = ret.path
    if ret.query: url += '?' + ret.query
    if ret.fragment: url += '#' + ret.fragment
    if not url: url = '/'
    
    method = method
    conn.request(method=method, url=url , headers={'Cookie': cookie, 'Content-Type':'application/x-www-form-urlencoded'}, body=urllib.urlencode(data))
    return conn.getresponse()

if __name__ == '__main__':
    cookie_str = 'JSESSIONID=24647B236727A3400FACC7CBC84E364E; Hm_lvt_ca4c14789976af32ed421eba13cd0981=1465776443; Hm_lpvt_ca4c14789976af32ed421eba13cd0981=1467849596; JSESSIONID=792A7262D6978977B1C8C77D91280F54; SERVERID=e67954bb2bd92a547b320a9d68f522e2|1467849614|1467849594'

    get_url = 'http://182.92.48.186/sac/stubm/selectdstinit.htm?examstupid=1029&userid=10801c9af499d442&bmid=eca406e077ef543a&examid=57bcea9c35beebcb'
    while 1:       
        html_doc = req('GET', get_url, {}, cookie_str).read()
        # print html_doc
        import re
        # html_doc = ' <option value="1" >深圳1</option> <option value="1" >深圳2</option>'
        kds = re.findall('<option value="(.*?)" >(.*?)</option>', html_doc, re.IGNORECASE)
        # print kds
        key = '深圳'
        for kd in kds:
            print str(kd[1]), str(kd[0]), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if str(kd[1]).find(key) > -1 :
                post_url = 'http://182.92.48.186/sac/stubm/selectds.htm'
                data = {'bmid':'eca406e077ef543a', 'examid':'57bcea9c35beebcb', 'userid' : '10801c9af499d442', 'hends':str(kd[0]), 'ds':str(kd[0])}
                html_doc = req('POST', post_url, data, cookie_str).read()
                print '========OK=============', str(kd[1]), str(kd[0])
                sys.exit() 
        time.sleep(600)
    # print html_doc