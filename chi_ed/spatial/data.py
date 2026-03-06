# from shapely.geometry import Point, Polygon
# from typing import NamedTuple
# import pathlib
# import shapefile
# import csv

import geopandas as gpd
import pandas as pd
import json


neigbhorhoods = gpd.read_file("path/to/your/neighborhoods.shp")

# class Neighborhood(NamedTuple):
#     id: str
#     polygon: Polygon


# def load_shapefiles(path: pathlib.Path) -> Neighborhood:
#     """
#     Extract and parse polygons from Census shapefiles.
#     """
#     neighborhoods = []
#     with shapefile.Reader(path) as sf:
#         # This iterates over all shapes with their associated data.
#         for shape_rec in sf.shapeRecords():
#             # the shape_rec object here has two properties of interest
#             #    shape_rec.record - dict containing the data attributes
#             #                       associated with the shape
#             #    shape_rec.shape.points - list of WKT points, used to construct
#             #                             a shapely.Polygon
#             neighborhoods.append(
#                 Neighborhood(
#                     id=shape_rec.record["FID"],
#                     polygon=Polygon(shape_rec.shape.points),
#                 )
#             )

#     return neighborhoods





