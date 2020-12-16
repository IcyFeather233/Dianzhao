# coding=utf-8
import socketio
import json
import requests
import pdb
import re
import logging
import time
import socket

'''
Python插件SDK Ver 0.0.2
维护者:enjoy(2435932516)
有问题联系我。
'''
targetQQ = "183319180"
robotqq = "2054479045"  # 机器人QQ号
webapi = "http://127.0.0.1:8888"  # Webapi接口 http://127.0.0.1:8888
sio = socketio.Client()
# log文件处理
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=0,
                    filename='new.log', filemode='a')


class GMess:
    # QQ群消息类型
    def __init__(self, message1):
        # print(message1)
        self.FromQQG = message1['FromGroupId']  # 来源QQ群
        self.QQGName = message1['FromGroupName']  # 来源QQ群昵称
        self.FromQQ = message1['FromUserId']  # 来源QQ
        self.FromQQName = message1['FromNickName']  # 来源QQ名称
        self.Content = message1['Content']  # 消息内容


def send(ToQQ, Content, sendToType, atuser=0, sendMsgType='TextMsg', groupid=0):
    tmp = {}
    tmp['sendToType'] = sendToType
    tmp['toUser'] = ToQQ
    tmp['sendMsgType'] = sendMsgType
    tmp['content'] = Content
    tmp['groupid'] = 0
    tmp['atUser'] = atuser
    tmp1 = json.dumps(tmp)
    requests.post(webapi + '/v1/LuaApiCaller?funcname=SendMsg&qq=' + robotqq, data=tmp1)


def zan(QQ):
    # QQ名片赞
    tmp = {}
    tmp['UserID'] = QQ
    tmp1 = json.dumps(tmp)
    requests.post(webapi + '/v1/LuaApiCaller?funcname=QQZan&timeout=10&qq=' + robotqq, data=tmp1)


def sendPic(ToQQ, Content, sendToType, imageUrl):
    # 发送图片信息
    tmp = {}
    tmp['sendToType'] = sendToType
    tmp['toUser'] = ToQQ
    tmp['sendMsgType'] = "PicMsg"
    tmp['content'] = Content
    tmp['picBase64Buf'] = ''
    tmp['fileMd5'] = ''
    tmp['picUrl'] = imageUrl
    tmp1 = json.dumps(tmp)
    # print(tmp1)
    print(requests.post(webapi + '/v1/LuaApiCaller?funcname=SendMsg&timeout=10&qq=' + robotqq, data=tmp1).text)


class Mess:
    def __init__(self, message1):
        self.FromQQ = message1['ToUin']
        self.ToQQ = message1['FromUin']
        self.Content = message1['Content']


# standard Python

# SocketIO Client
# sio = socketio.AsyncClient(logger=True, engineio_logger=True)

# -----------------------------------------------------
# Socketio
# -----------------------------------------------------
def beat():
    while (1):
        print("beating...")
        sio.emit('GetWebConn', robotqq)
        time.sleep(60)


@sio.event
def connect():
    print('connected to server')
    sio.emit('GetWebConn', robotqq)  # 取得当前已经登录的QQ链接
    beat()  # 心跳包，保持对服务器的连接


@sio.on('OnGroupMsgs')
def OnGroupMsgs(message):
    ''' 监听群组消息'''
    tmp1 = message
    tmp2 = tmp1['CurrentPacket']
    tmp3 = tmp2['Data']
    a = GMess(tmp3)
    cm = a.Content.split(' ', 3)  # 分割命令
    '''
    a.FrQQ 消息来源
    a.QQGName 来源QQ群昵称
    a.FromQQG 来源QQ群
    a.FromNickName 来源QQ昵称
    a.Content 消息内容
    '''

    menumsg = '''
    店招控制命令如下：
    1. #Openit: 开启店招
    2. #Closeit: 关闭店招
    3. #ShowMode: 显示模式
    4. #SetMode: 设置模式
    '''

    modemenu = '''
    HTTP-API 详情请查看
    https://github.com/Aircoookie/WLED/wiki/HTTP-request-API
    常用命令：
    &A=(0 to 255)    -- master brightness
    &T=(0,1,or 2)    -- master off/on/toggle
    &FX=(0 to 101)   -- LED Effect Index
    
    范例:
    输入#SetMode &T=2 可以切换店招开关状态
    '''

    if (str(a.FromQQG) == targetQQ):
        if str(a.Content) == '#店招':
            send(a.FromQQG, menumsg, 2, a.FromQQ)
            return
        elif str(a.Content) == '#Openit':
            send(a.FromQQG, "店招已开启", 2, a.FromQQ)
            mqttTest.run("T=1")
            return
        elif str(a.Content) == '#Closeit':
            send(a.FromQQG, "店招已关闭", 2, a.FromQQ)
            mqttTest.run("T=0")
            return
        elif str(a.Content).find('#SetMode') != -1:
            op = str(a.Content).replace('#SetMode', '', 1)
            mqttTest.run(op.strip())
            send(a.FromQQG, "模式已设置", 2, a.FromQQ)
            return
        elif str(a.Content) == '#ShowMode':
            send(a.FromQQG, modemenu, 2, a.FromQQ)
            return



@sio.on('OnFriendMsgs')
def OnFriendMsgs(message):
    ''' 监听好友消息 '''
    tmp1 = message
    tmp2 = tmp1['CurrentPacket']
    tmp3 = tmp2['Data']
    a = Mess(tmp3)
    # print(tmp3)
    cm = a.Content.split(' ')
    if a.Content == '#菜单':
        send(a.ToQQ, "你好", 1)


@sio.on('OnEvents')
def OnEvents(message):
    ''' 监听相关事件'''
    print(message)


# -----------------------------------------------------
def main():
    try:
        sio.connect(webapi, transports=['websocket'])
        # pdb.set_trace() 这是断点
        sio.wait()
    except BaseException as e:
        logging.info(e)
        print(e)


if __name__ == '__main__':
    main()
