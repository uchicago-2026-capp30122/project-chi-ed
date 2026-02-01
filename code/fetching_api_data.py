import json
import sys
import httpx
from pathlib import Path
from pprint import pprint

RAW_DATA_API = Path(__file__).parent.parent / "data/raw_data/api_data.json"


class FetchException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )


if RAW_DATA_API.exists():
    print(f'The downloaded API data can be found using the following file path')
else:
    url = "https://api.cps.edu/schoolprofile/CPS/AllSchoolProfiles"
    response = httpx.get(
        url, 
        timeout=10
        ) # increasing timeout helps load data
    if response.status_code != 200:
        raise FetchException(response)
    else:
        api_data = response.json()
        with open(RAW_DATA_API, 'w') as f:
            json.dump(api_data, f, indent=1)
