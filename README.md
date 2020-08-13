# news-scraper
Learning to scrape news sites using python

Made in a \*NIX environment. You're welcome to try it in others, but I'm not prioritizing it

### Usage
I used a Makefile because they make everything easier. If you want to do things manually, all the relevant commands can be found in there.

Running `make install` in a terminal will install dependencies

Running `make` will run the program

Running `make clean` will remove any files created by the program

As of now, I have a json file with relevant information telling my program how to scrape headlines from various news sites. I hope to utilize the Newspaper3k library to ease the burden of doing this manually, but it's a good thing to know how to do. When the program is run, it will import the data from this json file, scrape the websites, and then export them to a .csv file
