import datetime
import logging
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.by import By

finder = namedtuple('finder', ['findby', 'value'])
_ttf = 30


def get_cookie(baseurl, username, password, username_finder, password_finder, button_finder, account_owner_finder, cookie_filter=None):
    try:
        # below args are required for chrome to work in docker. This may break when run standalone
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--remote-debugging-pipe')
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(20)
        driver.get(baseurl)
        driver.find_element(eval(f'By.{username_finder.findby.upper()}'), username_finder.value).send_keys(username)
        driver.find_element(eval(f'By.{password_finder.findby.upper()}'), password_finder.value).send_keys(password)
        driver.find_element(eval(f'By.{button_finder.findby.upper()}'), button_finder.value).click()
        if account_owner_finder.findby and account_owner_finder.value:
            accounts = driver.find_elements(eval(f'By.{account_owner_finder.findby.upper()}'), account_owner_finder.value)
            if len(accounts) != 1:
                raise Exception(f'Number of accounts with account owner: {account_owner_finder.value} != 1')
            accounts[0].click()
        if cookie_filter:
            c = driver.get_cookie(cookie_filter)
            _start_time = datetime.datetime.now()
            while not c and (datetime.datetime.now() - _start_time).total_seconds() < _ttf:
                c = driver.get_cookie(cookie_filter)
        else:
            c = driver.get_cookies()
        driver.quit()
        return c
    except Exception as e:
        logging.exception(e)
        driver.quit()
        raise e
