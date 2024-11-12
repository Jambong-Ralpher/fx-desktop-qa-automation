import pytest
from selenium.webdriver import Firefox, Keys
from modules.page_object_google import GoogleSheets


@pytest.fixture()
def test_case():
    return "936864"


SHEET1_URL = "https://sheet.zoho.eu/sheet/open/b47r7ee5ed7cd220643fe8a98bc83794ef410"
SHEET2_URL = "https://docs.google.com/spreadsheets/d/1HDwm0E77eyVkMQYiDkCCBp3lep4n9Mq0pW7uVE6yncg/edit?usp=sharing"

expected_values = [
    ["Book", "Author", "Category"],
    ["Precipice", "Robert Harris", "fiction"],
]


def test_copy_from_an_editor_paste_in_another(driver: Firefox, sys_platform):
    """
    C936864: Pressing “Ctrl” key to select and copy multiple rows/columns of a table from an online editor then pasting
    to another online editor
    """
    # Initializing objects
    web_page = GoogleSheets(driver, url=SHEET1_URL).open()

    # Copy several rows/columns
    web_page.select_num_rows(3)
    web_page.copy(sys_platform)

    # Paste table in the second online editor
    GoogleSheets(driver, url=SHEET2_URL).open()
    web_page.paste(sys_platform)

    # Verify that the previous selection copied is pasted in the new place
    try:
        for row_index, row in enumerate(expected_values):
            for col_index, expected_value in enumerate(row):
                # Wait until value is present in the cell
                web_page.wait.until(
                    lambda _: expected_value in web_page.get_element("formula-box-input").get_attribute("innerHTML")
                )
                # Check that the current cell's value matches expected_value
                actual_value = web_page.get_element("formula-box-input").get_attribute("innerHTML")
                assert expected_value in actual_value
                # Move to the next cell to the right
                web_page.perform_key_combo(Keys.RIGHT)
            # Move to the beginning of the next row
            web_page.perform_key_combo(Keys.HOME)
            # Move down to the next row
            web_page.perform_key_combo(Keys.DOWN)
    finally:
        # Undo the paste operation
        web_page.undo(sys_platform)
