from flask import Flask, request, make_response
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.client import WeChatClient
from chatgpt.chatgpt import ChatGPT

app = Flask(__name__)
# OpenAI的api
api_key = 'your_api_key'

# 微信公众号的AppID和AppSecret
APPID = 'your_appid'
APPSECRET = 'your_appsecret'

# 微信服务器配置的Token和EncodingAESKey
TOKEN = 'your_token'
ENCODING_AES_KEY = 'your_encoding_aes_key'

# 实例化微信客户端
client = WeChatClient(APPID, APPSECRET)

# 实例化ChatGPT
chat = ChatGPT(api_key)

question = ''


@app.route('/', methods=['GET', 'POST'])
def wechat():
    # 验证消息的签名
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        return 'Invalid signature', 400

    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        return echo_str
    else:
        # 解析微信服务器发送的消息和事件
        msg = parse_message(request.data)
        # 自定义的消息处理器
        reply = custom_reply(msg)
        # 将回复包装成XML格式，以响应微信服务器
        xml = reply.render()
        return make_response(xml)


def custom_reply(msg):
    # 处理不同类型的消息和事件

    if msg.type == 'text':
        global question
        question = msg.content
        reply = create_reply('', msg)
    elif msg.type == 'image':
        reply = create_reply('您发送了一张图片', msg)
    elif msg.type == 'event':
        if msg.event == 'subscribe':
            reply = create_reply('欢迎关注霍山散木', msg)
        else:
            reply = create_reply('您触发了一个未知的事件', msg)
    else:
        reply = create_reply('您发送了一个未知的消息类型', msg)
    return reply


def process(msg):
    global question
    if question == '':
        return
    else:
        reply = create_reply(chat.ask(question))
        question = ''
        return reply


if __name__ == '__main__':
    app.run(port=14514, debug=True)
