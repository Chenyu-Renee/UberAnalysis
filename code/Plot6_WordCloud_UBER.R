library('tm')
library('wordcloud')
library('SnowballC')

## Must create a folder called "UBERLOGO" and place the exported
## textfile of exported tokens

uberlogo <- Corpus(DirSource("UBERLOGO/"))
# inspect(uberlogo)

uberlogo <- tm_map(uberlogo, stripWhitespace)
uberlogo <- tm_map(uberlogo, content_transformer(tolower))
uberlogo <- tm_map(uberlogo, removeWords, stopwords("english"))
uberlogo <- tm_map(uberlogo, stemDocument)

uberlogo <- tm_map(uberlogo, removeWords, c("uber", "new", "n't", 
                                            "logo","logos"))

wordcloud(uberlogo, scale=c(4.5,0.5), max.words=75, random.order=FALSE, 
          rot.per=0.35, use.r.layout=FALSE, colors=brewer.pal(6, "Dark2"))