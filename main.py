from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep
from time import localtime

import TelegramClient


class LineParser:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')

        self.tk = TelegramClient.TeleframClient()

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def visit_site_and_setup_timefiltr(self):       # Полностью работает
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

    def check_link(self, link):
        self.browser.execute_script("window.open('');")
        self.windows = self.browser.window_handles
        self.browser.switch_to.window(self.windows[-1])
        self.browser.get(f'https://melbet.ru/{link}')

        self.tk.send_text_message('Матч:')
        self.browser.save_screenshot('poster.png')
        TelegramClient.TeleframClient().send_screenshots()

        sleep(3)
        buttons = self.browser.find_elements(By.CLASS_NAME, 'markets__item-wrap')
        for item in buttons:
            if item.find_element(By.TAG_NAME, 'a').text.strip(' ') == 'Интервалы':
                try:
                    item.find_element(By.TAG_NAME, 'span').click()
                    sleep(2)
                    cells = self.browser.find_element(By.ID, 'group_309').find_element(By.ID, 's_309').find_elements(By.ID, 'z_1197')
                    self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", cells[0])
                    f_val = cells[0].find_elements(By.TAG_NAME, 'span')[-1].text
                    s_val = cells[1].find_elements(By.TAG_NAME, 'span')[-1].text

                    if 2.0 < float(f_val) < 2.6 and 1.4 < float(s_val) < 1.55:
                        self.windows = self.browser.window_handles
                        self.browser.switch_to.window(self.windows[-1])
                        return True
                except:
                    self.windows = self.browser.window_handles
                    self.browser.switch_to.window(self.windows[-1])
                    return False
        self.windows = self.browser.window_handles
        self.browser.switch_to.window(self.windows[-1])
        return False

    def infinity_parsing(self):
        matches = self.browser.find_elements(By.CLASS_NAME, 'kofsTableBody')
        for item in matches:
            time = item.find_element(By.CLASS_NAME, 'kofsTableLineNums').find_element(By.CLASS_NAME, 'dateCon').find_element(By.TAG_NAME, 'span').text
            cur_hour, cur_min = int(time[:time.index(':')]), int(time[time.index(':')+1:])
            print('**********')
            print(f'{cur_hour}:{cur_min}')
            print(f'Ждать ещё {cur_hour*60 + cur_min - localtime().tm_hour*60 - localtime().tm_min} минут')
            print(f'{localtime().tm_hour}:{localtime().tm_min}')
            print('**********')
            if 8 < cur_hour*60 + cur_min - localtime().tm_hour*60 - localtime().tm_min < 9:
                link = item.find_element(By.CLASS_NAME, 'kofsTableLineNums').find_element(By.TAG_NAME, 'a').get_attribute('href')
                if self.check_link(link):
                    message = f'''Коэффициенты удовлетворяют условию:
{self.browser.current_url}'''
                    self.tk.send_text_message(message)
                else:
                    message = f'''Коэффициенты не удовлетворяют условию:
{self.browser.current_url}'''
                    self.tk.send_text_message(message)


if __name__ == '__main__':
    lp = LineParser()
    while True:
        resp = lp.visit_site_and_setup_timefiltr()
        if not resp:
            print('something went wrong')
            continue
        lp.infinity_parsing()
        print('time  to sleep')
