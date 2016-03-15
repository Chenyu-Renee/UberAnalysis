library(ggplot2)
library(gridExtra)
setwd("~/Desktop/TwitterProject/")

sp <- read.csv('surgepricing1.csv', head=T)
sp <- sp[-c(1:14,375:392), ]
# sp <- data[,c(1,10:13)]
sp$X.surgepricing = sp$X.surgepricing + sp$X.SurgePricing + sp$X.surge + sp$surge + sp$Surge
sp$X.SurgePricing <- NULL
sp$X.surge <- NULL
sp$surge <- NULL
sp$Surge <- NULL

colnames(sp) <- c("Date","surgepricing")
sp$Date=strptime(sp$Date,format = "%Y-%m-%d %H:%M")
sp$DateIn4HrG = strptime(
  paste0(
  format(sp$Date,'%Y-%m-%d '),
  as.integer(format(strptime(sp$Date,format = "%Y-%m-%d %H:%M"),'%H'))%/%4*4,
  ':00'
  ),format = "%Y-%m-%d %H:%M")


grouphour=function(date){
  hour=as.integer(format(date,'%H'))
  hrinterval=c()
  for (i in 1:length(hour)){
    if (hour[i]>=22 | hour[i] <2){
      hrinterval[i]= "22:00-02:00"
    }
    else if (hour[i]>=2 & hour[i] <6){
      hrinterval[i]= '02:00-06:00'
    }
    else if (hour[i]>=6 & hour[i] <10){
      hrinterval[i]= '06:00-10:00'
    }
    else if (hour[i]>=10 & hour[i] <14){
      hrinterval[i]= '10:00-14:00'
    }
    else if (hour[i]>=14 & hour[i] <18){
      hrinterval[i]= '14:00-18:00'
    }
    else if (hour[i]>=18 & hour[i] <22){
      hrinterval[i]= '18:00-22:00'
    }
  }
  return (hrinterval)
}
sp$Interval4Hr=grouphour(sp$Date)

ggplot(data = sp, aes(x=Date, y=surgepricing)) + 
  geom_bar(stat="identity",fill="dodgerblue2")  + 
  ylab("Surge pricing frequency") + 
  ggtitle("Surge Pricing Occurred Trends") +
  theme(plot.title = element_text(lineheight=3, face="bold",color="dodgerblue4", size=20)) +
  theme(axis.title.y = element_text(size = rel(1.5), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1.5), angle = 00))




p1 = ggplot(data = sp, aes(x=DateIn4HrG, y=surgepricing)) + 
  geom_bar(stat="identity",fill="dodgerblue1")  + 
  xlab("Date") +
  ylab("Surge pricing frequency") + 
  ggtitle("Surge Pricing Occurred Time Trends") +
  theme(plot.title = element_text(lineheight=3, face="bold",color="dodgerblue4", size=18)) +
  theme(axis.title.y = element_text(size = rel(1.0), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1.0), angle = 00))

ggsave(file="surge_timeseries.png",dpi=1000)

# spn <- sp[with(sp, order(sp$Frequency)),]

p2 = ggplot(data = sp, aes(x=Interval4Hr, y=surgepricing)) + 
  geom_bar(stat="identity",fill="lightpink1")  + 
  xlab("Time Period") +
  ylab("Surge pricing frequency") + 
  ggtitle("Surge Pricing Occurred Interval") +
  theme(plot.title = element_text(lineheight=3, face="bold",color="lightpink4", size=18)) +
  theme(axis.title.y = element_text(size = rel(1.0), angle = 90)) +
  theme(axis.title.x = element_text(size = rel(1.0), angle = 00))
# grid.arrange(p1, p2, nrow =1)

ggsave(file="surge_group.png",dpi=1000)
