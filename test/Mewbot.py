import telebot
import base
import convert_currency as cc

bot = telebot.TeleBot(base.TOKEN)

base_currency = ''
target_currency = ''

print("The bot started working.")


@bot.message_handler(commands=['start'])
def send_message(message):
    first_name = message.from_user.first_name or "Unknown"
    last_name = message.from_user.last_name or ""
    username = message.from_user.username or "Empty"
    user_id = message.from_user.id

    text = (
        f"Welcome to our bot.\n\n"
        f"Name: {first_name} {last_name}\n"
        f"Username: @{username}\n"
        f"User ID: {user_id}\n\n"
        f"Use /menu to open the main menu."
    )

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help', 'contact'])
def send_reply(message):
    bot.reply_to(
        message,
        f"If you need assistance, please use the Contact Us option from the /menu.\n"
        f"Type / to see all commands"
    )


@bot.message_handler(commands=['news'])
def show_news(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    btn1 = telebot.types.InlineKeyboardButton(
        text="Sports News",
        url="https://www.varzesh3.com"
    )

    btn2 = telebot.types.InlineKeyboardButton(
        text="Daily News",
        url="https://www.entekhab.ir"
    )

    markup.add(btn1, btn2)

    bot.send_message(
        message.chat.id,
        "Choose a news source:",
        reply_markup=markup
    )


@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    btn1 = telebot.types.KeyboardButton("Contact Us")
    btn2 = telebot.types.KeyboardButton("About Us")
    btn3 = telebot.types.KeyboardButton("Join")
    btn4 = telebot.types.KeyboardButton("Back")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Select an option:",
        reply_markup=markup
    )


@bot.message_handler(commands=['convert'])
def convert_currency(message):
    msg = bot.send_message(
        message.chat.id,
        "Enter the base currency code (Example: USD)"
    )

    bot.register_next_step_handler(
        msg,
        get_base_currency
    )


def get_base_currency(message):
    global base_currency

    base_currency = message.text.upper()

    msg = bot.send_message(
        message.chat.id,
        "Enter the target currency code (Example: EUR)"
    )

    bot.register_next_step_handler(
        msg,
        get_target_currency
    )


def get_target_currency(message):
    global target_currency

    target_currency = message.text.upper()

    try:
        rate = cc.exchange_rate(
            base_currency,
            target_currency
        )

        bot.send_message(
            message.chat.id,
            f"Exchange Rate\n\n1 {base_currency} = {rate} {target_currency}"
        )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"Error: {e}"
        )


@bot.message_handler(func=lambda message: True)
def show_info(message):

    if message.text == "Contact Us":

        email = "snowdeveloperDM@gmail.com"
        mobile = "+1 424 800 8301 (Only telegram)"

        info = (
            f"Contact Information\n\n"
            f"Email: {email}\n"
            f"Phone: {mobile}"
        )

        bot.send_message(
            message.chat.id,
            info
        )

    elif message.text == "About Us":

        about = (
            "AI Based Company\n\n"
            "We provide technology and automation solutions."
        )

        bot.send_message(
            message.chat.id,
            about
        )

    elif message.text == "Join":

        markup = telebot.types.InlineKeyboardMarkup()

        btn = telebot.types.InlineKeyboardButton(
        text="Join Channel",
        url="https://t.me/skull_memoris"
        )

        markup.add(btn)

        bot.send_message(
        message.chat.id,
        "Join our community::",
        reply_markup=markup
        )

    elif message.text == "Back":

        markup = telebot.types.ReplyKeyboardRemove()

        bot.send_message(
            message.chat.id,
            "Main menu closed.",
            reply_markup=markup
        )


if __name__ == '__main__':
    bot.infinity_polling()