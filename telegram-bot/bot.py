import asyncio

from telethon.sync import TelegramClient
from telethon import functions, types
import db

api_id = 2421070
api_hash = '09cf660e04aaee9a5b8e88ea644c556f'
username = '79885430081'
client=None
def get_client():
    global client
    return client

def init_bot():
    global client
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    client.get_dialogs(limit=None)


async def invite_to_chat(chat_id, id):
    global client
    try:
        result = await client(functions.messages.AddChatUserRequest(
            chat_id,
            id,
            fwd_limit=5000
        ))
    except Exception:
        pass


async def create_chat(id, title):
    global client
    chat_id = db.get_chat_id(title)
    if (chat_id != None):
        await invite_to_chat(chat_id, id)
    else:
        result = await client(functions.messages.CreateChatRequest(
            users=[id],
            title=title
        ))
        id = result.to_dict()['updates'][1]['participants']['chat_id']
        db.update_chat_id(title, id)
        await send_grettings(id, title)


def get_all_chats():
    global client
    result = client(functions.messages.GetAllChatsRequest(
        except_ids=[]
    ))
    return result


async def send_grettings(chat_id, title):
    global client
    e = await client.get_entity(chat_id)
    await client(functions.messages.SendMessageRequest(
        e,
        message="Добро пожаловать в обсуждение темы {0}!".format(title)
    ))


async def send_message(topic, message):
    global client
    chat_id = db.get_chat_id(topic)
    e =await client.get_entity(chat_id)
    await client(functions.messages.SendMessageRequest(
        e,
        message=message
    ))


async def send_message_to_user(username, message):
    global client
    e =await client.get_entity(username)
    await client(functions.messages.SendMessageRequest(
        e,
        message=message
    ))


async def get_username_by_id(user_id):
    global client
    rez = (await client.get_entity(user_id)).to_dict()
    return rez['first_name'] + ((" "+rez['last_name']) if rez['last_name'] != None else "")


async def get_message_history(topic):
    global client
    chat_id = db.get_chat_id(topic)
    e = await client.get_entity(chat_id)
    result = await client.get_messages(e, limit=10)
    rez = []
    for elem in result:
        try:
            mdict = elem.to_dict()
            rez.append({'message': mdict['message'], 'user_name': mdict['from_id']['user_id']})
        except Exception:
            pass
    cache = {}
    for elem in rez:
        if elem['user_name'] in cache:
            elem['user_name'] = cache[elem['user_name']]
        else:
            cache[elem['user_name']] =await get_username_by_id(elem['user_name'])
            elem['user_name'] = cache[elem['user_name']]
    return rez


async def get_users_count(topic):
    global client
    chat_id = db.get_chat_id(topic) #тут все ок
    result = await client.get_entity(chat_id)
    return result.to_dict()['participants_count']
