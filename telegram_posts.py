import json
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import my_config
import os

session_file = f"{my_config.number}.session"
if os.path.exists(session_file):
    print(f"📂 Используется сессия: {session_file}")
else:
    print("⚠️ Файл сессии не найден. Будет создан новый.")
# Конфигурация
api_id = my_config.api_id
api_hash = my_config.api_hash
number = my_config.number
channel_username = "shot_shot"
output_file = "shot_posts.json"


async def fetch_posts():
    print("🔄 Запуск клиента...")
    async with TelegramClient(number, api_id, api_hash) as client:
        print(f"📡 Подключение к каналу @{channel_username}...")
        entity = await client.get_entity(channel_username)

        all_messages = []
        offset_id = 0
        limit = 100
        total_messages = 0
        max_posts = 5000
        offset_date = None

        print("🚀 Начинаю парсинг сообщений...")
        while total_messages < max_posts:

            try:
                history = await client(GetHistoryRequest(
                    peer=entity,
                    offset_id=offset_id,
                    offset_date=offset_date,
                    add_offset=0,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
            except Exception as e:
                print(f"❌ Ошибка при получении истории: {e}")
                break

            if not history.messages:
                print("✅ Сообщения закончились.")
                break

            messages = history.messages
            print(f"📝 Обработка {len(messages)} сообщений...")

            for msg in messages:
                if not msg.message and not msg.media:
                    continue

                # Реакции
                reaction_data = {}
                if msg.reactions and msg.reactions.results:
                    for reaction in msg.reactions.results:
                        emoji = getattr(reaction.reaction, "emoticon", "🔒")
                        reaction_data[emoji] = reaction.count

                # Ссылки
                urls = [ent.url for ent in msg.entities if hasattr(ent, 'url')] if msg.entities else []

                media_type = type(msg.media).__name__ if msg.media else None

                all_messages.append({
                    "id": msg.id,
                    "date": str(msg.date),
                    "text": msg.message if msg.message else None,
                    "views": msg.views,
                    "reactions": reaction_data if reaction_data else None,
                    "replies_count": msg.replies.replies if msg.replies else None,
                    "forwards": msg.forwards,
                    "media_type": media_type,
                    "has_media": bool(msg.media),
                    "links": urls if urls else None
                })

            total_messages += len(messages)
            offset_id = messages[-1].id
            offset_date = messages[-1].date  # Обновим offset_date по последнему сообщению

            print(f"📊 Суммарно скачано {total_messages} сообщений")

        print(f"✅ Парсинг завершён. Всего сообщений: {len(all_messages)}")

        print(f"💾 Сохраняю данные в файл: {output_file}...")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(all_messages, file, ensure_ascii=False, indent=4)

        print("✅ Готово! Файл сохранён.")


if __name__ == "__main__":
    print("👋 Скрипт запускается...")
    asyncio.run(fetch_posts())
