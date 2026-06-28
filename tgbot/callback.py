import telebot
import base
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(base.TOKEN)
print('bot started')
# -------------------------
# /start command
# -------------------------
@bot.message_handler(commands=['media'])
def start(message):
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("📷 ارسال عکس", callback_data="photo")
    btn2 = InlineKeyboardButton("🎥 ارسال ویدیو", callback_data="video")

    markup.add(btn1, btn2)

    bot.send_message(
        message.chat.id,
        "یکی از گزینه‌ها را انتخاب کن:",
        reply_markup=markup
    )

# -------------------------
# Callback handler
# -------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    bot.answer_callback_query(call.id)

    img_path = []
    # ارسال عکس
    if call.data == "photo":
            bot.send_photo(
                call.message.chat.id,
                photo="https://picsum.photos/600/400",
                caption="📷 این یک عکس نمونه است"
            )

    # ارسال ویدیو
    elif call.data == "video":
        bot.send_video(
            call.message.chat.id,
            video="https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
            caption="🎥 این یک ویدیو نمونه است"
        )

# -------------------------
# run bot
# -------------------------
bot.polling()