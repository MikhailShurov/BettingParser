import json

import telebot
import requests
import data


class TeleframClient:
    def __init__(self):
        self.token = data.bot_token
        self.bot = telebot.TeleBot(self.token)

        self.chat_ids = data.chat_ids

    def send_text_message(self, message):
        msg = self.bot.send_message(self.chat_ids[0], message)
        return msg.message_id

    def send_message_to_chanel(self, message):
        method = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={data.group_id}&text={message}"
        response = requests.post(method)
        resp = json.loads(response.text)
        return resp["result"]["message_id"]

    def edit_message_in_chat_with(self, message_id, message_text, add):
        self.bot.edit_message_text(chat_id=self.chat_ids[0], message_id=message_id, text=message_text + add)

    def edit_message_in_chanel_with(self, message_id, message_text, add):
        self.bot.edit_message_text(chat_id=data.group_id, message_id=message_id, text=message_text + add)
