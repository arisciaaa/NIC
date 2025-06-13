import json
import gspread
import time

# Аутентификация
gc = gspread.service_account(filename='gothic-avenue-448113-b0-7492d09b94a7.json')

# Открытие Google Таблицы и выбор листа
sh = gc.open('НИС - проект')
worksheet = sh.worksheet("row_data")

# Загрузка содержимого файла JSON
with open('shot_posts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Очистка листа перед загрузкой
worksheet.clear()

# Заголовки таблицы
headers = [["ID", "Дата", "Текст", "Просмотры", "Реакции", "Ответы", "Форварды", "Ссылки"]]
worksheet.update('A1:H1', headers)

# Начинаем запись с 2-й строки
row_index = 2

# Заголовки
headers = [["ID", "Дата", "Текст", "Просмотры", "Реакции", "Ответы", "Форварды", "Ссылки"]]
worksheet.update(values=headers, range_name='A1:H1')

# Начинаем со второй строки (первая — заголовки)
row_index = 2

for post in data:
    # 👉 Пропускаем посты без реакций
    if post.get("reactions") is None:
        print(f"⏩ Пропущен пост ID {post.get('id')} — нет реакций")
        continue

    # Безопасный текст
    text = post.get("text", "")
    if not isinstance(text, str):
        text = ""
    text = text.replace("\n", " ")

    # Безопасные ссылки
    links = post.get("links", [])
    if not isinstance(links, list):
        links = []
    joined_links = ", ".join(links)

    # Сбор строки
    row = [
        post.get("id", ""),
        post.get("date", ""),
        text,
        post.get("views", ""),
        json.dumps(post.get("reactions", {}), ensure_ascii=False),
        post.get("replies_count", ""),
        post.get("forwards", ""),
        joined_links
    ]

    # Запись строки
    worksheet.update(values=[row], range_name=f"A{row_index}:H{row_index}")
    print(f"✅ Записан пост ID {post.get('id')} в строку {row_index}")
    row_index += 1
    time.sleep(1)

print("🎉 Все посты записаны в Google Таблицу!")
