from flask import Flask, request, abort
import DAN
import csmapi
import random
import time
import threading
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random
import threading
import requests

from datetime import datetime

from urllib.request import urlretrieve

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

# 監聽所有來自 /callback 的 Post Request


# 監聽所有來自 /callback 的 Post Request
@app.route("/", methods=['GET', 'POST'])
def callback():
    if request.method == "GET":
        return "Hello! This is an echo LineBot"
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# IOTtalk
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     if event.message.text.lower() == "register":
#         ServerURL = 'http://140.114.77.75:9999/'
#         Reg_addr = None

#         DAN.profile['dm_name'] = 'Remote_control'
#         DAN.profile['df_list'] = ['Knob1','Luminance',]

#         DAN.device_registration_with_retry(ServerURL, Reg_addr)
#         message = event.message.text
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=DAN.profile['d_name']))

#     elif event.message.text.lower() == "push":
#         IDF_data = random.uniform(1, 10)
#         DAN.push('Knob1', IDF_data)  # Push data
#         # message = event.message.text
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=IDF_data))
#     elif event.message.text.lower() == "pull":
#         ODF_data = DAN.pull('Luminance')  # Pull data
#         if ODF_data != None:
#             line_bot_api.reply_message(
#                 event.reply_token, TextSendMessage(text=ODF_data[0]))
#             time.sleep(1)

#     elif event.message.text.lower() == "quit" or event.message.text.lower() == "exit" or event.message.text.lower() == "deregister":
#         DAN.deregister()
#         message = event.message.text
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=message))

#     else:
#         message = event.message.text
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=message))

# 處理訊息


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token, message)

    # you can wrtie some codes here to handle the message sent by users
    cmd = event.message.text
    if cmd is '1':
        S = DAN.profile['d_name']
        reply = event.message.text + "這台機器狀態為" + str(S)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    
    else:
        reply = "不是指令"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        


def receive():
    while True:
        id = DAN.pull('Name-O')  # list
        # record
        if id != None:
            washM_dict['w0'] = int(id[0])
            washM_dict['w1'] = int(id[0])
            washM_dict['w2'] = int(id[0])

            print(washM_dict['w0'])

        time.sleep(1)


def send():
    while True:
        IDF_data = random.uniform(1, 10)
        DAN.push('Status', int(IDF_data))
        time.sleep(1)


if __name__ == "__main__":

    ServerURL = 'http://140.114.77.73:9999'  # with no secure connection
    Reg_addr = None  # if None, Reg_addr = MAC address

    # Define your IoTtalk Device
    # DAN.profile['dm_name']=???
    # DAN.profile['df_list']=???
    # DAN.profile['d_name']= ???
    DAN.profile['dm_name'] = 'Wash'
    DAN.profile['df_list'] = ['Status', 'Name-O']

    # Register
    DAN.device_registration_with_retry(ServerURL, Reg_addr)

    # you can write a generator to random sensor data and then push to the IoTtalk
    # maybe use thread

    # you can create a thread function to pull the data from the IoTtalk

    t = threading.Thread(target=receive)
    t.daemon = True     # this ensures thread ends when main process ends
    t.start()

    t1 = threading.Thread(target=send)
    t1.daemon = True     # this ensures thread ends when main process ends
    t1.start()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
