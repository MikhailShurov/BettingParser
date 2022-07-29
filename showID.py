import telebot

bot = telebot.TeleBot('5555283909:AAEx05bAX-qQC-z_ebgDLLPPKN1xVdvrpL4')


@bot.message_handler(content_types=["text"])
def show_id(message):
    print(message.chat.id)

bot.infinity_polling()