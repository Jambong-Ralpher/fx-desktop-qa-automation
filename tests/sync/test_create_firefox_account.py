from selenium.webdriver import Firefox
from time import sleep

from modules.page_object import AboutPrefs

def test_create_firefox_account(driver: Firefox):
    about_prefs = AboutPrefs(driver, category="sync").open()
    sleep(40)