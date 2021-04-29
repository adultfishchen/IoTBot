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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.lower() == "register":

        event.message.text = event.message.text+" "+DAN.profile['d_name']
        message = event.message.text
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
        # line_bot_api.reply_message(
        #     event.reply_token, TextSendMessage(text=event.message.text))
            
    elif event.message.text.lower() == "exit" :
        DAN.deregister()
        message = event.message.text
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))

    elif event.message.text.lower() == "push":
        IDF_data = random.uniform(1, 10)
        DAN.push('Status', int(IDF_data))  # Push data
        event.message.text = event.message.text+" "+ str(IDF_data)
        message = event.message.text
        line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=message))

    elif event.message.text.lower() == "pull":
        ODF_data = DAN.pull('Name-O')  # Pull data
        if ODF_data != None:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=str(ODF_data[0])))

    else:
        message = event.message.text
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
            
if __name__ == "__main__":

    # connect to IoTtalk server
    ServerURL = 'http://140.114.77.75:9999/'
    Reg_addr = None

    # Define your IoTtalk Device
    # DAN.profile['dm_name'] = 'Remote_control'
    # DAN.profile['df_list'] = ['Knob1', 'Luminance']
    DAN.profile['dm_name'] = 'Wash'
    DAN.profile['df_list'] = ['Status','Name-O']

    # Register
    DAN.device_registration_with_retry(ServerURL, Reg_addr)

    # Deregister
    # DAN.deregister()
    # exit()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
