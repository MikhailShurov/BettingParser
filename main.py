from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep

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

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def visit_site_and_setup_timefiltr(self):       # Полностью работает
        self.browser.get('https://melbet.ru/line/football/')
        sleep(5)
        time_filtr = self.browser.find_element(By.ID, 'timeFiltr')
        time_filtr.click()
        select = Select(time_filtr)
        select.select_by_value("60")
        time_filtr.click()
        sleep(5)

        self.browser.save_screenshot('poster.png')
        TelegramClient.TeleframClient().send_screenshots()

    def infinity_parsing(self):
        football = self.browser.find_element(By.ID, 'allSport').find_element(By.TAG_NAME, 'div').find_element(By.CLASS_NAME, 'eventsMenuUl').find_element(By.CSS_SELECTOR, 'li.active')
        championats = football.find_elements(By.TAG_NAME, 'li')
        for championat in championats:
            print('chembumpelya')
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", championat)
            championat.find_elements(By.TAG_NAME, 'span')[-1].click()
            sleep(3)
            self.browser.save_screenshot('poster.png')
            TelegramClient.TeleframClient().send_screenshots()
            sleep(3)
            all_matches = championat.find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
            for li in all_matches:
                try:
                    current_date = li.find_element(By.CLASS_NAME, 'date').text[-6:-1]
                    print(current_date)
                except:
                    continue


if __name__ == '__main__':
    lp = LineParser()
    lp.visit_site_and_setup_timefiltr()
    lp.infinity_parsing()
