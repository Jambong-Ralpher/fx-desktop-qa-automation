import pytest


@pytest.fixture()
def suite_id():
    return ("S2130", "Sync and Firefox Account")


@pytest.fixture()
def set_prefs():
    """Set prefs"""
    return []
