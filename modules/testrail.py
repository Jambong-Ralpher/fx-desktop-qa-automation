"""TestRail API binding for Python 3.x.

(API v2, available since TestRail 3.0)

Compatible with TestRail 3.0 and later.

Learn more:

http://docs.gurock.com/testrail-api2/start
http://docs.gurock.com/testrail-api2/accessing

Copyright Gurock Software GmbH. See license.md for details.
"""

import base64
import json

import requests


class APIClient:
    def __init__(self, base_url):
        self.user = ""
        self.password = ""
        if not base_url.endswith("/"):
            base_url += "/"
        self.__url = base_url + "index.php?/api/v2/"

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("GET", uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("POST", uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(
            base64.b64encode(bytes("%s:%s" % (self.user, self.password), "utf-8")),
            "ascii",
        ).strip()
        headers = {"Authorization": "Basic " + auth}

        if method == "POST":
            if uri[:14] == "add_attachment":  # add_attachment API method
                files = {"attachment": (open(data, "rb"))}
                response = requests.post(url, headers=headers, files=files)
                files["attachment"].close()
            else:
                headers["Content-Type"] = "application/json"
                payload = bytes(json.dumps(data), "utf-8")
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except (
                requests.exceptions.HTTPError
            ):  # response.content not formatted as JSON
                error = str(response.content)
            raise APIError(
                "TestRail API returned HTTP %s (%s)" % (response.status_code, error)
            )
        else:
            if uri[:15] == "get_attachment/":  # Expecting file, not JSON
                try:
                    open(data, "wb").write(response.content)
                    return data
                except FileNotFoundError:
                    return "Error saving attachment."
            else:
                try:
                    return response.json()
                except requests.exceptions.HTTPError:
                    return {}


class APIError(Exception):
    pass


class TestRail:
    def __init__(self, host, username, password):
        self.client = APIClient(host)
        self.client.user = username
        self.client.password = password

    # Public Methods

    def create_test_run(
        self, testrail_project_id, testrail_milestone_id, name_run, testrail_suite_id
    ):
        data = {
            "name": name_run,
            "milestone_id": testrail_milestone_id,
            "suite_id": testrail_suite_id,
        }
        return self.client.send_post(f"add_run/{testrail_project_id}", data)

    def does_milestone_exist(self, testrail_project_id, milestone_name):
        num_of_milestones_to_check = 10  # check last 10 milestones
        milestones = self._get_milestones(
            testrail_project_id
        )  # returns reverse chronological order
        for milestone in milestones[
            -num_of_milestones_to_check:
        ]:  # check last 10 api responses
            if milestone_name == milestone["name"]:
                return True
        return False

    def update_test_cases_to_passed(
        self, testrail_project_id, testrail_run_id, testrail_suite_id
    ):
        test_cases = self._get_test_cases(testrail_project_id, testrail_suite_id)
        data = {
            "results": [
                {"case_id": test_case["id"], "status_id": 1} for test_case in test_cases
            ]
        }
        return self._update_test_run_results(testrail_run_id, data)

    # Private Methods

    def _get_test_cases(self, testrail_project_id, testrail_test_suite_id):
        return self.client.send_get(
            f"get_cases/{testrail_project_id}&suite_id={testrail_test_suite_id}"
        )

    def _update_test_run_results(self, testrail_run_id, data):
        return self.client.send_post(f"add_results_for_cases/{testrail_run_id}", data)

    def _get_milestones(self, testrail_project_id):
        return self.client.send_get(f"get_milestones/{testrail_project_id}")

    def _retry_api_call(self, api_call, *args, max_retries=3, delay=5):
        """
        Retries the given API call up to max_retries times with a delay between attempts.

        :param api_call: The API call method to retry.
        :param args: Arguments to pass to the API call.
        :param max_retries: Maximum number of retries.
        :param delay: Delay between retries in seconds.
        """
        for attempt in range(max_retries):
            try:
                return api_call(*args)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise  # Reraise the last exception
                time.sleep(delay)


def get_release_version():
    # Get the current script's directory (absolute path)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Initialize root_dir as script_dir initially
    root_dir = script_dir

    # Loop to traverse up until you find the version.txt or reach the filesystem root
    while root_dir != os.path.dirname(
        root_dir
    ):  # Check if root_dir has reached the filesystem root
        version_file_path = os.path.join(root_dir, "version.txt")
        if os.path.isfile(version_file_path):
            break
        root_dir = os.path.dirname(root_dir)  # Move one directory up

    # Check if version.txt was found
    if not os.path.isfile(version_file_path):
        raise FileNotFoundError(
            "version.txt not found in any of the parent directories."
        )

    # Read the version from the file
    with open(version_file_path, "r") as file:
        version = file.readline().strip()

    return version


def get_release_type(version):
    release_map = {"a": "Alpha", "b": "Beta"}
    # use generator expression to check each char for key else default to 'RC'
    product_type = next(
        (release_map[char] for char in version if char in release_map), "RC"
    )
    return product_type


def load_testrail_credentials(json_file_path):
    try:
        with open(json_file_path, "r") as file:
            credentials = json.load(file)
        return credentials
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to load TestRail credentials: {e}")
