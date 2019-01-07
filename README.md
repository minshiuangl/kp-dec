# kp-dec
To use the codes, please follow the format of the data files in the Raw Data folder. 

The remaining folders are labelled according to the order of execution. 
Please follow the number of the folders: first, clean the raw data; second, analyse the data; last, run regressions. 

In the Data Cleaning folder, there are 13 files, please follow the number labels. 
Use the 'IGNORE-knapsack-checkmissingdata.py' only to check for missing entries when extracting data from Ad-hoc markets. 

In the Data Analysis folder, there are 3 files, they can be run independently. 
These files are specific to the decision case of the Knapsack Problem.

In the Regressions folder, there are 2 files, use the file named 'regressions.R' to run all the regressions in the thesis. 
The regressions are run using Rstudio. "residuals.reg1.R" is used to check for heteroskedasticity of the first regression. 

There is an additional file called "Regression0.R". 
It is used to check for a relationship between price convergence and instance complexity. 
