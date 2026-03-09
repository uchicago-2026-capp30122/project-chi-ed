from ..spatial.data import (
    load_neighborhoods,
    load_schools,
    get_school_points,
    get_spatial_join,
    CLEAN_DATA_DIR,
)

if __name__ == "__main__":
    # Write explanation of what this file is doing

    neighborhoods = load_neighborhoods()
    schools = load_schools()
    school_points = get_school_points(schools)
    spatial_join = get_spatial_join(school_points, neighborhoods)

    # Adding neighborhood to panel cleaned data
    schools["neighborhood"] = spatial_join["pri_neigh"].values
    schools.to_csv(CLEAN_DATA_DIR / "clean_panel.csv", index=False)
