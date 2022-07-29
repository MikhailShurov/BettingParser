import telebot


class TeleframClient:
    def __init__(self):
        self.token = '5555283909:AAEx05bAX-qQC-z_ebgDLLPPKN1xVdvrpL4'
        self.bot = telebot.TeleBot(self.token)

        self.chat_ids = [1140886668, 958571682]

    def send_screenshots(self):
        with open("poster.png", 'rb') as file:
            self.bot.send_photo(self.chat_ids[0], file)

    def send_text_message(self, message):
        self.bot.send_message(self.chat_ids[0], message)

    def send_text_message_for_all(self, message):
        for c_id in self.chat_ids:
            self.bot.send_message(c_id, message)
