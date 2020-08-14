# news-scraper
Learning to scrape news sites using python

Made in a \*NIX environment. You're welcome to try it in others, but I'm not prioritizing it

### Usage
I used a Makefile because they make everything easier. If you want to do things manually, all the relevant commands can be found in there.

Running `make install` in a terminal will install dependencies

Running `make` will run the program

Running `make clean` will remove any files created by the program

* news-scraper.py
  * this is the main script, it contains the majority of functionality
* settings.json
  * I've tried to keep anything you might want to edit yourself in the json file, such as the output filename and the websites that need scraping.
* Makefile
  * Contains the commands used to run
* requirements.txt
  * Lists python libraries dependencies to be downloaded by pip
* headlines.csv
  * Default output file of scraped data
