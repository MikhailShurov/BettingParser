import telebot
from time import sleep


class TeleframClient:
    def __init__(self):
        self.token = '5049347663:AAHrg7oBpxXO_w5oeWaptAINCbkCKNojdYo'
        self.bot = telebot.TeleBot(self.token)

        self.chat_ids = [1140886668]

    def send_screenshots(self):
        with open("poster.png", 'rb') as file:
            self.bot.send_photo(self.chat_ids[0], file)

    def send_text_message(self, message):
        self.bot.send_message(self.chat_ids[0], message)
