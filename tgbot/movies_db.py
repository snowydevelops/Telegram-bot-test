import telebot
import base
import currencly_convertor as cc
import requests

bot = telebot.TeleBot(base.TOKEN)

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