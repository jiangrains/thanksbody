# -*- encoding: utf-8 -*-

import urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

appid = 'wx127e9b641dc9ff55'
secret = '4a2e07920d2a8380b87904a6a2512ef3'
gettoken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret

if 0:
    f = urllib2.urlopen( gettoken )
    stringjson = f.read() 
    access_token = json.loads(stringjson)['access_token']
    print access_token
else:
    access_token = 'ZquTOqlqCVRXvOl3cId0JPz1tfQg9AKNH564t0_RK_JgNOBT5BCTUkCejmQp7Av10LT4B4Kza_mLXTTozvx6HzIAH-uTIzo8T0jmrNyPrTILJNaACAOMQ'

posturl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token

menu = '''{
    "button":[
        {
           "name":"开始健身",
           "sub_button":
            [{
               "type":"click",
               "name":"预约教练",
               "key":"V1001_ORDER_COACH"
            },
            {
               "type":"click",
               "name":"预约课程",
               "key":"V1001_ORDER_COURSE"
            },
            {
               "type":"click",
               "name":"场馆状态",
               "key":"V1001_GYM_STATUS"
            },
            {
               "type":"view",
               "name":"测试网页",
               "url":"http://112.74.133.182/hello/"
            }
            ]
        },
        {
           "name":"订单中心",
           "sub_button":
            [{
               "type":"click",
               "name":"我的订单",
               "key":"V1001_MYORDER"
            },
            {
               "type":"click",
               "name":"我的余额",
               "key":"V1001_MYBALANCE"
            },
            {
               "type":"click",
               "name":"购买课程",
               "key":"V1001_BUYCOURSES"
            }
            ]
        },
        {
           "name":"我",
           "sub_button":
            [{
               "type":"click",
               "name":"健康报表",
               "key":"V1001_REPORT"
            },
            {
               "type":"click",
               "name":"个人信息",
               "key":"V1001_INFORMTATION"
            },
            {
               "type":"click",
               "name":"投诉建议",
               "key":"V1001_COMPLAIN"
            }
            ]
        }
    ]
}'''

request = urllib2.urlopen(posturl, menu.encode('utf-8') )

print request.read()
