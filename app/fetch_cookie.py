import datetime
from collections import namedtuple

from selenium import webdriver

finder = namedtuple('finder', ['findby', 'value'])
_ttf = 10


def get_cookie(baseurl, username, password, username_finder, password_finder, button_finder, cookie_filter=None):
    try:
        # below args are required for chrome to work in docker. This may break when run standalone
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.implicitly_wait(20)
        driver.get(baseurl)
        getattr(driver, 'find_element_by_{}'.format(username_finder.findby))(username_finder.value).send_keys(username)
        getattr(driver, 'find_element_by_{}'.format(password_finder.findby))(password_finder.value).send_keys(password)
        getattr(driver, 'find_element_by_{}'.format(button_finder.findby))(button_finder.value).click()
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
        driver.quit()
        raise


if __name__ == "__main__":

    x = get_cookie("https://cldre2e.oktapreview.com/app/cldre2e_e2egovclouddev_1/exk17itut5w7ndIF90h8/sso/saml",
               "hrt_alpha101", "P@ssW0rd123", finder("name", "username"), finder("name", "password"),
               finder("xpath", "//*[@type='submit']"), cookie_filter="cdp-session-token")
    print(x)
