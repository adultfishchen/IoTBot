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
@app.route("/", methods=['POST'])
def callback():
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
    print(event)
    text=event.message.text

    if (text=="Hi"):
        reply_text = "Hello"
        #Your user ID

    elif(text=="你好"):
        reply_text = "哈囉"
    elif(text=="機器人"):
        reply_text = "叫我嗎"
    else:
        reply_text = text
#如果非以上的選項，就會學你說話
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

# if __name__ == "__main__":

    # # connect to IoTtalk server
    # ServerURL = 'http://140.114.77.75:9999/'
    # Reg_addr = None

    # # Define your IoTtalk Device
    # DAN.profile['dm_name'] = 'Remote_control'
    # DAN.profile['df_list'] = ['Knob1', 'Luminance', ]

    # # Register
    # DAN.device_registration_with_retry(ServerURL, Reg_addr)

    # # Deregister
    # DAN.deregister()
    # exit()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # port = int(os.environ.get('PORT', 8000))
    # app.run(host='0.0.0.0', port=port)
