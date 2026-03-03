from rc_zip import merge_for_zip, REPORT_CARD_PATH, DIRECTORY_DATA_PATH
#from cps_api.cleaning_api import clean_api_json, RAW_DATA_API
import polars as pl
import re

# ------------------------------------------------------------------------------
# In this code we use fuzzy matching to link & merge API data with report card data
# ------------------------------------------------------------------------------

report_card_df = merge_for_zip()
#api_df = clean_api_json()


