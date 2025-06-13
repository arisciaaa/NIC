import asyncio
from telethon.sync import TelegramClient
import my_config


async def main():
    client = TelegramClient(my_config.number, my_config.api_id, my_config.api_hash)

    await client.connect()

    if not await client.is_user_authorized():
        phone = input("Введите ваш номер телефона: ")
        await client.send_code_request(phone)

        code = input("Введите код подтверждения: ")
        try:
            await client.sign_in(phone, code)
        except Exception as e:
            print(f"Ошибка входа: {e}")
            if "password is required" in str(e):
                password = input("Введите пароль от двухфакторной аутентификации: ")
                try:
                    await client.sign_in(password=password)
                except Exception as e:
                    print(f"Ошибка при вводе пароля: {e}")
                    return

    print("Успешный вход!")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
