import telebot
import base
import currencly_convertor as cc
import requests

bot = telebot.TeleBot(base.TOKEN)

base_currency = ''
target_currency = ''

print('bot Created')

@bot.message_handler(commands=['start'])
def send_message(message):
    first_name = message.from_user.first_name or "Unknown"
    last_name = message.from_user.last_name or ""
    username = message.from_user.username or "Empty"
    user_id = message.from_user.id

    text = (f"Welcome to our bot.\n\n"
            f"Name: {first_name} {last_name}\n"
            f"Username: @{username}\n"
            f"User ID: {user_id}\n\n"
            f"Use /menu to open the main menu.")

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help', 'contact'])
def send_reply(message):
    bot.reply_to(message, f"If you need assistance, please use the Contact Us option from the /menu.\n"
                f"Type / to see all commands")

@bot.message_handler(commands=['news'])
def show_news(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn1 = telebot.types.InlineKeyboardButton(text = 'Sports News' , url='https://varzesh3.com')
    btn2 = telebot.types.InlineKeyboardButton(text='Daily News' , url = 'https://entekhab.ir')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, reply_markup=markup, text = 'Choose one of the options below')


@bot.message_handler(commands=['menu'])
def show_menu(message):
    print('menu')
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton(text = 'Contact Us')
    btn2 = telebot.types.KeyboardButton(text= 'About Us')
    btn3 = telebot.types.KeyboardButton(text= 'Join')
    btn4 = telebot.types.KeyboardButton(text = '⬅️')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, reply_markup=markup, text='Select one of the menu options.')

@bot.message_handler(commands=['convert'])
def convert_currency(message):
    msg = bot.send_message(message.chat.id, 'Enter the base currency')
    bot.register_next_step_handler(msg, get_base_currency)

def get_base_currency(message):
    global base_currency
    base_currency = message.text.upper()
    msg = bot.send_message(message.chat.id, 'Enter the target currency')
    bot.register_next_step_handler(msg, get_target_currency)

def get_target_currency(message):
    global target_currency
    target_currency = message.text.upper()
    rate = cc.exchange_rate(base_currency, target_currency)
    bot.send_message(message.chat.id, f'Exchange rate is: {rate}')


@bot.message_handler(commands=['movieid'])
def movie_by_id(message):
    msg = bot.send_message(message.chat.id, 'Enter the movie ID')
    bot.register_next_step_handler(msg, get_movie_by_id)

def get_movie_by_id(message):
    movie_id = message.text.strip()
    if not movie_id.isdigit():
        bot.send_message(message.chat.id, 'ID must be a number')
        return
    response = requests.get(f'https://moviesapi.ir/api/v1/movies/{movie_id}')
    if response.status_code == 200:
        movie = response.json()
        text = format_movie(movie)
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'No movie found with this ID')


@bot.message_handler(commands=['moviename'])
def movie_by_name(message):
    msg = bot.send_message(message.chat.id, 'Enter the movie name')
    bot.register_next_step_handler(msg, get_movie_by_name)

def get_movie_by_name(message):
    movie_name = message.text.strip()
    response = requests.get(f'https://moviesapi.ir/api/v1/movies', params={'q': movie_name})
    if response.status_code == 200:
        data = response.json()
        
        movies = data.get('data', [])
        
        if not movies:
            bot.send_message(message.chat.id, 'No movie found with this name')
            return
        text = format_movie(movies[0])
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Error retrieving data')


def format_movie(movie):
    title = movie.get('title', 'Unknown')
    year = movie.get('year', 'Unknown')
    rating = movie.get('imdb_rating', 'Unknown')
    plot = movie.get('plot', 'No description available')
    genres = ', '.join(movie.get('genres', [])) or 'Unknown'

    text = f'Title: {title}\nYear: {year}\nGenre: {genres}\nIMDB Rating: {rating}\nPlot: {plot}'
    return text


@bot.message_handler(func=lambda message: True)
def show_info(message):

    if message.text == "Contact Us":

        email = "snowdeveloperDM@gmail.com"
        mobile = "+1 424 800 8301 (Only telegram)"

        info = (f"Contact Information\n\n"
                f"Email: {email}\n"
                f"Phone: {mobile}")
        bot.send_message(message.chat.id, info)

    elif message.text == "About Us":
        about = ("AI Based Company\n\n"
                 "We provide technology and automation solutions.")
        bot.send_message(message.chat.id, about)

    elif message.text == "Join":
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton(text="Join Channel", url="https://t.me/skull_memoris")
        markup.add(btn)
        bot.send_message(message.chat.id, "Join our community:", reply_markup=markup)

    elif message.text == "⬅️":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Main menu closed.", reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()