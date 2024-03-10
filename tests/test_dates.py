import pytest

import assignment1.main as main

@pytest.fixture
def text():
    text = "John and Mary have decided to organize two major events; the first one is set for 12 March 2023, where John will lead the workshop. The second event, managed by Mary, is scheduled for 24 August 2023, focusing on community engagement."
    return text


def test_extract_dates(text):
    data, date_list = main.dates(text)
    assert len(date_list) == 2
