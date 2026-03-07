# import json

# TODO: Temporary fix come back later to remove
import sys
import pathlib
ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT))



from chi_ed.spatial.data import load_neighborhoods, load_schools, get_school_points, get_spatial_join, CLEAN_DATA_DIR

neighborhoods = load_neighborhoods()
schools = load_schools()
school_points = get_school_points(schools)
spatial_join = get_spatial_join(school_points, neighborhoods)

# Adding neighborhood to cleaned data 
schools["neighborhood"] = spatial_join["pri_neigh"].values
schools.to_csv(CLEAN_DATA_DIR / "clean_panel.csv", index=False)

# Saving school-to-neighborhood mapping as JSON
# schools_by_neighborhoods = {}
# for _, row in spatial_join.iterrows():
#     schools_by_neighborhoods[row["school_name"]] = row["pri_neigh"]

# output_path = CLEAN_DATA_DIR / "schools_by_neighborhoods.json"
# with open(output_path, "w") as f:
#     json.dump(schools_by_neighborhoods, f, indent=2)