# import telebot
#
# bot = telebot.TeleBot('5555283909:AAEx05bAX-qQC-z_ebgDLLPPKN1xVdvrpL4')
#
#
# @bot.message_handler(content_types=["text"])
# def show_id(message):
#     print(message.chat.id)
#
# bot.infinity_polling()


from threading import *
from time import sleep


def mentor(word):
    for i in range(30):
        print(word, i)
        sleep(1)


def print_num(word):
    t1 = Thread(target=mentor, args=(word,))
    t1.start()


while True:
    print_num("bumbum")
    sleep(3)
