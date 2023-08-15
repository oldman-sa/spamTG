Ïfrom telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import time
import random

# Введите свои данные API (api_id, api_hash)
api_id = '12345678'
api_hash = '12345678901234567890123456789012'

session_string = ''
client = TelegramClient(StringSession(session_string), api_id, api_hash)
client.start()

# Список слов или фраз для рандомной отправки
random_words = ["Привет", "Пока"]

async def send_message_to_user(target_username, message, count):
    try:
        target_entity = await client.get_input_entity(target_username)

        for _ in range(count):
            await client.send_message(target_entity, message)
            print('Сообщение отправлено!')
            time.sleep(0.1)  # Задержка в 0.1 секунды между сообщениями
    except Exception as e:
        print(f'Ошибка при отправке сообщения: {e}')

async def delete_last_messages(target_entity, count):
    try:
        async for message in client.iter_messages(target_entity, limit=count):
            await client.delete_messages(target_entity, [message])
            print(f'Сообщение {message.id} удалено!')
            time.sleep(0.1)  # Задержка в 0.1 секунды между удалениями
    except Exception as e:
        print(f'Ошибка при удалении сообщений: {e}')

@client.on(events.NewMessage(pattern=r'\.спам', outgoing=True))
async def handle_spam_command(event):
    try:
        _, target_username, count, message = event.raw_text.split(' ', 3)
        count = int(count)
        
        await send_message_to_user(target_username, message, count)
    except Exception as e:
        print(f'Ошибка при обработке команды .спам: {e}')

@client.on(events.NewMessage(pattern=r'\.дел', outgoing=True))
async def handle_delete_command(event):
    try:
        _, target_entity, count = event.raw_text.split(' ', 2)
        count = min(int(count), 10)  # Устанавливаем максимальное количество удаляемых сообщений: 10
        
        await delete_last_messages(target_entity, count)
    except Exception as e:
        print(f'Ошибка при обработке команды .дел: {e}')

@client.on(events.NewMessage(pattern=r'\.ранд', outgoing=True))
async def handle_random_command(event):
    try:
        _, target_username, count = event.raw_text.split(' ', 3)
        count = int(count)
        
        for _ in range(count):
            random_word = random.choice(random_words)
            await send_message_to_user(target_username, random_word, 1)
    except Exception as e:
        print(f'Ошибка при обработке команды .ранд: {e}')

print('Bot started!')
client.run_until_disconnected()
