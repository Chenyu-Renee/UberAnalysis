library('ggplot2')

df <- scan("dates.txt", what = " ", sep = "\n")

a = c("Tue Jan 26", "Wed Jan 27", "Thu Jan 28", "Fri Jan 29", "Sat Jan 30",
      "Sun Jan 31", "Mon Feb 01", "Tue Feb 02", "Wed Feb 03")

a1 = c("2016-01-26", "2016-01-27", "2016-01-28", "2016-01-29", "2016-01-30", 
       "2016-01-31", "2016-02-01", "2016-02-02", "2016-02-03")

b = rep(1, 9)
c = seq(1:9)

x <- table(df)

for (i in 1:length(a)) {
  b[i] = x[names(x)==a[i]]
}

uber <- data.frame(dates = a1,tweets = b, c)

# write.csv(counts, file = "datecounts.csv", row.names=FALSE)
# uber <- read.csv('datecounts.csv')

uber$dates <- as.Date(uber$dates)

layer_line <- geom_line(mapping = aes(x = dates, y = tweets), data = uber)
ggplot() + layer_line + ggtitle("Direct Tweets to @Uber") + 
  annotate("segment", x=as.Date('2016-01-31','%Y-%m-%d'), y=750, 
           xend=as.Date('2016-02-02','%Y-%m-%d'), yend=475, size=0.5, 
           arrow=arrow(length=unit(.2, "cm"))) + 
  annotate("text", label="Twitter announces logo change", 
           x=as.Date('2016-01-31','%Y-%m-%d'), y=780, 
           size=4, fontface="bold") + xlab("Date") +
  ylab("Number of Tweets")
