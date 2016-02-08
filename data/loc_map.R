library(maps)
library(grid)
library(gridExtra)
library(ggplot2)
library(ggmap)
library(plyr)
library(XML)
library(curl)

city_state <-  read.csv("city_state.csv", header=TRUE)
data_keywords<-  read.csv("keywordsInfo.csv", header=TRUE)
data_state_ref <- read.csv("ref_state.csv", header=TRUE)
colnames(data_state_ref) <- c("ind", "STATE","region")
data1 = read.csv("location_usa.csv", header=TRUE)
data2 = read.csv("location.csv", header=TRUE)
data3 = data2
data3$CITY =as.character(data3$CITY)
data3 = data3[data3$CITY != "",] #only city data
summary(data2)

#ggplot of freq
theTable = data2[complete.cases(data2),]
theTable <- within(data2, STATE <- factor(STATE, 
    levels=names(sort(table(STATE), 
      decreasing=FALSE))))
p1<- ggplot(subset(theTable, STATE %in% c("ca","ny","tx","fl","il","oh"))
       , aes(factor(STATE),fill=STATE))+
  scale_fill_brewer(palette="Blues")+
  geom_bar()+
  labs(x="States")+
  ggtitle("Frequency of Tweets by State")+ 
  theme(plot.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=20, hjust=0))+
  theme(axis.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=15))+
  theme(text = element_text(size=20))+
  coord_flip()
p1

data3 <- within(data3, STATE <- factor(STATE, levels=names(sort(table(STATE), decreasing=FALSE))))
p2<-ggplot(subset(data3, STATE %in% c("ca","ny","tx","fl","il","oh"))
       , aes(factor(STATE),fill=CITY))+
  geom_bar()+
  labs(x="States")+
  ggtitle("Frequency of Tweets by State & City")+ 
  theme(plot.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=20, hjust=0))+
  theme(axis.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=15))+
  theme(text = element_text(size=20))+
  coord_flip()+
  guides(col = guide_legend(ncol = 2,byrow=TRUE))
p2

us_state_map <- map_data('state')
tmp<- merge(data_state_ref,us_state_map,by = 'region')
tmp<- tmp[,c(3,4,5,6,7)]

#turn the data into a freq table
merge1 = count(data2, "STATE")
map_data <- merge(merge1, tmp, by = 'STATE')
map_data <- arrange(map_data, order)

states <- data.frame(state.center, state.abb)
data_keywords$STATE = sapply(data_keywords$STATE,casefold,upper=TRUE)
colnames(data_keywords) = c("X","KEYWORD","state.abb" )
#sort keywords
data_keywords = data_keywords[order(data_keywords$state.abb),]
states = states[order(states$state.abb),]

state_keyword <- merge(x = states,y = data_keywords, by="state.abb", all.x=TRUE)
state_keyword$state.abb = paste(state_keyword$state.abb,":",state_keyword$KEYWORD)


p5 <- ggplot(data = map_data, aes(x = long, y = lat, group = group))+
  geom_polygon(aes(fill = 10-log(freq)))+
  geom_path(colour = 'white')+
  coord_map()+
  geom_text(data = state_keyword, aes(x = x, y = y, label = state.abb, group = NULL), size = 4, colour="gray")+
  theme_bw()+
  ggtitle("Frequency of Tweets by States before Normalization")+
  theme(text = element_text(size=20))+
  guides(fill=FALSE)
p5

#after normalization of population
URL <-"http://www.infoplease.com/us/states/population-by-rank.html"
html<- readLines(curl(URL))
tbls<-readHTMLTable(html)
sapply(tbls,nrow)
popu<- tbls$ipContentTable
colnames(popu) <- c("index","region","population")
popu$region <- sapply(popu$region,casefold)
popu$population <- as.integer(gsub(",", "", popu$population, fixed = TRUE))
merge2<- merge(x = data_state_ref, popu, by="region")
merge2 <- merge(merge2,merge1, by="STATE")

map_data2 <- merge(merge2, tmp, by = 'STATE')
map_data2 <- arrange(map_data2, order)
map_data2 <-cbind(map_data2, nmlz<-map_data2$freq/map_data2$population*10000000)

p6 <- ggplot(data = map_data2, aes(x = long, y = lat, group = group))+
  geom_polygon(aes(fill = 10-log(nmlz)))+
  geom_path(colour = 'white')+
  coord_map()+
  geom_text(data = state_keyword, aes(x = x, y = y, label = state.abb, group = NULL), size = 4, colour="gray")+
  theme_bw()+
  ggtitle("Frequency of Tweets by States and Keyword after Normalization")+
  theme(text = element_text(size=20))+
  guides(fill=FALSE)
p6

#city heat map
map<- get_map(location="USA",zoom=4,maptype = "hybrid")
MapIt <- ggmap(map)
MapIt

#prepare coord
city_coor <- us.cities
city_coor$name <- sapply(substr(city_coor$name, 1, nchar(city_coor$name)-3),casefold)
city_coor$country.etc <- sapply(substr(city_coor$country.etc, 1, nchar(city_coor$name)-3),casefold)
colnames(city_coor) <- c("CITY","STATE","pop","lat","long","capital")

#prepare freq
tmp2 = count(data2,c("CITY","STATE"))

              data_coord_city <- merge(x=data_city,city_coor,by=c("CITY","STATE"), all.x=TRUE)
              tmp2 = count(data_coord_city, c("CITY","STATE"))
              data_city_final<- merge(tmp2,data_coord_city,by=c("CITY","STATE"))
              data2 = data2[order(data2$CITY,data2$STATE),]
              data_city_final = data_city_final[order(data_city_final$CITY,data_city_final$STATE),]
              data_city_final <- merge(data2,data_city_final,by=c("CITY","STATE"),all.x=TRUE)
              unique(data_city_final)

#finally, select that 30 cities
tmp3<-merge(city_state[order(city_state$STATE,city_state$CITY),],tmp2[order(tmp2$STATE,tmp2$CITY),])
final_city<- merge(tmp3,city_coor[order(city_coor$STATE,city_coor$CITY),])


MapIt + geom_point(aes(x=long, y=lat, size = freq), col = "red",data = final_city, alpha=0.6) +
  ggtitle("Frequency of Tweets by City")+
  theme(text = element_text(size=20))+
  geom_text(data = final_city, aes(x = long, y = lat, label = CITY, group = NULL), colour="grey", alpha=1)
  
