# -*- coding: UTF-8 -*-

#Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import threading
import time
import DAN

line_bot_api = LineBotApi('sI5/ARrCcKv+kjoMEOSfYB9WJFDVDaNOzU6XExCuvi6nXx/BoZPeOTvnnjc+2pnXnzeeSFtEyar0/4AwhbPUwnuAD5TRjiSWyzIGwFmi6l0sw5xHiPsYz8pduf5zS9Aa+gckehFaHQsYrZ9V2n3qxQdB04t89/1O/w1cDnyilFU=') #LineBot's Channel access token
handler = WebhookHandler('e8b810775604542d3073a965e71573d2')        #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)

ServerURL = 'https://6.iottalk.tw' #with SSL connection
Reg_addr = 'hank2302011115464' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='hank_linebot'
DAN.profile['df_list']=['MSG-I','MSG-O']

DAN.device_registration_with_retry(ServerURL, Reg_addr)

def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()

def pushlinemsg(user_id_set):
    while True:
        msg = DAN.pull('MSG-O')
        msg = str(msg)
        #print('msg:',msg)
        if msg:
            print('PushMsg:{}'.format(msg))
            for usrId in user_id_set:
                if msg!='None':
                    line_bot_api.push_message(userId, TextSendMessage(text=msg))
                    time.sleep(5)


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))
    
    DAN.push ('MSG-I', Msg)
    
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="GOT IT!!"))   # Reply API example
    
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)
        

                    
if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)


    
    try:
       for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='LineBot is ready for you.'))  # Push API example
    except Exception as e:
        print(e)
        
    t = threading.Thread(target=pushlinemsg,args=(user_id_set,)) #f -> function
    t.daemon = True     # this ensures thread ends when main process ends
    t.start()
    
    app.run('127.0.0.1', port=37777, threaded=True, use_reloader=False)

    

