# main.py
from telethon import TelegramClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

async def fetch_dialogues():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()
    dialogues = []
    async for dialogue in client.iter_dialogs():
        dialogues.append({
            'dialogue_id': dialogue.id,
            'name': dialogue.name
        })
    await client.disconnect()
    return dialogues

async def get_messages_by_dialogue_id(dialogue_id, last_message_date=None):
    messages_list = []  # Список для хранения данных сообщений
    async with TelegramClient('session_name', api_id, api_hash) as client:
        try:
            entity = await client.get_input_entity(dialogue_id)
            async for message in client.iter_messages(entity, offset_date=last_message_date, limit=100):
                # Собираем данные сообщения в словарь
                message_data = {
                    'message_id': message.id,
                    'user_id': message.sender_id,
                    'date': message.date.strftime("%Y-%m-%d %H:%M:%S"),
                    'text': message.text
                }
                messages_list.append(message_data)
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
    return messages_list  # Возвращаем список сообщений
