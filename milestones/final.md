# Chi-Ed

## Data Documentation

### Chicago Public Schools API Date
- Source URL: https://api.cps.edu/schoolprofile/CPS/AllSchoolProfiles
- Source Type: API
- Number of Records (rows): 649
- Number of Attributes (columns): 188

This was our primary data sorce. It contains information on all public schools in Chicago as administered by Chicago Public Schools. The data is for a single year i.e., 2025 and does not contain historical data.

### Illinois State Board of Education - School Report Card Data
- Source URL: https://www.isbe.net/pages/illinois-state-report-card-data.aspx
- Source Type: Bulk data (CSV, XLSX)

This was our secondary data source which contained information on individual school performances on indicators that we use like mathematical efficiency, english language efficiency. We also have panel data available for this data which was used to do a historical anylsis on specific school outcomes.


### Chicago Neighborhood Level Shapefiles
- Source URL: https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Neighborhoods/bbvz-uum9
- Source Type: Shapefile

This is our geospatial data which was used to build the dashboard and do spatial merge to find which schools fall under which neighborhood.


### Directory of Educational Entities
- Source URL: https://www.isbe.net/Pages/Data-Analysis-Directories.aspx
- Source Type: CSV

Auxillary data that we used to merge with report card data to get ZIP codes that we then use as blocking for our main merge between report card data and API data.


## Project Structure

![prject_flow](../docs/coding_workflow.png)

## Team Responsibilites

## Final Thoughts
