from chi_ed.cps_api.fetching_api_data import get_api_data
from pathlib import Path
import json

API_JSON = Path(__file__).parent.parent / "data/raw/api_data/api_data.json"
HIGH_SCHOOL_COUNT = 173


def test_api_length():
    get_api_data()  # this function checks if API data exists, if not it fetches the API
    with open(API_JSON, "r") as api_json:
        api_data = json.load(api_json)
    assert len(api_data) == 649, "Expected 649 Total Schools!"
    assert api_data[0]["SchoolShortName"] == "FISHER", "First School Name: FISHER"

    hs_count = 0
    for school in api_data:
        if school["IsHighSchool"]:
            hs_count += 1

    assert hs_count == HIGH_SCHOOL_COUNT, "Total High Schools Should be 173!"
