import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = telebot.TeleBot(BOT_TOKEN)

# FAQ данные для базы отдыха "Пеликан" на озере Алаколь
FAQ = {
    "🏨 Заезд и выезд": {
        "text": "🏨 <b>Время заезда и выезда</b>\n\n"
               "📥 <b>Заезд (Check-in):</b> с 11:00\n"
               "📤 <b>Выезд (Check-out):</b> до 9:00\n\n"
               "⏰ <b>Важно:</b>\n"
               "• При размещении до 11:00 - оплата за полсуток (при наличии номера)\n"
               "• При выезде после 9:00 - оплата по договорённости\n\n"
               "📋 <b>Для заселения нужны:</b>\n"
               "• Паспорт или удостоверение личности\n"
               "• Заполнить анкету гостя\n"
               "• Внести депозит 5 000 тенге (возвратный)\n\n"
               "🎫 <b>Браслет гостя:</b>\n"
               "При заселении выдаётся контрольный браслет для:\n"
               "• Бесплатного проезда на пароме до косы\n"
               "• Контроля в столовой\n"
               "• Бесплатного купания в бассейне (дети)",
        "emoji": "🏨"
    },
    "💳 Оплата и бронь": {
        "text": "💳 <b>Оплата и бронирование</b>\n\n"
               "💰 <b>Способы оплаты:</b>\n"
               "✅ Наличные тенге при заселении\n"
               "✅ Безналичный расчет (по договорённости)\n\n"
               "🔒 <b>Депозит:</b>\n"
               "При заселении вносится 5 000 тенге возвратный залог\n"
               "Возвращается при выезде, если номер сдан без ущерба\n\n"
               "💸 <b>Скидки при раннем бронировании:</b>\n\n"
               "<b>При 100% предоплате:</b>\n"
               "• 10.06 - 16.06 и 18.08 - 01.09: скидка 8%\n"
               "• 16.06 - 18.08 (высокий сезон): скидка 5%\n\n"
               "<b>При предоплате от 40%:</b>\n"
               "• 10.06 - 16.06 и 18.08 - 01.09: скидка 5%\n\n"
               "📞 <b>Контакты для бронирования:</b>\n"
               "WhatsApp: +7 776 756 00 89\n"
               "Телефоны: +7 (727) 275-00-89, +7 (727) 275-38-76",
        "emoji": "💳"
    },
    # ... все остальные разделы как в вашем оригинальном словаре FAQ ...
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for question in FAQ.keys():
        markup.add(types.InlineKeyboardButton(question, callback_data=f"faq_{question}"))
    bot.send_message(
        message.chat.id,
        f"👋 <b>Добро пожаловать в ЦСО «Пеликан»!</b>\n\n"
        f"Здравствуйте, {message.from_user.first_name}! 🌊\n\n"
        "🏖️ База отдыха «Пеликан» на озере Алаколь\n"
        "🌳 Самая зелёная база с более 5000 деревьев\n"
        "🏡 Уютные деревянные домики\n"
        "👨‍👩‍👧 Идеально для семейного отдыха\n\n"
        "Выберите интересующий раздел ⬇️",
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('faq_'))
def callback_faq(call):
    question = call.data[4:]  # убираем префикс "faq_"
    if question in FAQ:
        answer_data = FAQ[question]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("◀️ Назад к вопросам", callback_data="back"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=answer_data["text"],
            reply_markup=markup,
            parse_mode='HTML'
        )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back")
def callback_back(call):
    bot.answer_callback_query(call.id, "Возвращаюсь к вопросам...")
    start(call.message)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📖 <b>Помощь</b>\n\n"
        "• Используйте кнопки для выбора раздела\n"
        "• /start - вернуться в главное меню\n"
        "• /help - показать эту справку\n\n"
        "📞 <b>Контакты для бронирования:</b>\n"
        "WhatsApp: +7 776 756 00 89\n"
        "Телефон: +7 (727) 275-00-89\n"
        "Телефон: +7 (727) 275-38-76\n\n"
        "🌐 Сайт: pelican-alacol.ru",
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda message: True)
def fallback(message):
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
    print("🤖 Бот «Пеликан Алаколь» запущен и готов к работе...")
    print(f"📝 Загружено {len(FAQ)} FAQ разделов")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Перезапуск через 5 секунд...")
        import time
        time.sleep(5)
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
