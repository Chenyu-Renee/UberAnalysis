library(ggplot2)
library(scales)
setwd("~/Desktop/TwitterProject/")

nw <- read.csv('NegativeTweets.csv', head=F)
colnames(nw) = c("NegativeWords", "Frequency")
nwn <- nw[with(nw, order(nw$Frequency)),]

ggplot(nw, aes(x=nw$NegativeWords, y=nw$Frequency)) +
  geom_bar(stat='identity',fill = "aquamarine3") +
  coord_flip() +
  ggtitle("Most Common Negative Words Occured in Tweets") +
  scale_x_discrete(
    limits= nwn$NegativeWords) +
  ylab("Frequency") + 
  xlab("Most common negative words") + 
  theme(axis.text.y = element_text(angle = 00, hjust = 1, size=20,color="aquamarine4")) +
  theme(plot.title = element_text(lineheight=3, face="bold",color="aquamarine4", size=29)) +
  theme(axis.title.y = element_text(size = rel(1.8), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1.8), angle = 00))
