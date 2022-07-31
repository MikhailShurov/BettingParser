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
import asyncio
from time import sleep


async def print_num(num):
    while True:
        print(num)
        await asyncio.sleep(2)

async def main():
    await asyncio.run(print_num(5))
    await asyncio.run(print_num(6))
asyncio.run(main())
