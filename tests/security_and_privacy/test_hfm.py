
import pytest
from selenium.webdriver import Firefox

from modules.browser_object import PanelUi
# from modules.browser_object import Navigation, PanelUi, TabBar
from modules.page_object import AboutPrefs


@pytest.fixture()
def add_prefs():
    return []


def test_hfm_enable_https_mode(driver: Firefox):
    about_prefs = AboutPrefs(driver, category="privacy").open()
    panel_ui = PanelUi(driver)
    # nav = Navigation(driver)
    # tabs = TabBar(driver)

    # ensure that the HTTPS in All Windows is selected
    about_prefs.get_element("privacy-enable-https-all-windows").click()
    panel_ui.open_private_window()
