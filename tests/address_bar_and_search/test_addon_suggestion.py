import json
import time

import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.service import Service

# from selenium.webdriver import Firefox
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire.webdriver import Firefox

from modules.browser_object import Navigation

# Map input text to addon names
input_to_addon_name = {
    "clips": "video-downloadhelper",
    # "grammar": "languagetool",
    # "Temp mail": "private-relay",
    # "pics search": "search_by_image",
    # "darker theme": "darkreader",
    # "privacy": "privacy-badger17",
    # "read aloud": "read-aloud",
}


@pytest.mark.parametrize("input_text, addon_name", input_to_addon_name.items())
def test_addon_suggestion_based_on_search_input(
    driver: Firefox, input_text: str, addon_name: str
):
    """
    C2234714: Test that add-on suggestions match the URL bar input.
    """
    # driver = webdriver.Firefox()

    nav = Navigation(driver).open()
    # print(
    #     request.url,
    #     request.response.status_code,
    #     request.response.headers['Content-Type']
    # )
    # Define the capabilities for Firefox
    # caps = DesiredCapabilities.FIREFOX.copy()
    # caps['loggingPrefs'] = {'performance': 'ALL'}

    # # Set up the Firefox options and service
    # options = webdriver.FirefoxOptions()
    # options.set_capability("moz:firefoxOptions", {"args": ["-headless"]})  # Optional: Run in headless mode

    # service = Service(executable_path='/path/to/geckodriver')  # Adjust path to your geckodriver

    # # Initialize the WebDriver for Firefox
    # driver = webdriver.Firefox(service=service, options=options)
    # driver.get('about:blank')

    # def process_browser_log_entry(entry):
    #     response = json.loads(entry['message'])['message']
    #     return response

    # # Retrieve the browser logs
    # browser_log = driver.get_log('performance')
    # events = [process_browser_log_entry(entry) for entry in browser_log]
    # events = [event for event in events if 'Network.response' in event['method']]

    # # # Process the captured network events
    # for event in events:
    #     print(event)
    # driver = webdriver.Firefox()
    # driver.get('about:blank')

    # for request in driver.requests:
    #     if request.response:
    #         print(
    #             request.url,
    #             request.response.status_code,
    #             request.response.headers['Content-Type']
    #         )
    while 1:
        pass

    # time.sleep(7)
    prev_len = 0
    url_count = 0
    j = 0
    while j < 100:
        # for request in driver.requests:
        #     if request.response:
        #         if "https://firefox.settings.services.mozilla.com/v1/buckets/main/collections/quicksuggest/" in request.url:
        #             i+=1
        #             break
        request_len = len(driver.requests)
        for i in range(prev_len, request_len):
            if (
                "https://firefox.settings.services.mozilla.com/v1/buckets/main/collections/quicksuggest/"
                in driver.requests[i].url
            ):
                url_count += 1

        prev_len = request_len
        j += 1
        time.sleep(0.1)

    # nav.set_awesome_bar()
    # time.sleep(10)
    # nav.awesome_bar.click()

    # nav.awesome_bar.send_keys(input_text)
    # # # time.sleep(3)
    # nav.element_visible("addon-suggestion")
    # nav.get_element("addon-suggestion").click()

    # # Construct the expected URL
    # expected_url = f"https://addons.mozilla.org/en-US/firefox/addon/{addon_name}/"
    # nav.expect_in_content(EC.url_contains(expected_url))
