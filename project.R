setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
rm(list=ls())
library(tidyverse)
test1 = read_csv("test1.csv", col_names=F)
test1$X3 = (test1$X3-test1$X3[1])/60
test1$X4 = str_detect(test1$X2,"note")
test1$X5 = str_detect(test1$X2,"!songrequest|!skip")
for (i in 1:length(test1$X1)) {
  if (test1$X4[i] == T) {
    test1$X6[i] = "note"
  } 
  if (test1$X5[i] == T) {
    test1$X6[i] = "songrequest/skip"
  } 
  if (test1$X4[i] == F && test1$X5[i] == F) {
    test1$X6[i] = "bot responses"
  }
}
library(ggplot2)
p1 = ggplot(test1,aes(x=test1$X3,fill=test1$X6)) + 
  geom_histogram(binwidth=1) +
  theme(legend.title=element_blank()) +
  scale_y_continuous(breaks=seq(0,15,5),limits=c(0,15)) +
  xlab("minutes")

test2 = read_csv("test2.csv", col_names=F)
test2$X3 = (test2$X3-test2$X3[1])/60
test2$X4 = str_detect(test2$X2,"note")
test2$X5 = str_detect(test2$X2,"!songrequest|!skip")
for (i in 1:length(test2$X1)) {
  if (test2$X4[i] == T) {
    test2$X6[i] = "note"
  } 
  if (test2$X5[i] == T) {
    test2$X6[i] = "songrequest/skip"
  } 
  if (test2$X4[i] == F && test2$X5[i] == F) {
    test2$X6[i] = "bot responses"
  }
}
library(ggplot2)
p2 = ggplot(test2,aes(x=test2$X3,fill=test2$X6)) + 
  geom_histogram(binwidth=1) +
  theme(legend.title=element_blank()) +
  scale_y_continuous(breaks=seq(0,15,5),limits=c(0,15)) +
  xlab("minutes")

library(cowplot)
plot_grid(p1, p2, labels = c('A', 'B'), label_size = 12)

