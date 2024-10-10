from time import sleep

import pytest
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

from modules.browser_object_navigation import Navigation
from modules.browser_object_tabbar import TabBar
from modules.page_object_about_pages import AboutLogins
from modules.page_object_autofill import LoginAutofill
from modules.page_object_generics import GenericPage
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def test_case():
    return "2240907"


@pytest.fixture()
def set_prefs():
    """Set prefs"""
    return [("signon.rememberSignons", True), ("cookiebanners.service.mode", 1)]


FACEBOOK_URL = "https://www.facebook.com/"


def test_autocomplete_dropdown_is_toggled_for_focused_login_fields_on_page_load(driver: Firefox):
    """
    C2240907 - Verify that autocomplete dropdown is toggled for focused login fields on page load
    """
    tabs = TabBar(driver)
    about_logins = AboutLogins(driver)
    login_autofill = LoginAutofill(driver)

    # Go to sites that have login field focus on page load
    GenericPage(driver, url=FACEBOOK_URL).open()
    tabs.new_tab_by_button()
    tabs.switch_to_new_tab()

    # Save 2 set of credentials for the visited sites
    about_logins.open()
    about_logins.click_add_login_button()
    about_logins.create_new_login(
        {
            "origin": "facebook.com",
            "username": "username1",
            "password": "password1",
        }
    )
    about_logins.click_add_login_button()
    about_logins.create_new_login(
        {
            "origin": "facebook.com",
            "username": "username2",
            "password": "password2",
        }
    )

    # Autocomplete dropdown is toggled for focused login fields on page load
    tabs.click_tab_by_index(1)
    with driver.context(driver.CONTEXT_CHROME):
        username_element = login_autofill.get_element("facebook-credentials")
        assert username_element.get_attribute("ac-value") == "username1"
