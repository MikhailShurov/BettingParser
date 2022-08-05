import telebot
import time

bot = telebot.TeleBot('5555283909:AAEx05bAX-qQC-z_ebgDLLPPKN1xVdvrpL4')

msg = bot.send_message(1140886668, 'loool')
time.sleep(5)
add = '\n\nlooooooooool'
bot.edit_message_text(chat_id=1140886668, message_id=msg.message_id, text=msg.text + add)


# from threading import *
# from time import sleep
#
#
# def mentor(word):
#     for i in range(30):
#         print(word, i)
#         sleep(1)
#
#
# def print_num(word):
#     t1 = Thread(target=mentor, args=(word,))
#     t1.start()
#
#
# while True:
#     print_num("bumbum")
#     sleep(3)
