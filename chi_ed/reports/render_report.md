---
title: "School Comparison Report"
subtitle: "{{school1}} | {{school2}}"
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

This report is a brief comparison of **{{school1}}** and **{{school2}}** across key performance and operational metrics. 
The data used here is collected by the Chicago Public Schools (CPS) authority and theIllinois State Board of Education.
We mostly have data for the most recent academic year 2024/2025, but for a few select number of variables, 
we will show you the schools' performance from the 2018/2019 to the 2024/2025 academic years.


\vspace{0.5 cm}

# Overview of the Past 7 Years

{{figure:Overview}}


\newpage

# A Closer Look at the Most Recent Academic Year: 2024/2025
We zoom in on the 2024/2024 academic year and also show how these two schools perform relative to other high schools in Chicago. 

{{figure:Academic Performance}}

\newpage

# Enrollment & Demographics
This section presents student counts, with a more details in-look on racial distributions. 
{{table:Enrollment & Demographics}}


# Faculty Experience and Students' Discipline
It is important to understand the quality and experience of the academic faculty, so we compare both institutions
teaching experience and discipline of their instructors (proxied here by their absenteeism). 
We also include the overall discipline of student while we discuss this topic. 

{{table:Faculty & Attendance}}


# Transportation services, CTA Access, Bilingual services, and other support programs

{{table:Infrastructure & Services}}


# Safety, culture, and overall school ratings

{{table:Ratings}}



# Contact Information

{{school1_address}}

{{school2_address}}
