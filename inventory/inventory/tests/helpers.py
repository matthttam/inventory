from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from authentication.tests.factories import UserFactory
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from shutil import which

from selenium.webdriver.chrome.service import Service as ChromeService

# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.chrome.service import Service as BraveService
# from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager

# from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.core.utils import ChromeType


# Get a permission based on model and codename
def get_permission(model: models.Model, codename: str) -> Permission:
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(codename=codename, content_type=content_type)
    return permission


def get_driver(type: str):
    options = webdriver.ChromeOptions()
    # options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    # if type == "Chrome":
    driver = webdriver.Chrome(
        options=options, service=ChromeService(ChromeDriverManager().install())
    )
    # elif type == "Chromium":
    #    driver = webdriver.Chrome(
    #        options=options,
    #        service=ChromiumService(
    #            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    #        ),
    #    )
    # elif type == "Brave":
    #    driver = webdriver.Chrome(
    #        options=options,
    #        service=BraveService(
    #            ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
    #        ),
    #    )
    # elif type == "Firefox":
    #    options = webdriver.FirefoxOptions()
    #    options.headless = True
    #    options.page_load_strategy = "eager"
    #    options.add_argument("--disable-gpu")
    #    driver = webdriver.Firefox(
    #        options=options, service=FirefoxService(GeckoDriverManager().install())
    #    )
    return driver


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.page_load_strategy = "eager"
    # options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--dns-prefetch-disable")
    # options.add_argument("--proxy-server='direct://'")
    # options.add_argument("--proxy-bypass-list=*")
    # options.add_argument("start-maximized")
    # options.add_argument("disable-infobars")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-preconnect")

    driver = webdriver.Chrome(
        options=options, service=ChromeService(ChromeDriverManager().install())
    )
    driver.set_page_load_timeout(120)
    return driver


def chrome_set_value(driver, element, value, timeout=10):
    driver.execute_script(
        f"arguments[0].value = '{value}';",
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(element)),
    )


def chrome_click_element(driver, element, timeout=10):
    driver.execute_script(
        f"arguments[0].click();",
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(element)),
    )


# def get_firefox_driver():
#    options = webdriver.FirefoxOptions()
#    options.headless = True
#    options.add_argument("--disable-gpu")
#    driver = webdriver.Firefox(
#        options=options, service=FirefoxService(GeckoDriverManager().install())
#    )
#    return driver
#    FIREFOX_PATH = which("firefox")
#    GECKO_PATH = which("geckodriver")
#    # options = Options()
#    options = webdriver.FirefoxOptions()
#    options.headless = True
#    options.add_argument("--disable-gpu")
#    # options.add_argument("--headless")
#    driver = webdriver.Firefox(options=options, executable_path=GECKO_PATH)
#    return driver
#    FIREFOX_PATH = which("firefox")
#    options = Options()
#    # options.binary = FIREFOX_PATH
#    # options.profile = webdriver.FirefoxProfile()
#    options.add_argument("--headless")
#    # options.add_argument("--disable-gpu")
#    # options.add_argument("--no-sandbox")
#    # options.add_argument("--dns-prefetch-disable")
#    #
#    driver = webdriver.Firefox(options=options, firefox_binary=FIREFOX_PATH)
#    driver.set_page_load_timeout(90)
#    return driver
