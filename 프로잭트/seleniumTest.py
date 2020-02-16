from selenium import webdriver

driver = webdriver.Chrome('C:/Users/justi/Documents/chromedriver/chromedriver')

driver.get("http://www.google.com")
input_element = driver.find_element_by_name("q")
input_element.send_keys("파이썬")
input_element.submit()