import json
import httpx
from pathlib import Path

RAW_DATA_API = Path(__file__).parent.parent.parent / "data/raw/api_data/api_data.json"
URL = "https://api.cps.edu/schoolprofile/CPS/AllSchoolProfiles"

# ------------------------------------------------------------------------------
# This codes attempts to fetch Chicago Public School API data - we make the call
# only if the data does not exist to speed up the process 
# ------------------------------------------------------------------------------

class FetchException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )


def get_api_data(filename: Path = RAW_DATA_API, api_url: str=URL):
    """
    This function checks for whether the API data has previosly been downloaded
    and saved, if not it makes the httpx.get call and writes the data in the
    folder.

    Input:
    filename: Path object identifying the name and path of the api data
    """
    if RAW_DATA_API.exists():  # check if data already exists
        print(
            f"The downloaded API data can be found using the following file path",
            filename,
        )
    else:
        url = api_url
        response = httpx.get(url, timeout=10)
        if response.status_code != 200:
            raise FetchException(response)
        else:  # get api data and save
            api_data = response.json()
            with open(filename, "w") as f:
                json.dump(api_data, f, indent=1)
