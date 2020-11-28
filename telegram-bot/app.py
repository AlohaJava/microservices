from quart import Quart,request
import socket
from telethon import TelegramClient
import bot
import json
app = Quart(__name__)

bot.init_bot()

@app.route('/')
def hello_world():
    return 'Telegram bot is Running!'

@app.route('/get_user_count', methods=['POST'])
async def get_user_count():
    try:
        data =await request.json
        result = await bot.get_users_count(data['topic'])
        return str({'count':result})
    except Exception:
        return "Server error!"

@app.route('/invite_user', methods=['POST'])
async def invite_user():
    try:
        data =await request.json
        result = await bot.create_chat(data['user_name'],data['topic'])
        return "OK"
    except Exception:
        return "Server error!"

@app.route('/get_messages', methods=['POST'])
async def get_messages():
    try:
        data =await request.json
        result = await bot.get_message_history(data['topic'])
        return json.dumps(result,ensure_ascii=False,)
    except Exception:
        return "Server Error"

@app.route('/send_message', methods=['POST'])
async def send_message():
    try:
        data =await request.json
        result = await bot.send_message(data['topic'],data['message'])
        return "OK"
    except Exception:
        return "Server Error"

@app.route('/send_message_to_user', methods=['POST'])
async def send_message_to_user():
    try:
        data =await request.json
        result = await bot.send_message_to_user(data['username'],data['message'])
        return "OK"
    except Exception:
        return "Server Error"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
