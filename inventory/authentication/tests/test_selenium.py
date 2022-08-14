from selenium import webdriver
from selenium.webdriver import ChromeOptions

chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)
browser.get("http://selenium.dev/")
