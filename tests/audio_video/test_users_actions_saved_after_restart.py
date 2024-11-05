import pytest
from selenium.webdriver import Firefox

from modules.browser_object_navigation import Navigation
from modules.page_object_generics import GenericPage
from modules.util import BrowserActions

from modules.page_object_prefs import AboutPrefs


@pytest.fixture()
def test_case():
    return "330168"


@pytest.fixture()
def add_prefs():
    return [("media.autoplay.default", 1), ("media.autoplay.enabled.user-gestures-needed", True)]


TEST_URL = "https://www.mlb.com/video/rockies-black-agree-on-extension"


def test_users_actions_saved_after_restart(driver: Firefox):
    """
    C330168: Verify that the users actions are saved after restart
    """
    # Instantiate objects
    nav = Navigation(driver)
    about_prefs = AboutPrefs(driver, category="privacy")
    ba = BrowserActions(driver)

    # Open Test page
    GenericPage(driver, url=TEST_URL).open()

    # Open the Site information panel and check "Allow Audio and Video"
    nav.click_on("autoplay-permission")
    nav.click_on("permission-popup-audio-blocked")
    nav.click_and_hide_menu("allow-audio-video-menuitem")

    # Refresh test page and check the site information panel shows "Allow Audio and Video"
    driver.get(driver.current_url)
    nav.element_visible("permission-popup-audio-video-allowed")

    # The Crossed off Play icon is no longer displayed
    nav.element_not_visible("blocked-permission-icon-autoplay-media-icon")

    # The website is added to the exceptions list in about:preferences#privacy
    about_prefs.open()
    about_prefs.get_element("autoplay-settings-button").click()

    # Get the web element for the iframe
    iframe = about_prefs.get_iframe()
    ba.switch_to_iframe_context(iframe)

    about_prefs.element_visible("mlb-allow-audio-video")

    # Open Test page
    GenericPage(driver, url=TEST_URL).open()

    # Open the Site information panel and check "Block Audio and Video"
    nav.click_on("autoplay-permission")
    nav.click_on("permission-popup-audio-video-allowed")
    nav.click_and_hide_menu("block-audio-video-menuitem")

    # Refresh test page and check the site information panel shows "Block Audio and Video"
    driver.get(driver.current_url)
    nav.element_visible("permission-popup-audio-video-allowed")
    nav.element_visible("blocked-permission-icon-autoplay-media-icon")
