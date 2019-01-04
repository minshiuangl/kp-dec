#Regression 0- Propagation vs. Normalised Price Convergence
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

#Regression 1: Individual Performance
#Set working directory
setwd("C:/Users/minshiuangl/Downloads/")

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
df$sec_complexity <- factor(df$sec_complexity, ordered= FALSE)

#Create Lag terms
lag <- c("change_in_marketbid")
setDT(df)[,c("change_in_marketbid_lag1", "change_in_marketbid_lag2", 
             "change_in_marketbid_lag3", "change_in_marketbid_lag4",
             "change_in_marketbid_lag5" ) := shift(.SD, 1:5), 
          keyby = c("problem", "participant_id", "security"), .SDcols = lag]

fvar11 <- change_in_var ~ change_in_marketbid
fvar12 <- change_in_var ~ change_in_marketbid + change_in_marketbid_lag1 + 
  change_in_marketbid_lag2 + change_in_marketbid_lag3 + change_in_marketbid_lag4 + 
  change_in_marketbid_lag5

reg11 <- lme(fvar11, data=df, random = ~ 1|participant_id/tradetime, na.action = na.omit)
reg12 <- lme(fvar12, data=df, random = ~ 1|participant_id/tradetime, na.action = na.omit)

stargazer(reg11, reg12, covariate.labels=
            c("$\\Delta Market\\;bid_{p, j, t}$", "$\\Delta Market\\;bid_{p, j, t-1}$", 
              "$\\Delta Market\\;bid_{p, j, t-2}$", "$\\Delta Market\\;bid_{p, j, t-3}$", 
              "$\\Delta Market\\;bid_{p, j, t-4}$", "$\\Delta Market\\;bid_{p, j, t-5}$",
              "Constant"), dep.var.labels.include=FALSE, dep.var.caption='$\\Delta var_{i, p, j, t}$', 
          add.lines = list(c("Individual Fixed Effects", "Yes", "Yes"),
                           c("Time Fixed Effects", "Yes", "Yes")),
          title='Regression 1', column.labels = NULL, align=TRUE, no.space=TRUE,
          column.sep.width="-20pt", omit.stat=c("ser"), star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg1a.tex')

stargazer(reg12, covariate.labels=
            c("$\\Delta Market\\;bid_{p, j, t}$", "$\\Delta Market\\;bid_{p, j, t-1}$", 
              "$\\Delta Market\\;bid_{p, j, t-2}$", "$\\Delta Market\\;bid_{p, j, t-3}$", 
              "$\\Delta Market\\;bid_{p, j, t-4}$", "$\\Delta Market\\;bid_{p, j, t-5}$",
              "Constant"), dep.var.labels.include=FALSE, 
          dep.var.caption='$\\Delta var_{i, p, j, t}$', 
          add.lines = list(c("Individual Fixed Effects", "Yes"),
                           c("Time Fixed Effects", "Yes")),
          title='Regression 1', column.labels = NULL, align=TRUE, no.space=TRUE,
          column.sep.width="-50pt", omit.stat=c("ser"), star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg1.tex')

rm(list=ls())

#Regression 2: Information flow from market to individual 
#Set working directory
setwd("C:/Users/minshiuangl/Downloads/")

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
df$sec_complexity <- factor(df$sec_complexity, ordered= FALSE)

df$moves_improve <- df$moves*df$negative_var_opt

#Create Lag terms
lag <- c("change_in_marketbid")
setDT(df)[,c("bid_lag1", "bid_lag2", "bid_lag3", "bid_lag4", "bid_lag5") := 
            shift(.SD, 1:5), keyby = c("problem", "participant_id", 'security'), .SDcols = lag]

#Regression 2.2
fvar11 <- moves_improve ~ change_in_marketbid + (1|participant_id) + (1|tradetime)
fvar12 <- moves_improve ~ change_in_marketbid + bid_lag1 + (1|participant_id) + (1|tradetime)
fvar13 <- moves_improve ~ change_in_marketbid + bid_lag2 + (1|participant_id) + (1|tradetime)
fvar14 <- moves_improve ~ change_in_marketbid + bid_lag3 + (1|participant_id) + (1|tradetime)
fvar15 <- moves_improve ~ change_in_marketbid + bid_lag4 + (1|participant_id) + (1|tradetime)
fvar16 <- moves_improve ~ change_in_marketbid + bid_lag5 + (1|participant_id) + (1|tradetime)
fvar17 <- moves_improve ~ change_in_marketbid + bid_lag1+ bid_lag2 + bid_lag3 + bid_lag4 + bid_lag5 + 
  (1|participant_id) + (1|tradetime)

reg11 <- glmer(fvar11, data=df, family='poisson', na.action = na.omit)
reg12 <- glmer(fvar12, data=df, family='poisson', na.action = na.omit)
reg13 <- glmer(fvar13, data=df, family='poisson', na.action = na.omit)
reg14 <- glmer(fvar14, data=df, family='poisson', na.action = na.omit)
reg15 <- glmer(fvar15, data=df, family='poisson', na.action = na.omit)
reg16 <- glmer(fvar16, data=df, family='poisson', na.action = na.omit)
reg17 <- glmer(fvar17, data=df, family='poisson', na.action = na.omit)

stargazer(reg11, reg12, reg13, reg14, reg15, reg16, reg17, 
          covariate.labels=c("$\\Delta Market\\;bid_{p, j, t}$", "$\\Delta Market\\;bid_{p, j, t-1}$", 
              "$\\Delta Market\\;bid_{p, j, t-2}$", "$\\Delta Market\\;bid_{p, j, t-3}$", 
              "$\\Delta Market\\;bid_{p, j, t-4}$", "$\\Delta Market\\;bid_{p, j, t-5}$", 'Constant'),
          dep.var.labels.include=FALSE, dep.var.caption='$No.\\;of\\;Moves_{i, p, j, t}$', 
          add.lines = list(c("Individual Fixed Effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
                           c("Time Fixed Effects", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes")),
          title='Regression 2', align=TRUE, no.space=TRUE,
          column.sep.width="-20pt", omit.stat=c("ser"), star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg2a.tex')

stargazer(reg17, covariate.labels=
            c("$\\Delta Market\\;bid_{p, j, t}$", "$\\Delta Market\\;bid_{p, j, t-1}$", 
              "$\\Delta Market\\;bid_{p, j, t-2}$", "$\\Delta Market\\;bid_{p, j, t-3}$", 
              "$\\Delta Market\\;bid_{p, j, t-4}$", "$\\Delta Market\\;bid_{p, j, t-5}$", 'Constant'),
          dep.var.labels.include=FALSE, dep.var.caption='$No.\\;of\\;Moves_{i, p, j, t}$', 
          add.lines = list(c("Individual Fixed Effects", "Yes"),
                           c("Time Fixed Effects", "Yes")),
          title='Regression 2', align=TRUE, no.space=TRUE,
          column.sep.width="-50pt", omit.stat=c("ser"), star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg2.tex')

rm(list=ls())

#Regression 3: Information flow from individual to market
#Set working directory
setwd("C:/Users/minshiuangl/Downloads/")

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
df$sec_complexity <- factor(df$sec_complexity, ordered= FALSE)

df$bidcount_improve <- df$bidcount*df$positive_var
df$bidcount_ninety <- df$bidcount*df$positive_var*df$ninety
df$bidcount_eighty <- df$bidcount*df$positive_var*df$eighty

#Create Lag terms
lag <- c("var_bid")
setDT(df)[,c("var_lag1", "var_lag2", "var_lag3", "var_lag4", "var_lag5") := shift(.SD, 1:10), 
          keyby = c("problem", "participant_id", "security"), .SDcols = lag]

#Regression 1.1
fvar11 <- bidcount_improve ~ var_bid + (1|participant_id) + (1|tradetime)
fvar12 <- bidcount_improve ~ var_bid + var_lag1 + (1|participant_id) + (1|tradetime)
fvar13 <- bidcount_improve ~ var_bid + var_lag1 + var_lag2 + var_lag3 + var_lag4 + var_lag5 + 
  (1|participant_id) + (1|tradetime)

fvar21 <- bidcount_ninety ~ var_bid + (1|participant_id) + (1|tradetime)
fvar22 <- bidcount_ninety ~ var_bid + var_lag1 + (1|participant_id) + (1|tradetime)
fvar23 <- bidcount_ninety ~ var_bid + var_lag1 + var_lag2 + var_lag3 + var_lag4 + var_lag5 + 
  (1|participant_id) + (1|tradetime)

fvar31 <- bidcount_eighty ~ var_bid + (1|participant_id) + (1|tradetime)
fvar32 <- bidcount_eighty ~ var_bid + var_lag1 + (1|participant_id) + (1|tradetime)
fvar33 <- bidcount_eighty ~ var_bid + var_lag1 + var_lag2 + var_lag3 + var_lag4 + var_lag5 + 
  (1|participant_id) + (1|tradetime)

reg11 <- glmer(fvar11, data=df, family='poisson', na.action = na.omit)
reg12 <- glmer(fvar12, data=df, family='poisson', na.action = na.omit)
reg13 <- glmer(fvar13, data=df, family='poisson', na.action = na.omit)

reg21 <- glmer(fvar21, data=df, family='poisson', na.action = na.omit)
reg22 <- glmer(fvar22, data=df, family='poisson', na.action = na.omit)
reg23 <- glmer(fvar23, data=df, family='poisson', na.action = na.omit)

reg31 <- glmer(fvar31, data=df, family='poisson', na.action = na.omit)
reg32 <- glmer(fvar32, data=df, family='poisson', na.action = na.omit)
reg33 <- glmer(fvar33, data=df, family='poisson', na.action = na.omit)

#summary(reg1)
stargazer(reg11, reg12, reg13, reg21, reg22, reg23, reg31, reg32, reg33,
          dep.var.labels.include=FALSE, dep.var.caption='$No.\\;of\\;Bid\\;Orders_{i, p, j, t}$', 
          covariate.labels = 
            c("$\\Delta var_{i, p, j, t}$", "$\\Delta var_{i, p, j, t-1}$",
              "$\\Delta var_{i, p, j, t-2}$", "$\\Delta var_{i, p, j, t-3}$",
              "$\\Delta var_{i, p, j, t-4}$", "$\\Delta var_{i, p, j, t-5}$", 'Constant'),
          column.labels=c('$Market\\;bids_{p, j, t}$', '$Market\\;bids_{p, j, t}$ < 0.9', '$Market\\;bids_{p, j, t}$ < 0.8'),
          column.separate = c(3, 3, 3),
          title='Regression 3', align=TRUE, no.space=TRUE,
          add.lines = list(c("Individual Fixed Effects", "Yes", "Yes", "Yes", "Yes", 
                             "Yes", "Yes", "Yes", "Yes", "Yes"),
                           c("Time Fixed Effects", "Yes", "Yes", "Yes", "Yes", 
                             "Yes", "Yes", "Yes", "Yes", "Yes")),
          column.sep.width="-20pt", omit.stat=c("ser"), star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg3.1a.tex')

stargazer(reg13, dep.var.labels.include=FALSE, dep.var.caption='$No.\\;of\\;Bid\\;Orders_{i, p, j, t}$',
          title='Regression 3', align=TRUE, no.space=TRUE,
          covariate.labels = c("$\\Delta var_{i, p, j, t}$", "$\\Delta var_{i, p, j, t-1}$",
              "$\\Delta var_{i, p, j, t-2}$", "$\\Delta v ar_{i, p, j, t-3}$",
              "$\\Delta var_{i, p, j, t-4}$", "$\\Delta var_{i, p, j, t-5}$", 'Constant'),
          add.lines = list(c("Individual Fixed Effects", "Yes"),
                           c("Time Fixed Effects", "Yes")),
          column.sep.width="-50pt", omit.stat=c("ser"), star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg3.1.tex')

rm(list=ls())

#Set working directory
setwd("C:/Users/minshiuangl/Downloads/")

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
df$sec_complexity <- factor(df$sec_complexity, ordered= FALSE)

df$askcount_improve <- df$askcount*df$negative_var
df$askcount_ten <- df$askcount*df$negative_var*df$ten
df$askcount_twenty <- df$askcount*df$negative_var*df$twenty

#Create Lag terms
lag <- c("var_ask")
setDT(df)[,c("var_lag1", "var_lag2", "var_lag3", "var_lag4", "var_lag5") := shift(.SD, 1:10), 
          keyby = c("problem", "participant_id", "security"), .SDcols = lag]

#Regression 1.2
fvar11 <- askcount_improve ~ var_ask + (1|participant_id) + (1|tradetime)
fvar12 <- askcount_improve ~ var_ask + var_lag1 + (1|participant_id) + (1|tradetime)
fvar13 <- askcount_improve ~ var_ask + var_lag1 + var_lag2 + var_lag3 + var_lag4 + var_lag5 + 
  (1|participant_id) + (1|tradetime)

fvar21 <- askcount_ten ~ var_ask + (1|participant_id) + (1|tradetime)
fvar22 <- askcount_ten ~ var_ask + var_lag1 + (1|participant_id) + (1|tradetime)
fvar23 <- askcount_ten ~ var_ask + var_lag1 + var_lag2 + var_lag3 + var_lag4 + var_lag5 + 
  (1|participant_id) + (1|tradetime)

fvar31 <- askcount_twenty ~ var_ask + (1|participant_id) + (1|tradetime)
fvar32 <- askcount_twenty ~ var_ask + var_lag1 + (1|participant_id) + (1|tradetime)
fvar33 <- askcount_twenty ~ var_ask + var_lag1 + var_lag2 + var_lag3 + var_lag4 + var_lag5 + 
  (1|participant_id) + (1|tradetime)

reg11 <- glmer(fvar11, data=df, family='poisson', na.action = na.omit)
reg12 <- glmer(fvar12, data=df, family='poisson', na.action = na.omit)
reg13 <- glmer(fvar13, data=df, family='poisson', na.action = na.omit)

reg21 <- glmer(fvar21, data=df, family='poisson', na.action = na.omit)
reg22 <- glmer(fvar22, data=df, family='poisson', na.action = na.omit)
reg23 <- glmer(fvar23, data=df, family='poisson', na.action = na.omit)

reg31 <- glmer(fvar31, data=df, family='poisson', na.action = na.omit)
reg32 <- glmer(fvar32, data=df, family='poisson', na.action = na.omit)
reg33 <- glmer(fvar33, data=df, family='poisson', na.action = na.omit)


#summary(reg1)
stargazer(reg11, reg12, reg13, reg21, reg22, reg23, reg31, reg32, reg33,
          covariate.labels = 
            c("$\\Delta var_{i, p, j, t}$", "$\\Delta var_{i, p, j, t-1}$",
              "$\\Delta var_{i, p, j, t-2}$", "$\\Delta var_{i, p, j, t-3}$",
              "$\\Delta var_{i, p, j, t-4}$", "$\\Delta var_{i, p, j, t-5}$", 'Constant'),
          dep.var.labels.include=FALSE, dep.var.caption='$No.\\;of\\;Ask\\;Orders_{i, p, j, t}$', 
          column.labels = c('$Market\\;asks_{p, j, t}$', '$Market\\;asks_{p, j, t}$ > 0.1', '$Market\\;asks_{p, j, t}$ > 0.2'), 
          title='Regression 3', align=TRUE, no.space=TRUE,
          column.separate = c(3, 3, 3),
          add.lines = list(c("Individual Fixed Effects", "Yes", "Yes", "Yes", "Yes", 
                             "Yes", "Yes", "Yes", "Yes", "Yes"),
                           c("Time Fixed Effects", "Yes", "Yes", "Yes", "Yes", 
                             "Yes", "Yes", "Yes", "Yes", "Yes")),
          column.sep.width="-20pt", omit.stat=c("ser"), star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg3.2a.tex')

stargazer(reg13, covariate.labels = c("$\\Delta var_{i, p, j, t}$", "$\\Delta var_{i, p, j, t-1}$",
              "$\\Delta var_{i, p, j, t-2}$", "$\\Delta var_{i, p, j, t-3}$",
              "$\\Delta var_{i, p, j, t-4}$", "$\\Delta var_{i, p, j, t-5}$", 'Constant'),
          dep.var.labels.include=FALSE, dep.var.caption='$No.\\;of\\;Ask\\;Orders_{i, p, j, t}$', 
          title='Regression 3', align=TRUE, no.space=TRUE,
          add.lines = list(c("Individual Fixed Effects", "Yes"),
                           c("Time Fixed Effects", "Yes")),
          column.sep.width="-50pt", omit.stat=c("ser"), star.char = c("+", "*", "**", "***"),
          star.cutoffs = c(0.1, 0.05, 0.01, 0.001),
          notes = c("+ p<0.1; * p<0.05; ** p<0.01; *** p<0.001"), 
          notes.append = F, out='reg3.2.tex')

rm(list=ls())

