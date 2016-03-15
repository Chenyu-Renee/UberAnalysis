library('ggplot2')

df <- scan("dates.txt", what = " ", sep = "\n")
df2 <- scan("dates2.txt", what = " ", sep = "\n")
df3 <- append(df, df2)

a = c("Tue Jan 26", "Wed Jan 27", "Thu Jan 28", "Fri Jan 29", "Sat Jan 30",
      "Sun Jan 31", "Mon Feb 01", "Tue Feb 02", "Wed Feb 03", "Thu Feb 04",
      "Fri Feb 05", "Sat Feb 06", "Sun Feb 07", "Mon Feb 08", "Tue Feb 09",
      "Wed Feb 10", "Thu Feb 11", "Fri Feb 12", "Sat Feb 13")

a1 = c("2016-01-26", "2016-01-27", "2016-01-28", "2016-01-29", "2016-01-30", 
       "2016-01-31", "2016-02-01", "2016-02-02", "2016-02-03", "2016-02-04",
       "2016-02-05", "2016-02-06", "2016-02-07", "2016-02-08", "2016-02-09", 
       "2016-02-10", "2016-02-11", "2016-02-12", "2016-02-13")

b = rep(1, 19)
c = seq(1:19)

x <- table(df3)

for (i in 1:length(a)) {
  b[i] = x[names(x)==a[i]]
}

uber <- data.frame(dates = a1,tweets = b, c)

# write.csv(counts, file = "datecounts.csv", row.names=FALSE)
# uber <- read.csv('datecounts.csv')

uber$dates <- as.Date(uber$dates)

layer_line <- geom_line(mapping = aes(x = dates, y = tweets), data = uber, 
                        color = 'blue', lwd = 1.5)
ggplot() + layer_line + ggtitle("Direct Tweets to @Uber") + 
  ggplot2::annotate("segment", x=as.Date('2016-01-31','%Y-%m-%d'), y=750, 
           xend=as.Date('2016-02-02','%Y-%m-%d'), yend=475, size=0.5, 
           arrow=arrow(length=unit(.2, "cm"))) + 
  ggplot2::annotate("text", label="Uber changes logo", 
           x=as.Date('2016-01-30','%Y-%m-%d'), y=775, 
           size=5.5, fontface="bold") + 
  ylab("Number of Tweets") + 
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=16,face="bold"), 
        plot.title = element_text(size=22, face="bold"), 
        axis.title.x=element_blank(), 
        axis.text.x = element_text(angle = 45, hjust = 1))

ggsave('LogoAnnounce.png', dpi = 600)
