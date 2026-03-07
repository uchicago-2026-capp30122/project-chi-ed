---
title: "School Comparison Report"
subtitle: "{{school1}} vs. {{school2}}"
author: "Chi-Ed Star Team"
date: \today
geometry: "left = 0.5in, right = 0.5in, top = 1in, bottom = 1in"
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{caption}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \floatplacement{table}{H}
numbersections: true
---

In this report, we compare **{{school1}}** and **{{school2}}** across key performance and operational metrics. 
The data is collected by the Chicago Public Schools (CPS) authority and theIllinois State Board of Education. 
For some variables, we have a time series analysis from 2019 to 2025. 
We mostly have data for the most recent academic year 2024/2025, but for a few select number of variables, 
we will show you the schools' performance from 201/2019 to 2024/2025 academic years.


\vspace{0.5 cm}

# Overview of the Past 7 Years

{{figure:Overview}}


\newpage

# Academic Performances
Now we zoom in on the most recent academic year, and also show how these two schools perform relative to other 
high schools in Chicago. 

{{figure:Academic Performance}}

\newpage

# Enrollment & Demographics
This section presents student counts, with a more details in-look on racial distributions. 
{{table:Enrollment & Demographics}}


# Faculty Experience and Students' Discipline
Student Chronic Absenteeism is the only metric in this section that is student-centered. 
We instead look at the experience of teachers and their performance (proxied here by their absenteeism). 

{{table:Faculty & Attendance}}


# Transportation services, CTA Access, Bilingual services, and other support programs

{{table:Infrastructure & Services}}


# Safety, culture, and overall school ratings
We also have ratings on the safety, culture, and an overall rating of each school. These ratings were performed by the public. 

{{table:Ratings}}



# Contact Information

{{school1_address}}

{{school2_address}}
