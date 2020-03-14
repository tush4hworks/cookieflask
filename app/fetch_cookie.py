from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import namedtuple

finder = namedtuple('finder', ['findby', 'value'])

def get_cookie(baseurl, username, password, username_finder, password_finder, button_finder):
	try:
		driver = webdriver.Chrome()
		driver.implicitly_wait(30)
		driver.get(baseurl)
		getattr(driver, 'find_element_by_{}'.format(username_finder.findby))(username_finder.value).send_keys(username)
		getattr(driver, 'find_element_by_{}'.format(password_finder.findby))(password_finder.value).send_keys(password)
		getattr(driver, 'find_element_by_{}'.format(button_finder.findby))(button_finder.value).click()
		c = driver.get_cookies()
		driver.quit()
		return c
	except Exception as e:
		driver.quit()
		raise