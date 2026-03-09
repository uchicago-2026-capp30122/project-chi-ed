# Chi-Ed - An Interactive Dashboard to Compare Highschool Outcomes Across Chicago
Authors: Apollinaire Abi, Mehwish Waheed, Muhammad Faizan Imran

## Abstract

Understanding high school outcomes across a major city like Chicago is important; our project aims to provide an overall aggregation of high schools across various metrics (e.g., graduation rate, college enrollment rate, SAT scores) across different neighborhoods in Chicago and it also allows draws on comprehensive Chicago Public Schools and Illinois Report Card data sets to compare any two schools across a wider range of outcomes and facilities. 

With the dashboard and the report card we aim to facilitate both neighborhood level policy analysis which is aimed at policymakers to visualize the disparities in educational outcomes across different neighborhoods. The report card on the other hand provides a tool aimed at individual level decision making, through providing meaningful high school comparisons allowing users to make informed decisions about which high school would align best with their goals.

## Running the Code

Please follow the following steps and command line instructions to execute and run the project:

1. Clone the repository:

``` 
git clone git@github.com:uchicago-2026-capp30122/project-chi-ed.git
```

2. Run the cleaning sequence from the project root to get all the files needed to run the dashboard and generate reports:

``` 
uv run python -m chi_ed clean
```

3. Execute the dashboard:

``` 
uv run python -m chi_ed dashboard
```

4. Generate reports comparing schools in neighborhoods of your choice:

``` 
uv run python -m chi_ed report
```






