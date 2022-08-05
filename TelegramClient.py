import telebot


class TeleframClient:
    def __init__(self):
        self.token = '5555283909:AAEx05bAX-qQC-z_ebgDLLPPKN1xVdvrpL4'
        self.bot = telebot.TeleBot(self.token)

        self.chat_ids = [1140886668, 958571682]

    def send_screenshots(self):
        with open("lol.png", 'rb') as file:
            self.bot.send_photo(self.chat_ids[0], file)

    def send_error(self):
        with open("error.html", 'rb') as file:
            self.bot.send_document(self.chat_ids[0], file)

    def send_text_message(self, message):
        self.bot.send_message(self.chat_ids[0], message)

    def send_text_message_for_all(self, message):
        ret = []
        for c_id in self.chat_ids:
            answ = self.bot.send_message(c_id, message)
            ret.append([c_id, answ.message_id])
        return ret

    def edit_text_message_for_all(self, message, goal_time, message_text):
        add = f'\n\n✅✅✅ {goal_time}'
        for pair in message:
            self.bot.edit_message_text(chat_id=pair[0], message_id=pair[1], text=message_text + add)
