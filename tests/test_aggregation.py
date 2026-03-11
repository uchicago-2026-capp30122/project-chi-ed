import pytest
import pandas as pd
from chi_ed.spatial.aggregation import aggregate_by_neighborhood


@pytest.fixture
def sample_schools():
    """Three schools in Lincoln Park — one has missing ELA data."""
    return pd.DataFrame({
        "neighborhood": ["Lincoln Park", "Lincoln Park", "Lincoln Park"],
        "ELA_proficiency": [80.0, 60.0, None],
    })


def test_average_ignores_missing_values(sample_schools):
    result = aggregate_by_neighborhood(sample_schools, "ELA_proficiency", 2025)
    avg = result[result["neighborhood"] == "Lincoln Park"]["ELA_proficiency"].iloc[0]
    assert avg == pytest.approx(70.0)