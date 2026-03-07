from chi_ed.cps_api.cleaning_api import clean_api_json
import polars as pl


def test_cleaning():
    clean_data = clean_api_json()
    assert clean_data.shape[0] == 173, "Dataframe Should Have 173 Rows"
    assert clean_data.shape[1] == 40, "Dataframe Should Have 40 Columns"
    assert clean_data.select(
        pl.col.school_short_name.n_unique() == pl.col.school_short_name.len()
    ).item(), "Each Row Should Contain a Unique School"
    # reference: https://stackoverflow.com/questions/79611225/polars-check-if-column-is-unique
    assert clean_data.with_columns(pl.col("zip").is_not_null()).shape[0] == 173, (
        "There Should be no Missing Zip Codes"
    )
