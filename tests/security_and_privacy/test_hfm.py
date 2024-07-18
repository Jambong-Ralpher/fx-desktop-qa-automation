from time import sleep

import pytest
from selenium.webdriver import Firefox

# from modules.browser_object import PanelUi
from modules.browser_object import ContextMenu, Devtools, Navigation, PanelUi, TabBar
from modules.page_object import AboutPrefs, GenericPage
from modules.util import BrowserActions, Utilities


@pytest.fixture()
def add_prefs():
    return []


def test_hfm_enable_https_mode(driver: Firefox):
    about_prefs = AboutPrefs(driver, category="privacy").open()
    panel_ui = PanelUi(driver)
    nav = Navigation(driver)
    generic_page = GenericPage(driver)
    context_menu = ContextMenu(driver)
    dev_tools = Devtools(driver)
    util = Utilities()
    ba = BrowserActions(driver)

    # ensure that the HTTPS in All Windows is selected
    about_prefs.get_element("privacy-enable-https-all-windows").click()
    panel_ui.open_private_window()
    nav.switch_to_new_window()

    generic_page.context_click("body")
    context_menu.click_and_hide_menu("context-menu-inspect")

    sleep(5)
    # util.write_html_content("contentschrome", driver, True)
    # util.write_html_content("contents", driver, False)
    with driver.context(driver.CONTEXT_CHROME):
        # iframe = dev_tools.get_element("dev-tools-iframe")
        # ba.switch_to_iframe_context(iframe)
        dev_tools.get_element("console-tab-button").click()
    # # util.wri
    # sleep(10)
