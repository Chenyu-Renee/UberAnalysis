## UC Berkeley's Statistics Capstone
### Spring Term 2016 

_**Group members:**_ Xinyue Zhou, Siyao Chang, Chenyu Wang, Aksa Ahmad & Fengshi Niu 

_**Topic:**_ [An Exploratory Data Analysis of Uber Based on Twitter]


### Directions/Roadmap
1. __Want a result?__ - take a look at the conference poster under /poster folder.
2. __Want graphs?__ - go to /figures folder. The plots there are more complete than used in the poster.
3. __Want more data?__ - run the "script1-fetch" file under /code folder. You will get the most recent data about Uber on Twitter.
4. __Want analysis?__ - find the corresponding script under /code folder for part of the analysis.
5. __Want reproduce?__ - please ask one of the contributors for original dataset. And follow the further directions in Analysis section for reproducing.
6. __Want some slides?__ - go to the slide folder. There is a short representation there.



### Data

Our data is from Twitter API. You can download the real time data using [script1_fetch.py] under code folder. Unfortunately, this script can only give you the most recent Twitter data about Uber. If you want to reproduce the results presenting in this Github repository, please contact one of the contributor for the origin dataset. It is about 660MB.



### Analysis

Our project, in general, is composed of two steps. Firstly, extract data and data cleaning, which are accomplished sequentially by using script 2-11. Those scripts produce the intermediate files of cleaned data in /data under main repository. Secondly, we use the cleaned data in R for visualization, and generate the plots in /figures. The main point we do these is to take advantage of the visualization tools built in R and some R packages. You can get the plots by running "Plot" script 1-6.

### Figures

Our visualization results are put in this folder. You can find explanations in the poster.

### Poster

__'make'__ produces the full conference poster describing this research project.


### Contributers

Xinyue Zhou [z357412526] (https://github.com/z357412526)

Chenyu Wang [Chenyu-Renee] (https://github.com/Chenyu-Renee)

Siyao Chang [changsiyao] (https://github.com/changsiyao)

Aksam Ahmad 

Fengshi Niu 


Very special thanks to [Jarrod Millman] (https://github.com/jarrodmillman), for your teaching and your invaluable advice over the course of the semester — this project would not have been possible without your help!
