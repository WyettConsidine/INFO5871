library(arules)
library(tidyverse)
library(arules)
library(stringr)
install.packages('arulesViz')
library(arulesViz)



setwd("C:\\Users\\wyett\\OneDrive\\Documents\\INFO5871\\Assignment1") #to set the new working Directory
data <- read.csv('resourceFiles\\tfidfData.csv')
head(data)


transtotal <- arules::read.transactions("CSCI5502/AIInGreenTechSus/cleanedCompedData.csv",
                  rm.duplicates = TRUE, 
                  format = "basket",  ##if you use "single" also use cols=c(1,2)
                  sep=" ",  ## csv file
                  cols=NULL) ## The dataset has no row numbers

print(typeof(transtotal))

rules = arules::apriori(transtotal, parameter = list(support = 0.2,confidence = 0.6), maxlen=5)
print(length(rules))
rules <- subset(rules, subset = arules::size(arules::lhs(rules)) != 0)
print(arules::inspect(rules))

plot(rules, method="graph")
