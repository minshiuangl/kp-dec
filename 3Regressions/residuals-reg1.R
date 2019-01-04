#Set working directory
setwd("/Users/MLEE/Desktop/UniMelb/Honours/Research/KP-DEC/Data/Python")

#Load libraries
library(car)
library(carData)
library(stargazer)
library(nlme)
library(lme4)
library(lmtest)
library(data.table)

#Load files
df <- read.csv(file = "KP-security-reg-15.csv", header=TRUE)
df <- subset(df, select = -c(X))
df$problem <- factor(df$problem , ordered = FALSE )
df$complexity <- factor(df$complexity, ordered= FALSE)
df$security <- factor(df$security, ordered= FALSE)
df$participant_id <- factor(df$participant_id, ordered= FALSE)
df$session <- factor(df$session, ordered= FALSE)

#Create new variables to check for heteroskedasticity
df$tradeprice_deviation <- (df$tradeprice - 0.5)^2
df$marketbid_deviation <- (df$marketbid - 0.5)^2

#Regression 1.1.1
fvar <- change_in_var_opt ~ change_in_marketbid
fvar1 <- change_in_var ~ change_in_marketbid
fvar2 <- change_in_var ~ change_in_tradeprice

reg1 <- lm(fvar, data=df, na.action = na.omit)
reg2 <- lm(fvar1, data=df, na.action = na.omit)
reg3 <- lm(fvar2, data=df, na.action = na.omit)
resid <- resid(reg1, na.action = na.omit)
resid1 <- resid(reg2, na.action = na.omit)
resid2 <- resid(reg3, na.action = na.omit)
f <- abs(resid) ~ mktbid_deviation
f1 <- abs(resid1) ~ mktbid_deviation
f2 <- abs(resid2) ~ trdprc_deviation
dt <- df[!is.na(df$change_in_marketbid),]
mktbid_deviation <- dt$marketbid_deviation
reg <- lm(f)
rega <- lm(f1)
dt <- df[!is.na(df$change_in_tradeprice),]
trdprc_deviation <- dt$tradeprice_deviation
regb <- lm(f2)

stargazer(reg1, reg, reg2, rega, reg3, regb, dep.var.labels.include=FALSE, 
          dep.var.caption='Check for Heteroskedasticity', title='Regression 1.1', 
          column.labels = c('$\\Delta var_opt_{t}$', 'Abs Residuals', '$\\Delta var_{t}$', 
                            'Abs Residuals', '$\\Delta var_{t}$', 'Abs Residuals'), 
          align=TRUE, no.space=TRUE, column.sep.width="-8pt", omit.stat=c("ser"), 
          star.char = c("+", "*", "**", "***"), star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg1.1.1.1.tex')
