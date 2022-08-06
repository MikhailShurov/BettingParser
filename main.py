from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep
from time import localtime

import TelegramClient

import schedule

from threading import *

from rich.console import Console
from rich.traceback import install

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
                time = item.find_element(By.CLASS_NAME, 'kofsTableLineNums').find_element(By.CLASS_NAME, 'dateCon').find_element(By.TAG_NAME, 'span').text
                cur_hour, cur_min = int(time[:time.index(':')]), int(time[time.index(':') + 1:])
                print(f'Ещё ждать {cur_hour * 60 + cur_min - localtime().tm_hour * 60 - localtime().tm_min}')
                if 8 <= cur_hour * 60 + cur_min - localtime().tm_hour * 60 - localtime().tm_min <= 11:
                    link = item.find_element(By.CLASS_NAME, 'kofsTableLineNums').find_element(By.TAG_NAME, 'a').get_attribute('href')
                    response = self.check_link(link)
                    if response[0] and link not in self.used_links:
                        cur_hour = (cur_hour + 3) % 24
                        cur_hour_str = f'{cur_hour}'
                        cur_min_str = f'{cur_min}'
                        if len(str(cur_hour)) == 1:
                            cur_hour_str = f'0{cur_hour}'
                        if len(str(cur_min)) == 1:
                            cur_min_str = f'0{cur_min}'
                        message = f'''⚽️Лига: {response[1]}
    
🏆Команды: {response[2]}
    
☑️Настоящий я: @ESPANSEO
    
⏰Начало матча: {cur_hour_str}:{cur_min_str} (МСК)
    
💰Прогноз: гол до 30 минуты или ТБ 0.5 в первом тайме'''
                        msg = self.tk.send_text_message_for_all(message)
                        msg.append(message)
                        self.used_links.append(link)
                        t1 = Thread(target=LineParser().check_stats, args=(link, cur_min, cur_hour, msg, message))
                        t1.start()
        except Exception as ex:
            # Улетает в except тк не во всех матчах есть вкладка "Интервалы"
            print(ex)

    def check_stats(self, link, start_min, start_hour, ids, message_text):
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)

        mod_link = f'{link[:link.index("line")]}live{link[link.index("line") + 4:]}'

        self.tk.send_text_message(f'''Трекаю матч, его url: {mod_link}''')

        self.driver.get(mod_link)
        sleep(5)

        while True:
            print('В потоке')
            try:
                if start_hour * 60 + start_min - localtime().tm_hour * 60 - localtime().tm_min > 0:
                    print('Жду-с')
                    sleep(5)
                    continue
                elif localtime().tm_hour * 60 + localtime().tm_min - start_hour * 60 - start_min >= 30:
                    self.tk.send_text_message(f'''Закончил трекать этот матч, выхожу

{mod_link}''')
                    print('Вышло время...')
                    return
                elif 0 <= localtime().tm_hour * 60 + localtime().tm_min - start_hour * 60 - start_min <= 30:
                    sleep(10)
                    self.driver.save_screenshot('lol.png')
                    self.tk.send_screenshots()
                    try:
                        print('Пошла жара')
                        try:
                            print(self.driver.find_element(By.ID, 'scoreboard__time').text)
                        except:
                            print('Не вижу время')
                        left_score = int(self.driver.find_element(By.ID, 'scoreboard__score_left').text)
                        right_score = int(self.driver.find_element(By.ID, 'scoreboard__score_right').text)
                        if left_score + right_score != 0:
                            self.tk.edit_text_message_for_all(ids, localtime().tm_min, message_text)
                            self.tk.send_text_message('Edited')
                            print('Завершаю поток...')
                            return
                        else:
                            print('Пока по нулям')
                    except:
                        print('Hmmm, something went wrong...')
                        continue
            except:
                self.tk.send_text_message('Главный except')
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
            sleep(30)
        TelegramClient.TeleframClient().send_text_message('Cкрипт фулл вылетел')
    except:
        console.save_html("error.html")
        TelegramClient.TeleframClient().send_error()
