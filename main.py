import requests
import schedule
import time
from pymongo import MongoClient
from install import BOT_TOKEN, CHAT_IDS, MONGO_URI, DB_NAME, COLLECTION_NAME




# Функция для отправки сообщений в Telegram
def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.get(telegram_url, params=params)
        if response.status_code == 200:
            print("Сообщение успешно отправлено в Telegram")
        else:
            print(f"Ошибка при отправке сообщения в Telegram: {response.status_code}, {response.text}")

# Функция для выполнения GET запроса с данными из MongoDB
def send_get_request():
    # Подключаемся к MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Забираем все данные из коллекции
    data = collection.find()
    
    # Проходим по всем записям из коллекции и отправляем GET запрос
    for record in data:
        # Пример: подставляем данные из записи в GET запрос (вы можете изменить под ваши нужды)
        pixel = {
            "pixel": str(record.get("number", "")).replace(".0", ""),
            "token": record.get("token", ""),
            # Добавьте другие параметры, которые нужно передать в запрос
        }
        FACEBOOK_URL = f"https://graph.facebook.com/v19.0/{pixel['pixel']}?access_token={pixel['token']}"

        print(FACEBOOK_URL)

        # Выполняем GET запрос
        response = requests.get(FACEBOOK_URL)

        # Обрабатываем результат запроса
        if response.status_code == 200:
            print(f"Запрос успешен: {response.json()}")
        else:
            error_message = f"Ошибка при выполнении запроса: {response.status_code}, {response.text}"
            print(error_message)
            # Отправляем сообщение в Telegram
            send_telegram_message(f"Номер пикселя: {pixel['pixel']}\nОшибка запроса: {response.status_code}.\nТекст ошибки: {response.text}")

    # Закрываем подключение к базе
    client.close()


schedule.every(24).hours.do(send_get_request)


# Бесконечный цикл для запуска планировщика
while True:
    schedule.run_pending()
    time.sleep(1)
