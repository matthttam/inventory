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

# Get a permission based on model and codename
def get_permission(model: models.Model, codename: str) -> Permission:
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(codename=codename, content_type=content_type)
    return permission


def get_chrome_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


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
