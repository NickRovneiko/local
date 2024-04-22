import asyncio
from telethon.sync import TelegramClient

api_id = '21992840'  # Ваш API ID
api_hash = 'da0843d28758f33ad168037e277f7bb0'  # Ваш API Hash

async def download_messages():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        try:
            # Используем отрицательный ID для получения сообщений
            entity = await client.get_input_entity(-1001862680773)

            # Получаем последние 100 сообщений из канала или группы
            async for message in client.iter_messages(entity, limit=100):
                print(message.id, message.sender_id, message.date.strftime("%Y-%m-%d %H:%M:%S"), message.text)

        except Exception as e:
            print("Ошибка:", e)

def main():
    # Запускаем асинхронную функцию для загрузки сообщений
    asyncio.run(download_messages())

if __name__ == '__main__':
    main()


