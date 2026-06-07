import telebot
import base
import currencly_convertor as cc


bot = telebot.TeleBot(base.TOKEN)

print("bot created")

@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_message(message.chat.id, "Hello, welome to Mew bot.")

@bot.message_handler(commands=['help'])
def send_replay(message):
    bot.reply_to(message, 'If you have any trouble please contact support.' \
    '\nSupport pv: https://t.me/+14248008301')

@bot.message_handler(commands=['news'])
def show_news(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text = 'Sport news', url='https://www.varzesh3.com')
    btn2 = telebot.types.InlineKeyboardButton(text='Daily news', url='https://www.entekhab.ir')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, reply_markup=markup, text= 'Choose what news you want to know')

@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton(text='Contact')
    btn2 = telebot.types.KeyboardButton(text='About')
    btn3 = telebot.types.KeyboardButton(text='Join')
    btn4 = telebot.types.KeyboardButton(text='Back')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, reply_markup=markup, text='Choose one markers')

if __name__ == '__main__':
    bot.infinity_polling()