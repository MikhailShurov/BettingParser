import json
import requests

import time as tm
from time import sleep
from time import localtime

import TelegramClient

from threading import *

import schedule

from math import floor
from rich.console import Console
from rich.traceback import install

install()
console = Console(record=True)


class LineParser:
    def __init__(self):
        self.tk = TelegramClient.TeleframClient()
        self.used_ids = []

    def clear_used_ids(self):
        self.used_ids = []

    def check_id(self, match_id):
        try:
            response = requests.get(f'https://melbet.ru/LineFeed/GetGameZip?id={match_id}&partner=195')
            response = json.loads(response.text)

            for item in range(len(response["Value"]["E"])):
                try:
                    if response["Value"]["E"][item]["G"] == 309:
                        total15 = float(response["Value"]["E"][item]["C"])
                        total30 = float(response["Value"]["E"][item+1]["C"])
                        print(total15, total30)
                        if 2.0 <= total15 <= 2.6 and 1.4 <= total30 <= 1.55:
                            return True
                        else:
                            return False
                except:
                    continue

            return False
        except:
            return False

    def infinity_parsing(self):

        response = requests.get('https://melbet.ru/LineFeed/Get1x2_VZip?sports=1&count=200&tf=60&mode=4&cyberFlag=4&partner=195')
        response = json.loads(response.text)

        for item in range(len(response["Value"])):
            unix_time = int(response["Value"][item]["S"])
            if 480 <= abs(unix_time - int(tm.time())) <= 660:
                match_id = int(response["Value"][item]["LI"])
                print([match_id, unix_time, response["Value"][item]["L"], response["Value"][item]["O1"], response["Value"][item]["O2"]])
                if self.check_id(match_id) and match_id not in self.used_ids:
                    time_hour = int(localtime(int(unix_time)).tm_hour)
                    time_hour = (time_hour + 3) % 24
                    time_min = int(localtime(int(unix_time)).tm_min)
                    mod_time_hour, mod_time_min = str(time_hour), str(time_min)
                    if len(str(time_hour)) == 1:
                        mod_time_hour = f'0{time_hour}'
                    if len(str(time_min)) == 1:
                        mod_time_min = f'0{time_min}'

                    message = f'''⚽️Лига: {response["Value"][item]["L"]}
        
🏆Команды: {response["Value"][item]["O1"]} - {response["Value"][item]["O2"]}
        
☑️Настоящий я: @ESPANSEO
        
⏰Начало матча: {mod_time_hour}:{mod_time_min} (МСК)
        
💰Прогноз: гол до 30 минуты или ТБ 0.5 в первом тайме'''

                    self.used_ids.append(match_id)
                    chat_message_id = self.tk.send_text_message(message)
                    chanel_message_id = self.tk.send_message_to_chanel(message)

                    t1 = Thread(target=self.check_stats, args=(match_id, chat_message_id, chanel_message_id, message, localtime().tm_hour))
                    t1.start()
                else:
                    continue
            else:
                print(f'Ждать {int((unix_time - tm.time())/60)} минут')

    def check_stats(self, track_id, chat_id, chanel_id, message_text, start):

        while True:
            sleep(3)
            if start + 2 == localtime().tm_hour:
                break
            try:
                response = requests.get(f'https://melbet.ru/LiveFeed/GetGameZip?id={track_id}&partner=195')
                response = json.loads(response.text)
                timer = int(response["Value"]["SC"]["TS"])
                if timer >= 1800:
                    print('Время вышло...')
                    add = '\n\n❌❌❌❌❌'
                    self.tk.edit_message_in_chat_with(chat_id, message_text, add)
                    self.tk.edit_message_in_chanel_with(chanel_id, message_text, add)
                    break
                elif timer <= 1800:
                    print('проверяю гол')
                    try:
                        if len(response["Value"]["SC"]["PS"][0]["Value"]) != 0:
                            add = f'\n\n✅✅✅✅✅ {floor(timer/60)}-я минута'
                            self.tk.edit_message_in_chat_with(chat_id, message_text, add)
                            self.tk.edit_message_in_chanel_with(chanel_id, message_text, add)
                            break
                    except:
                        print('Hmmm, something went wrong...')
                        continue
            except:
                print('Всё хорошо')
                sleep(10)
                continue


if __name__ == '__main__':
    lp = LineParser()
    schedule.every(2).hours.do(lp.clear_used_ids)
    while True:
        schedule.run_pending()
        lp.infinity_parsing()
        print('**************************************************')
        sleep(6)

