import telebot
import requests
from confing.confing import WHITELIST, CURRENCY_RATE, ARTICLE_ID

token = "7712321312:AAGTEOW2Yfe1vBFe4s1WpdKN4rr8qn_oEwM"
bot = telebot.TeleBot(token)


def bool_login(chat_id):
    return chat_id in WHITELIST


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if bool_login(message.chat.id):
        bot.reply_to(message, f"Ваш ID: {message.chat.id}")
    else:
        bot.reply_to(message, "Нет доступа")


@bot.message_handler(commands=['info'])
def send_info(message):
    if bool_login(message.chat.id):
        art = ARTICLE_ID
        url = f"https://basket-01.wbbasket.ru/vol{art[0:2]}/part{art[0:4]}/{art}/info/ru/card.json"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "referer": f"https://global.wildberries.ru/catalog/{art}/detail.aspx"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            name = data.get("imt_name", "Название не найдено")
            bot.reply_to(message, name)
        else:
            bot.reply_to(message, f"Ошибка: код {response.status_code}")
    else:
        bot.reply_to(message, "Нет доступа")


@bot.message_handler(commands=['price'])
def analyze_price(message):
    if not bool_login(message.chat.id):
        bot.reply_to(message, "Нет доступа")
        return

    art = ARTICLE_ID
    url = "https://basket-05.wbbasket.ru/vol{art[0:2]}/part{article[0:4]}/{article}/info/price-history.json"
    headers = {
        "user-agent": "Mozilla/5.0",
        "referer": f"https://global.wildberries.ru/catalog/{art}/detail.aspx"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        bot.reply_to(message, f"Ошибка: {response.status_code}")
        return

    data = response.json()

    all_prices = []
    for p in data:
        if "price" in p and "RUB" in p["price"]:
            rub_price = int(p["price"]["RUB"]) / 100
            all_prices.append(rub_price)
            print(p["price"])

    if not all_prices:
        bot.reply_to(message, "Цены не найдены.")
        return

    avg_rub = round(sum(all_prices) / len(all_prices), 2)
    curr_rub = round(all_prices[-1], 2)

    rate = CURRENCY_RATE
    avg_kzt = round(avg_rub * rate, 2)
    curr_kzt = round(curr_rub * rate, 2)
    
    

    if curr_rub > avg_rub:
        status = "Невыгодно"
    elif curr_rub < avg_rub:
        status = "Выгодно"
    else:
        status = "Нейтрально"

    bot.reply_to(
        message,
        f"Cредняя цена: {avg_kzt} Тг\n"
        f"Текущая цена: {curr_kzt} Тг\n"
        f"Анализ: {status}"
    )

@bot.message_handler(commands=['rating'])
def analyze_rating(message):
    if not bool_login(message.chat.id):
        bot.reply_to(message, "Нет доступа")
        return

    art = ARTICLE_ID
    url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=269&spp=30&hide_dtype=13&ab_testing=false&lang=ru&nm={art}"
    headers = {
        "user-agent": "Mozilla/5.0",
        "referer": f"https://global.wildberries.ru/catalog/{art}/detail.aspx"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        bot.reply_to(message, f"Ошибка: {response.status_code}")
        return

    data = response.json()
    product = data["data"]["products"][0]

    rating = float(product.get("reviewRating", 0))
    feedbacks = float(product.get("feedbacks", 1))

    result = rating / feedbacks

    if rating >= 4.5 and feedbacks >= 500:
        status = "Отличный рейтинг"
    elif rating >= 4.0 and feedbacks >= 100:
        status = " Хороший рейтинг"
    elif rating >= 3.5 and feedbacks >= 50:
        status = " Средний рейтинг"
    else:
        status = " Низкий рейтинг"

    bot.reply_to(message,
        f"Рейтинг / отзывов = {result:.10f}\n"
        f"Отзывов: {feedbacks}\n"
        f"Анализ: {status}"
    )

@bot.message_handler(commands=['question'])
def analyze_rating(message):
    if not bool_login(message.chat.id):
        bot.reply_to(message, "Нет доступа")
        return

    art = ARTICLE_ID
    url = f"https://questions.wildberries.ru/api/v1/questions?imtId=124082395&take=10&skip=0"
    headers = {
        "user-agent": "Mozilla/5.0",
        "referer": f"https://global.wildberries.ru/catalog/{art}/detail.aspx"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        bot.reply_to(message, f"Ошибка: {response.status_code}")
        return

    data = response.json()
    
bot.polling()
