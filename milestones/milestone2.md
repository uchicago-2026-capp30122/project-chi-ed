# Chi-Ed

## Abstract

<p style='text-align: justify;'>  This project compares academic performance across Chicago high schools and aggregates these comparisons to the neighborhood level to examine how schools perform across different parts of the city. It will enable comparisons both between individual schools and across neighborhoods to identify areas where schools tend to perform relatively better or worse.
We will use three datasets from multiple public sources. First, we will access data on school performance and school characteristics from Chicago Public Schools (queried via their School Profile API), which provides information on graduation rates, attendance, enrollment, and school locations for Chicago high schools. Second, we will rely on data from the Illinois State Board of Education (ISBE) Report Card to capture additional information on school resources and student demographics, including student–teacher ratios, investment, and expenditure. Finally, we will use geospatial boundary data for Chicago community areas from the City of Chicago Data Portal to define neighborhoods and aggregate school outcomes at the neighborhood level. We present our findings through an interactive, map-based dashboard that uses graphs and visual summaries to compare individual schools and neighborhoods across multiple performance and resource metrics. Our application will allow users to select schools or neighborhoods to produce a comparative study. </p>

## Data Sources

### Data Source #1
- Source URL: https://api.cps.edu/schoolprofile/CPS/AllSchoolProfiles
- Source Type: API
- Approximate Number of Records (rows): 649
- Approximate Number of Attributes (columns): 188
- Current Status: We have written code to fetch and store data from the CPS School Profile API. Each row represents a unique school, and the dataset includes school-level performance metrics (e.g., graduation rates, attendance rates), school type, and geographic coordinates. 
- Challenges: The unique identifiers used in the CPS API do not directly match those used in the ISBE Report Card data.

### Data Source #2
- Source URL: https://www.isbe.net/pages/illinois-state-report-card-data.aspx
- Source Type: Bulk data (CSV, XLSX)
- Approximate Number of Records (rows): 629
- Approximate Number of Attributes (columns): 899
- Current Status: We have downloaded the datasets and have done some basic exploratory analysis.
- Challenges: This dataset contains approximately 30 fewer high schools than the CPS API dataset. These discrepancies may need to be addressed during reconciliation. The dataset also contains missing values for some variables.

### Data Source #3
- Source URL: https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Neighborhoods/bbvz-uum9
- Source Type: Shapefile
- Current Status: We have downloaded the shapefiles for neighborhood boundaries. 

### Data Source #4 (New Addition)
- Source URL: https://www.isbe.net/Pages/Data-Analysis-Directories.aspx
- Source Type: CSV
- Approximate Number of Records (rows): 659
- Approximate Number of Attributes (columns): 20
- Current Status: We have written code to merge this dataset with the ISBE Report Card data to obtain zip code information for schools. These zip codes will be used as an additional validation step when matching schools across datasets.


## Data Reconciliation Plan

We will first consolidate Data Source #1 (CPS School Profile API) and Data Source #2 (ISBE Report Card) at the school level. Because the two datasets use different identifiers, we will rely on school names as the primary matching key and apply fuzzy string matching to align records. To improve matching accuracy, we will incorporate zip code information from Data Source #4 as a secondary validation step and manually review unmatched or ambiguous cases.
Once school-level datasets are consolidated, we will assign each school to a Chicago community area using geographic coordinates from the CPS API and shapefiles from Data Source #3. This spatial join will allow us to aggregate school-level performance and resource metrics to the neighborhood level for comparison and visualization.

## Project Plan

Note: The name infront of a task indicates the person who will lead its progress

### Weeks 4–5
- Fetch and store school-level data from the CPS School Profile API (Complete)
- Download and explore ISBE Report Card datasets (Complete)
- Finalize selection of metrics of interest for our project (Apo, Faizan, Mehwish)

### Week 5
- Consolidate CPS and ISBE datasets using name-based and zip-code-assisted matching (Faizan)
- Additional literature review of how educational outcomes are compared across schools (Mehwish)
- Clean and filter merged data to retain variables of interest (Apo)
- Discuss in details the metrics schools (or neighborhoods) will be compared on (Mehwish)
- Assess if we can do a temporal analysis or limit our comparisons to the most recent year that data is available (Faizan)
- Write the structure of our application, i.e., modules and functions that will: (Apo)
- Allow users to select if the want to compare schools or neighborhoods to compare from:
    - The command line (or)
    - A jupyter notebook
- Automate the creation of a pdf that compare schools or neighboorhoods

### Weeks 6–7
- Assign schools to community areas (neighborhoods) using geospatial shapefiles (Faizan)
- Generate an initial interactive map plotting school locations (Mehwish)
- Implement basic comparison graphs for selected metrics (Mehwish)
- Automate PDF creation for comparisons, with text, tables and static graphs (Apo)

### Week 7 (Prototype)
- Enable user interaction to select schools or neighborhoods (Mehwish)
- Validate school-to-neighborhood assignments, visual outputs, and PDF comparisons (Apo)
- Have 5 different users clone and test our application (Faizan)

## Questions

1. Are there recommended practices for handling discrepancies in school coverage across administrative datasets?
2. Do you have guidance on best practices for aggregating school-level metrics to neighborhood-level summaries in a geospatial context?
3. Which GIS libraries would you recommend using? The most we will do is work with shapefiles to map schools and neighborhood

