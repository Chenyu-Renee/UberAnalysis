library(ggplot2)
library(plyr)
library(gridExtra)
library(grid)
require("lubridate")
setwd("~/Desktop/TwitterProject/")

hashtags <- read.csv("token_timeseries.csv")
hashtags$X.taxi = hashtags$X.taxi + hashtags$X.Taxi
hashtags$X.logo = hashtags$X.logo + hashtags$X.design + hashtags$X.uberlogo
hashtags$X.SuperBowl50 = hashtags$X.SuperBowl50 + hashtags$X.SB50

hashtags$X.Taxi <- NULL
hashtags$X.design <- NULL
hashtags$X.uberlogo <- NULL
hashtags$X.SB50 <- NULL

colnames(hashtags) = c("Date", "taxi", "logo", "SuperBowl50", "Paris")
hashtags$Date=strptime(hashtags$Date,format = "%Y-%m-%d %H:%M")

#hashtags$taxi = log(hashtags$taxi + 1)
#hashtags$Paris = log(hashtags$Paris + 1)
#hashtags$SuperBowl50 = log(hashtags$SuperBowl50 + 1)
#hashtags$logo = log(hashtags$logo + 1)
time1 = hashtags$Date[168]
time2 = hashtags$Date[1]

# multiple lines
p1 = ggplot(data = hashtags, aes(x=Date, y=taxi)) + 
  geom_bar(stat="identity", color="aquamarine3")  +
  theme(axis.title.y = element_text(size = rel(1.8), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1.8), angle = 00))
p2 = ggplot(data = hashtags, aes(x=Date, y=logo)) +
  geom_bar(stat="identity", colour="cadetblue2")
p2 = p2 + geom_vline(xintercept = as.numeric(as.POSIXct(time1)),size = 2, color = "cadetblue4") +
  theme(axis.title.y = element_text(size = rel(1.8), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1.8), angle = 00))
          
p3 = ggplot(data = hashtags, aes(x=Date, y=SuperBowl50)) +
  geom_bar(stat="identity",color="azure4") +
  theme(axis.title.y = element_text(size = rel(1.8), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1.8), angle = 00))
p4 = ggplot(data = hashtags, aes(x=Date, y=Paris)) +
  geom_bar(stat="identity",color="goldenrod1") +
  theme(axis.title.y = element_text(size = rel(1.8), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1.8), angle = 00))
p4 = p4 + geom_vline(xintercept = as.numeric(as.POSIXct(time2)),size = 2, color = "blue4") 

grid.arrange(p1 + ggtitle("#taxi") + scale_y_continuous(limits = c(0, 130)),
             p2 + ggtitle("#logo") + scale_y_continuous(limits = c(0, 130)),
             p3 + ggtitle("#SuperBowl50") + scale_y_continuous(limits = c(0, 130)),
             p4 + ggtitle("#Paris") + scale_y_continuous(limits = c(0, 130)),
             nrow =2, 
             top = textGrob("Hashtags Frequency Trends",
                            gp = gpar(fontsize=29)) 
)

