#Set working directory
setwd('/Users/MLEE/desktop/KP-DEC-Python-Results/')

#Load libraries
library(car)
library(carData)
library(easyGgplot2)
library(stargazer)
library(nlme)
library(lme4)
library(MASS)
library(data.table)

df <- read.csv(file = "priceconvergence-market-15.csv", header=TRUE)
df <- subset(df, select = -c(X))
df$problem <- factor(df$problem , ordered = FALSE )
df$sec_complexity <- factor(df$sec_complexity, ordered= FALSE)
df$hard <- factor(df$hard, ordered= FALSE)
df$security <- factor(df$security, ordered= FALSE)
df$session <- factor(df$session, ordered= FALSE)
df$normalised_tradetime[df$normalised_tradetime == 0] <- NA

df$log_prop <- log(df$propagation)
df$log_price <- log(df$normalised_tradetime)
df$log_market <- log(df$marketactivity)

fvar1 <- log_price ~ log_prop*sec_complexity
fvar2 <- log_price ~ log_prop*sec_complexity

reg1 <- lme(fvar1, data=df, random = ~ 1|session/problem, na.action = na.omit)
reg2 <- lme(fvar2, data=df, random = ~ 1|session/problem, na.action = na.omit)
summary(reg2)


stargazer(reg2,covariate.labels=
            c("$\\text{log}(propagation_{p,j})$", "D2", "D3", "D4", 
              "$\\text{log}(propagation_{p,j})\\times D2$", 
              "$\\text{log}(propagation_{p,j})\\times D3$",
              '$\\text{log}(propagation_{p,j})\\times D4$', "Constant"),
          dep.var.labels.include=FALSE, 
          add.lines = list(c("Session Fixed Effects", "Yes"),
                           c("Problem Fixed Effects", "Yes")),
          dep.var.caption='$\\text{log}(npc_{s,p,j})$)', 
          title='Regression 4', column.labels = NULL, align=TRUE, no.space=TRUE,
          column.sep.width="-50pt", star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg0.tex')

rm(list=ls())



