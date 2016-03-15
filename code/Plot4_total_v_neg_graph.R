library(ggplot2)
library(reshape2)
library(grid)

data <- read.csv("../data/total_neg_tweets.csv")
data$Date=strptime(data$Date,format = "%Y-%m-%d %H:%M")

time1 = data$Date[1]
time2 = data$Date[25]
time3 = data$Date[49]
time4 = data$Date[73]
time5 = data$Date[97]
time6 = data$Date[121]
time7 = data$Date[145]
time8 = strptime('2016-02-01 00:00',format = "%Y-%m-%d %H:%M")

test_data <- data.frame(
  Date = data$Date,
  Total = data$Total,
  Negative = data$Negative)

test_data_long <- melt(test_data, id="Date")  # convert to long format

p1 = ggplot(data=test_data_long,
            aes(x=Date, ymin=0, ymax=value, fill=variable)) + 
  geom_line(data=test_data_long,aes(x=Date, y=value, color=variable)) 
p1 = p1 + geom_vline(xintercept = as.numeric(as.POSIXct(time1)),size = 0.5, color = "white") +
  theme(axis.title.y = element_text(size = rel(1), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1), angle = 00))
p1 = p1 + geom_vline(xintercept = as.numeric(as.POSIXct(time3)),size = 0.5, color = "white") +
  theme(axis.title.y = element_text(size = rel(1), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1), angle = 00))
p1 = p1 + geom_vline(xintercept = as.numeric(as.POSIXct(time5)),size = 0.5, color = "white") +
  theme(axis.title.y = element_text(size = rel(1), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1), angle = 00))
p1 = p1 + geom_vline(xintercept = as.numeric(as.POSIXct(time7)),size = 0.5, color = "white") +
  theme(axis.title.y = element_text(size = rel(1), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1), angle = 00))
p1 = p1 + geom_ribbon(alpha=0.8)
p1 = p1 + ggtitle("Total vs Negative Tweets") + ylab("Number of Tweets") + theme(plot.title = element_text(face='bold', size = 18))

change_label <- function(x){
  return(c('Jan 25','Jan 26','Jan 27','Jan 28','Jan 29','Jan 30','Jan 31','Feb 01'))
}
xlabel <- as.POSIXct(c(unique(substr(test_data_long$Date, 1, 10)),"2016-02-01"))

p1 = p1 + scale_x_datetime(breaks=xlabel, labels=change_label) 
p1
p1 = p1 + scale_color_manual(values=c("dodgerblue1", "hotpink")) + scale_fill_manual(values=c("dodgerblue1", "hotpink")) 

p1 = p1 + ggplot2::annotate("text", label="Paris protest", 
                    x=as.POSIXct(time6), y=220, 
                    size=5.5, fontface="bold")

p1 + geom_segment(aes(x=as.POSIXct(time5), xend=as.POSIXct(time3), y=220, yend = 220),
                 data = test_data_long,
                 color="black", arrow=arrow(length=unit(.2, "cm"))) 

ggsave('total_v_neg.png', dpi=600)
