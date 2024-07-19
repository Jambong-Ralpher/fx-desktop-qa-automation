from time import sleep

import pytest
from selenium.webdriver import Firefox
from selenium.webdriver.support import expected_conditions as EC

# from modules.browser_object import PanelUi
from modules.browser_object import ContextMenu, Devtools, Navigation, PanelUi, TabBar
from modules.page_object import AboutPrefs, GenericPage
from modules.util import BrowserActions, Utilities


def inject_log_capture_script(driver):
    script = """
    (function() {
        if (window.__logCaptureInitialized) return;
        window.__logCaptureInitialized = true;
        window.__logs = [];

        ['log', 'warn', 'error'].forEach(function(level) {
            var original = console[level];
            console[level] = function() {
                window.__logs.push({
                    level: level,
                    message: Array.from(arguments).map(String).join(' ')
                });
                original.apply(console, arguments);
            };
        });
    })();
    """
    driver.execute_script(script)


def get_captured_logs(driver):
    script = "return window.__logs;"
    logs = driver.execute_script(script)
    return logs


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

    # generic_page.context_click("body")
    # context_menu.click_and_hide_menu("context-menu-inspect")
    context_menu.click_context_item("context-menu-inspect")
    context_menu.hide_popup_by_child_node(inspect_option)
    devtools.check_opened()

    nav.search("https://permission.site/")
    sleep(5)
    # util.write_html_content("contentschrome", driver, True)
    # util.write_html_content("contents", driver, False)
    with driver.context(driver.CONTEXT_CHROME):
        # iframe = dev_tools.get_element("dev-tools-iframe")
        # dev_tools.expect(EC.frame_to_be_available_and_switch_to_it(dev_tools.get_selector("dev-tools-iframe")))
        # ba.switch_to_iframe_context(iframe)
        # dev_tools.get_element("console-tab-button").click()
        driver.execute_script("console.log('hello')")
        script = """
window.consoleMessages = [];
(function() {
    var oldLog = console.log;
    console.log = function (message) {
        window.consoleMessages.push(message);
        oldLog.apply(console, arguments);
    };
})();
"""
        sleep(10)
        driver.execute_script(script)
        messages = driver.execute_script("return window.consoleMessages")
        for message in messages:
            print(message)
    # # util.wri
    # sleep(10)
