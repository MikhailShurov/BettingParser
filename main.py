from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep
from time import localtime

import TelegramClient

import schedule


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
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")

        self.tk = TelegramClient.TeleframClient()

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
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
            print(48)
            print(ex)
            return False

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
            if 2.0 < float(f_val) < 2.6 and 1.4 < float(s_val) < 1.55:
                self.browser.close()
                self.windows = self.browser.window_handles
                self.browser.switch_to.window(self.windows[-1])
                return True
            else:
                message = f'''Проверка коэффициентов:
{link}
{f_val}/{s_val}'''
                self.tk.send_text_message(message)
        except:
            self.browser.close()
            self.windows = self.browser.window_handles
            self.browser.switch_to.window(self.windows[-1])
            return False
        return False

    def infinity_parsing(self):
        try:
            matches = self.browser.find_elements(By.CLASS_NAME, 'kofsTableBody')
            for item in matches:
                time = item.find_element(By.CLASS_NAME, 'kofsTableLineNums').find_element(By.CLASS_NAME, 'dateCon').find_element(By.TAG_NAME, 'span').text
                cur_hour, cur_min = int(time[:time.index(':')]), int(time[time.index(':')+1:])
                print(f'Ещё ждать {cur_hour*60 + cur_min - localtime().tm_hour*60 - localtime().tm_min}')
                if 8 <= cur_hour*60 + cur_min - localtime().tm_hour*60 - localtime().tm_min <= 9:
                    print('Это подошло')
                    link = item.find_element(By.CLASS_NAME, 'kofsTableLineNums').find_element(By.TAG_NAME, 'a').get_attribute('href')
                    if self.check_link(link) and link not in self.used_links:
                        message = f'''Коэффициенты удовлетворяют условию:
{link}'''
                        self.tk.send_text_message_for_all(message)
                        self.used_links.append(link)
        except Exception as ex:
            print(88)
            print(ex)


if __name__ == '__main__':
    lp = LineParser()
    schedule.every().hour.do(lp.clear_used_links)
    while True:
        schedule.run_pending()
        resp = lp.visit_site_and_setup_timefiltr()
        if not resp:
            continue
        lp.infinity_parsing()
        print('**************************************************')
        sleep(5)
