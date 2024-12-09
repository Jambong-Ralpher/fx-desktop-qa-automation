import pytest
from selenium.webdriver import Firefox

from modules.browser_object import Navigation, PanelUi
from modules.page_object import LoginAutofill


@pytest.fixture()
def test_case():
    return "101670"


SAMPLE_USER = "bob_c"
SAMPLE_PASS = "123456"


@pytest.fixture()
def add_prefs():
    return [("signon.rememberSignons", True)]


def test_no_password_doorhanger_private_browsing(driver: Firefox):
    """
    C101670: Ensure no save password doorhanger shows up and settings are correct
    """
    # instantiate objects
    login_auto_fill = LoginAutofill(driver)
    panel_ui = PanelUi(driver)
    nav = Navigation(driver)

    # open private window
    panel_ui.open_private_window()
    nav.switch_to_new_window()

    # open the form, fill the user and password
    login_auto_fill.open()
    login_form = login_auto_fill.LoginForm(login_auto_fill)
    login_form.fill_username(SAMPLE_USER)
    login_form.fill_password(SAMPLE_PASS)
    login_form.submit()

    # ensure that the panel is not open
    with driver.context(driver.CONTEXT_CHROME):
        login_auto_fill.wait.until(
            lambda d: login_auto_fill.get_element("save-login-popup").get_attribute(
                "panelopen"
            )
            is None
        )
