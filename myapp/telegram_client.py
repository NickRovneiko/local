# myproject/myapp/telegram_client.py
from telethon import TelegramClient
from django.conf import settings

# Создаем экземпляр клиента Telegram
telegram_client = TelegramClient('anon_session', '21992840', 'da0843d28758f33ad168037e277f7bb0')

# Функция для запуска клиента, если это еще не было сделано
async def start_telegram_client():
    if not telegram_client.is_connected():
        await telegram_client.connect()
    if not await telegram_client.is_user_authorized():
        print("Client is not authorized. Check your settings.")
        # Тут можно добавить процедуру авторизации, если это необходимо
