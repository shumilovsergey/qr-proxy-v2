import json
import requests
from project.const import BOT_TOKEN
from .models import Chats
import qrcode
from PIL import Image


def message_get(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'callback_query' in data:
        callback = data['callback_query']['data']
        message_id = data['callback_query']["message"]["message_id"]
        chat_id = data['callback_query']['from']["id"]
        user = Chats.objects.get(chat_id=chat_id)
        user.last_callback = callback
        user.last_id = message_id
        user.save()      
    else:
        chat_id = data["message"]["chat"]["id"]
        message_id = data["message"]["message_id"]
        callback = "none"

    ###
    try: 
        text = data["message"]["text"]
    except:
        text = "none"
    ###    
    try:
        photo_id = data["message"]["photo"][0]["file_id"]
    except:
        photo_id = "none"
    ###
    try: 
        audio_name = data["message"]["audio"]["file_name"]
        audio_type = data["message"]["audio"]["mime_type"]
        audio_id = data["message"]["audio"]["file_id"]
        audio = {
            "audio_name" : audio_name,
            "audio_type" : audio_type,
            "audio_id" : audio_id
        }
    except:
        audio = "none"
    ###
    try:
        document_name = data["message"]["document"]["file_name"]
        document_type = data["message"]["document"]["mime_type"]
        document_id = data["message"]["document"]["file_id"]
        document = {
            "document_name" : document_name,
            "document_type" : document_type,
            "document_id" : document_id
        }
    except:
        document = "none"
    ###
    message = {
        "data" : {
            "chat_id" : chat_id,
            "message_id" : message_id,
            "callback" : callback
        }, 
        "content" : {
            "text" : text,
            "photo_id" : photo_id,
            "audio" : audio,
            "document" : document
        }
    }
    return message

def message_send(chat_id, text, keyboard):
    if keyboard == "none":
        data = { 
            "chat_id": chat_id,
            "text": text
        }
    else:
        data = { 
            "chat_id": chat_id,
            "text": text,
            "reply_markup" : json.dumps(keyboard)
        }

    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data)
    return response

def message_edit(chat_id, message_id, text, keyboard):
    if keyboard == "none":
        data = { 
            "chat_id": chat_id,
            "text": text,
            "message_id" : message_id
        }
    else:
        data = { 
            "chat_id": chat_id,
            "text": text,
            "message_id" : message_id,
            "reply_markup" : json.dumps(keyboard)
        }

    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", data)
    return response

def message_delete(chat_id, message_id):
    data = {
        "chat_id": chat_id,
        "message_id" : message_id
    }
    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage", data)
    return response

def qr_create(chat_id, user):
    url = user.public_url
    qr = qrcode.make(url)
    file_path = "qr.png"
    qr.save(file_path)
    text = "Готово! Вот ваш QrCode"
    keyboard = {
        "inline_keyboard" :  [
            [
                {'text': 'Меню', 'callback_data': 'menu'}
            ]
        ]
    }

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    files = {'photo': open(f"{file_path}", 'rb')}
    data = {
        'chat_id': chat_id,
        'caption': text, 
        "reply_markup" : json.dumps(keyboard)
    }

    response = requests.post(url, files=files, data=data)
    data = response.json()
    photo_id = data['result']['photo'][0]['file_id']
    user.qr_id = photo_id
    user.save()
    return photo_id

def photo_send(chat_id, text, keyboard, photo_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    data = {
        'chat_id': chat_id, 
        'caption': text, 
        'photo': photo_id,
        "reply_markup" : json.dumps(keyboard)
    }

    response = requests.post(url, data=data)
    return response

