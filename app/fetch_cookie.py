from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import namedtuple

finder = namedtuple('finder', ['findby', 'value'])

def get_cookie(baseurl, username, password, username_finder, password_finder, button_finder, cookie_filter = None):
	try:
		#below args are required for chrome to work in docker. This may break when run standalone
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.implicitly_wait(20)
		driver.get(baseurl)
		getattr(driver, 'find_element_by_{}'.format(username_finder.findby))(username_finder.value).send_keys(username)
		getattr(driver, 'find_element_by_{}'.format(password_finder.findby))(password_finder.value).send_keys(password)
		getattr(driver, 'find_element_by_{}'.format(button_finder.findby))(button_finder.value).click()
		if cookie_filter:
			c = driver.get_cookie(cookie_filter)
		else:
			c = driver.get_cookies()
		driver.quit()
		return c
	except Exception as e:
		driver.quit()
		raise