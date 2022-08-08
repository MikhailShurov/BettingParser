import json
import requests

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep
from time import localtime

import TelegramClient

from threading import *

import schedule

from rich.console import Console
from rich.traceback import install

from math import floor

install()
console = Console(record=True)


class LineParser:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument(f'user-agent={user_agent}')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--ignore-certificate-errors')

        self.tk = TelegramClient.TeleframClient()

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)
        self.used_links = []

        self.headers = {
            "Cookie": "SESSION=66e05adcbc32c62291caf2569e6531b1; lng=ru; auid=F2nvfGLiv0em05QCMXiHAg==; _ga=GA1.1.352226497.1659027273; tzo=3; sh.session=abb29fc3-7fe3-454f-bb7f-a614b23a6b42; geocountry=ca; _ga_X2B11TMFNG=GS1.1.1659951299.42.1.1659951390.0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }

    def clear_used_links(self):
        self.used_links = []

    def visit_site_and_setup_timefiltr(self):
        try:
            self.browser.get('https://melbet.ru/line/football/')
            sleep(5)
            time_filtr = self.browser.find_element(By.ID, 'timeFiltr')
            time_filtr.click()
            select = Select(time_filtr)
            select.select_by_value("60")
            time_filtr.click()
            sleep(5)
            return True
        except Exception as ex:
            print(ex)
            return False

    def show_league(self, link):
        try:
            mod_link = link[:link.rfind('/') + 1]
            self.browser.execute_script("window.open('');")
            self.windows = self.browser.window_handles
            self.browser.switch_to.window(self.windows[-1])
            self.browser.get(mod_link)
            sleep(3)
            league = self.browser.find_element(By.ID, 'h1').text
            self.browser.close()
            self.windows = self.browser.window_handles
            self.browser.switch_to.window(self.windows[-1])
            return league
        except Exception as ex:
            print(ex)
            return 'не удалось найти лигу'

    def check_link(self, link):
        self.browser.execute_script("window.open('');")
        self.windows = self.browser.window_handles
        self.browser.switch_to.window(self.windows[-1])
        self.browser.get(link)
        sleep(3)
        try:
            cells = self.browser.find_element(By.ID, 'group_309').find_element(By.ID, 's_309').find_elements(By.ID, 'z_1197')
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", cells[0])
            f_val = cells[0].find_elements(By.TAG_NAME, 'span')[-1].text
            s_val = cells[1].find_elements(By.TAG_NAME, 'span')[-1].text
            teams = self.browser.find_element(By.ID, 'h1').text
            if 2.0 < float(f_val) < 2.6 and 1.4 < float(s_val) < 1.55:
                self.browser.close()
                self.windows = self.browser.window_handles
                self.browser.switch_to.window(self.windows[-1])
                league = self.show_league(link[:-2])
                return [True, league, teams]
        except:
            self.browser.close()
            self.windows = self.browser.window_handles
            self.browser.switch_to.window(self.windows[-1])
            return [False]
        return [False]

    def infinity_parsing(self):
        try:
            try:
                group = self.browser.find_element(By.ID, 'line_bets_on_main')
                matches = group.find_elements(By.CLASS_NAME, 'kofsTableBody')
            except:
                matches = self.browser.find_elements(By.CLASS_NAME, 'kofsTableBody')
            for item in matches:
                try:
                    time = item.find_element(By.CLASS_NAME, 'kofsTableLineNums').find_element(By.CLASS_NAME, 'dateCon').find_element(By.TAG_NAME, 'span').text
                    cur_hour, cur_min = int(time[:time.index(':')]), int(time[time.index(':') + 1:])
                    print(f'Ещё ждать {cur_hour * 60 + cur_min - localtime().tm_hour * 60 - localtime().tm_min}')
                    if 8 <= cur_hour * 60 + cur_min - localtime().tm_hour * 60 - localtime().tm_min <= 11:
                        link = item.find_element(By.CLASS_NAME, 'kofsTableLineNums').find_element(By.TAG_NAME, 'a').get_attribute('href')
                        response = self.check_link(link)
                        if response[0] and link not in self.used_links:
                            cur_hour_str = f'{(cur_hour + 3) % 24}'
                            cur_min_str = f'{cur_min}'
                            if len(str((cur_hour + 3) % 24)) == 1:
                                cur_hour_str = f'0{(cur_hour + 3) % 24}'
                            if len(str(cur_min)) == 1:
                                cur_min_str = f'0{cur_min}'
                            message = f'''⚽️Лига: {response[1]}
        
🏆Команды: {response[2]}
        
☑️Настоящий я: @ESPANSEO
        
⏰Начало матча: {cur_hour_str}:{cur_min_str} (МСК)
        
💰Прогноз: гол до 30 минуты или ТБ 0.5 в первом тайме'''
                            self.used_links.append(link)

                            chat_message_id = self.tk.send_text_message(message)
                            chanel_message_id = self.tk.send_message_to_chanel(message)

                            t1 = Thread(target=self.check_stats, args=(link, chat_message_id, chanel_message_id, message, localtime().tm_hour))
                            t1.start()
                except:
                    continue
        except Exception as ex:
            # Улетает в except тк не во всех матчах есть вкладка "Интервалы"
            print(ex)

    def check_stats(self, link, chat_id, chanel_id, message_text, start):

        link = link[:-1]
        track_id = int(link[link.rfind('/')+1:link.index('-', link.rfind('/')+1)])

        while True:
            sleep(3)
            if start + 2 == localtime().tm_hour:
                break
            try:
                response = requests.get(f'https://melbet.ru/LiveFeed/GetGameZip?id={track_id}&partner=195')
                response = json.loads(response.text)
                timer = int(response["Value"]["SC"]["TS"])
                if timer >= 1800:
                    print('Вышло время...')
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
    try:
        lp = LineParser()
        schedule.every(2).hours.do(lp.clear_used_links)
        while True:
            schedule.run_pending()
            resp = lp.visit_site_and_setup_timefiltr()
            if not resp:
                continue
            lp.infinity_parsing()
            print('**************************************************')
            sleep(6)
    except:
        print('jj')
