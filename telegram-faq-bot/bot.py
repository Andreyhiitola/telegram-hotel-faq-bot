import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = telebot.TeleBot(BOT_TOKEN)

FAQ = {
    "⏰ Часы работы": {
        "text": "🕐 <b>Часы работы</b>\n\nМы работаем ежедневно:\n• Пн-Пт: 9:00 - 21:00\n• Сб-Вс: 10:00 - 20:00",
        "emoji": "⏰"
    },
    "📞 Контакты": {
        "text": "📞 <b>Как с нами связаться</b>\n\n• Email: support@example.com\n• Телефон: +7 (xxx) xxx-xx-xx\n• Telegram: @support_username\n• Адрес: г. Москва, ул. Примерная, д. 1",
        "emoji": "📞"
    },
    "💳 Способы оплаты": {
        "text": "💳 <b>Способы оплаты</b>\n\n✅ Банковские карты (Visa, MasterCard, Мир)\n✅ Наличные при получении\n✅ СБП (Система быстрых платежей)\n✅ Электронные кошельки\n✅ Безналичный расчет для юр. лиц",
        "emoji": "💳"
    },
    "🚚 Доставка": {
        "text": "🚚 <b>Условия доставки</b>\n\n• Москва: 1-2 дня, от 300₽\n• Московская область: 2-3 дня, от 500₽\n• Россия: 3-7 дней, от 500₽\n\n🎁 Бесплатная доставка от 3000₽",
        "emoji": "🚚"
    },
    "ℹ️ О компании": {
        "text": "ℹ️ <b>О нашей компании</b>\n\n🏢 Мы работаем на рынке с 2010 года\n👥 Более 50 000 довольных клиентов\n⭐ Рейтинг 4.8/5.0\n🏆 Лучший сервис 2024 года\n\n📝 ИНН: 1234567890\nОГРН: 1234567890123",
        "emoji": "ℹ️"
    },
    "❓ Частые вопросы": {
        "text": "❓ <b>Часто задаваемые вопросы</b>\n\n<b>Можно ли вернуть товар?</b>\nДа, в течение 14 дней.\n\n<b>Есть ли гарантия?</b>\nДа, официальная гарантия от производителя.\n\n<b>Как отследить заказ?</b>\nВы получите трек-номер на email.",
        "emoji": "❓"
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for question in FAQ.keys():
        buttons.append(types.KeyboardButton(question))
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i + 1])
        else:
            markup.row(buttons[i])
    markup.row(types.KeyboardButton("🔄 Главное меню"))
    bot.send_message(
        message.chat.id,
        f"👋 <b>Привет, {message.from_user.first_name}!</b>\n\n"
        "Я FAQ-бот компании. Выберите интересующий раздел:\n\n"
        "Используйте кнопки ниже для быстрой навигации ⬇️",
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📖 <b>Помощь</b>\n\n"
        "• Используйте кнопки для выбора раздела\n"
        "• /start - вернуться в главное меню\n"
        "• /help - показать эту справку\n\n"
        "💬 Если не нашли ответ, напишите нам:\n"
        "support@example.com",
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda message: message.text == "🔄 Главное меню")
def main_menu(message):
    start(message)

@bot.message_handler(func=lambda message: message.text in FAQ.keys())
def handle_faq(message):
    question = message.text
    answer_data = FAQ[question]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад к вопросам", callback_data="back"))
    bot.send_message(
        message.chat.id,
        answer_data["text"],
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data == "back")
def callback_back(call):
    bot.answer_callback_query(call.id, "Возвращаюсь к вопросам...")
    start(call.message)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📋 Показать меню", callback_data="show_menu"))
    bot.send_message(
        message.chat.id,
        "🤔 Не понимаю вашего вопроса.\n\n"
        "Пожалуйста, используйте кнопки меню ниже или нажмите на кнопку:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "show_menu")
def callback_menu(call):
    bot.answer_callback_query(call.id)
    start(call.message)

if __name__ == '__main__':
    print("🤖 Бот запущен и готов к работе...")
    print(f"📝 Загружено {len(FAQ)} FAQ разделов")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Перезапуск через 5 секунд...")
        import time
        time.sleep(5)
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
