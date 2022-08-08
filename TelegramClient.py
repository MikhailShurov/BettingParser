import json

import telebot
import requests


class TeleframClient:
    def __init__(self):
        self.token = '5555283909:AAEx05bAX-qQC-z_ebgDLLPPKN1xVdvrpL4'
        self.bot = telebot.TeleBot(self.token)

        self.chat_ids = [1140886668]

    # def send_screenshots(self):
    #     with open("lol.png", 'rb') as file:
    #         self.bot.send_photo(self.chat_ids[0], file)

    # def send_error(self):
    #     with open("error.html", 'rb') as file:
    #         self.bot.send_document(self.chat_ids[0], file)

    def send_text_message(self, message):
        msg = self.bot.send_message(self.chat_ids[0], message)
        return msg.message_id

    def send_message_to_chanel(self, message):
        method = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id=-1001732681694&text={message}"
        response = requests.post(method)
        resp = json.loads(response.text)
        return resp["result"]["message_id"]

    def edit_message_in_chat_with(self, message_id, message_text, add):
        self.bot.edit_message_text(chat_id=self.chat_ids[0], message_id=message_id, text=message_text + add)

    def edit_message_in_chanel_with(self, message_id, message_text, add):
        self.bot.edit_message_text(chat_id=-1001732681694, message_id=message_id, text=message_text + add)
