# Chi-Ed
## Members
- Mehwish Waheed - mehwishwaheed@uchicago.edu
- Essosolim Apollinaire Abi - eabi@uchicago.edu
- Muhammad Faizan Imran - imran_faiz@uchicago.edu

## Abstract
<p style='text-align: justify;'> This project compares academic performance across Chicago high schools and aggregates these comparisons to the neighborhood level to examine how schools perform across different parts of the city. It will enable comparisons both between individual schools and across neighborhoods to identify areas where schools tend to perform relatively better or worse.
We will use three datasets from multiple public sources. First, we will access data on school performance and school characteristics from Chicago Public Schools (queried via their School Profile API), which provides information on graduation rates, attendance, enrollment, and school locations for Chicago high schools. Second, we will rely on data from the Illinois State Board of Education (ISBE) Report Card to capture additional information on school resources and student demographics, including student–teacher ratios, investment, and expenditure. Finally, we will use geospatial boundary data for Chicago community areas from the City of Chicago Data Portal to define neighborhoods and aggregate school outcomes at the neighborhood level. We present our findings through an interactive, map-based dashboard that uses graphs and visual summaries to compare individual schools and neighborhoods across multiple performance and resource metrics. Our application will allow users to select schools or neighborhoods to produce a comparative study. 


## Preliminary Data Sources
###  Chicago Public Schools
- Source URL: https://api.cps.edu/schoolprofile/help
- Source Type: API
- Summary: This data has been published by Chicago Public Schools. It provides school-level data on academic performance and school characteristics, including graduation rates, attendance rates, enrollment, school type, and geographic coordinates. 
- Challenges: A primary challenge is missing data and inconsistent reporting of outcome variables across schools and neighborhoods.

### Illinois State Board of Education (ISBE)
- Source URL: https://www.isbe.net/pages/illinois-state-report-card-data.aspx
- Source Type: Bulk data (CSV, XLSX)
- Summary: Published by ISBE, this school-level data provides annual statistics such as average class size, student performance on standardized tests (ELA, math, and science), dropout rates, graduation rates, transfer-out rates, multiple expenditure categories, and teacher attendance ratios.
- Challenges: This data contains missing data, and we will have to identify sound methods of handling these inconsistencies. Furthermore, this dataset needs to be consolidated with Chicago Public Schools data. There might be challenges in matching data for the same school across both datasets due to the potential lack of a shared unique identifier.

### City of Chicago Data Portal
- Source URL: https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Neighborhoods/bbvz-uum9

- Source Type: Shapefile
- Summary: This data is published by the City of Chicago Data Portal and provides geospatial boundary shapefiles defining Chicago community areas. These boundaries will be used to map school locations and aggregate school-level outcomes and characteristics to the neighborhood level.
- Challenges: We need to decide the geographic level at which we need to aggregate the school-level characteristics. Schools located on or near neighborhood boundaries may also present challenges for analysis.

## Questions
1. For data loaded through API, should we plan to store the pre-loaded data in the project directory or integrate a dataloader.py file that loads the data once a user runs the app? This is important for execution speed and also GitHub’s capacity to store large datasets.
