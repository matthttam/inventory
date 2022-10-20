from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

# Get a permission based on model and codename
def get_permission(model: models.Model, codename: str) -> Permission:
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(codename=codename, content_type=content_type)
    return permission


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


class RealTransactionalStaticLiveServerTestCase(StaticLiveServerTestCase, TestCase):
    pass
