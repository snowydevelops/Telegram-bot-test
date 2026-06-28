import telebot

import base

bot  = telebot.TeleBot(base.TOKEN)
print('bot running ... ')

@bot.message_handler(commands=['media'])
def get_message(message):

    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text='نمایش تصویر', 
                                              callback_data='picture')
    btn2 = telebot.types.InlineKeyboardButton(text='نمایش ویدیو',
                                              callback_data='movie')
    
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='یک گزینه را انتخاب کنید', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    
    if call.data == 'picture':
        bot.send_photo(
            call.message.chat.id,
            photo='https://www.blendernation.com/wp-content/uploads/2018/06/A-sunny-living-room.jpg',
            caption='تصویر طبیعت'
        )
    
    elif call.data == 'movie':
        bot.send_video(
            call.message.chat.id,
            video="https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",

            caption='ویدیو منظره'
        )


if __name__ == '__main__':
    bot.infinity_polling()