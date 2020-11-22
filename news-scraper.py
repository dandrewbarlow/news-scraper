#! /usr/local/bin/python3

# Andrew Barlow
# https://github.com/dandrewbarlow/news-scraper
# A python program to scrape news sites and practice my python skills on

# LIBRARIES ========================================================
#web requests
import requests

# regex
import re

# parser
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
# creating csv files
import csv

# Allow naming for current date
from datetime import date

# read json file for settings
import json
# so we can export the csv with a date to keep files unique
from datetime import date

# for console arguments and general os stuff
import sys
import os

# rich console output
from rich.console import Console
console = Console()
from rich.prompt import *
from rich.traceback import install
install()

# A lot of functionality exists in this module, worth looking into
# Newspaper3k

# GLOBAL VARS ========================================================
# a list of dicts containing news sites and the regex settings for getting their headlines
# headlines will be added to the dicts when parsed
websites = []

# a dict of settings and their value. Currently only the output directory
options = {}

# FUNCTIONS ========================================================
def help():
    console.print("[bold purple]News Scraper[/bold purple] by [blue underline link=https://github.com/dandrewbarlow]Andrew Barlow[/blue underline link]")
    console.print("[yellow]usage[/yellow] ./news-scraper.py \[options]")
    console.print("-run with no arguments to use CLI")
    console.print("-use settings.json to configure. The version in the repo at [blue underline link=https://github.com/dandrewbarlow/news-scraper]github.com/dandrewbarlow/news-scraper[/blue underline link] has been made by me with some common news sites, but you can change or add sites through this file, as well as setting the output file name")
    console.print("[bold yellow]options[/bold yellow]")
    console.print("[yellow]-h[/yellow] print help information (this text)")
    console.print("[yellow]-y[/yellow] bypass scraping confimation")

# the actual function to scrape a website
def scrape(website):

    # user feedback
    console.print("scraping [yellow]" + website["name"] + "[/yellow]")

    # download page
    page = requests.get( website["url"] )

    # create BeautifulSoup parsing object
    mySoup = BeautifulSoup( page.content, 'html.parser' )

    # use regex to get any matched content
    matchedContent = mySoup.find_all( website["element"], class_ = re.compile( website["regex"] ) )

    # create empty array of headlines
    headlines = []

    # marker to show whether or not any valid headlines were found
    success = False

    # go through matched headlines
    for content in matchedContent:

        # exclude anything that includes the publication's name && the wsj error message
        if ( ( content.get_text().find( website["name"] ) == -1 ) and
        ( content.get_text().find( "We can’t find the page you're looking for") == -1) ):

            # add the headlines to the array
            headlines.append( content.get_text() )
            success = True

    # notify user if no headlines are scraped
    if (success == False):
        console.print("[bold red]ERROR[/bold red] Failed to scrape content: [bold yellow]" + website["name"] + "[/bold yellow]")

    # return said array
    return headlines


# import the scraping info from a json file into the websites variable/array
def importSettings(filename):

    # tell the user whats goin on
    console.print("[purple]Importing settings[/purple]")

    # open the .json file with the given filename
    with open(filename) as file:

        # decode the json data into the data variable
        data = json.load(file)

        # go through the data and populate the websites array with the info
        for entry in data["websites"]:
            websites.append(entry)

        # create a local options variable with the json settings
        options = data["options"]

        # close the json file
        file.close()

        # return the options (they are put in the global options var in main)
        return options


# export scraped data into a csv using the given filename
def export(options):
    # User feedback
    console.print("[purple]Exporting[/purple]")

    try:
        assert options["filetype"] == "csv"
    except:
        console.print("CSV is currently the only supported filetype")
        console.print("[red]exiting[/red]")
        exit(code=1)

    if "results" not in os.listdir():
        os.mkdir("results")
    
    # create a csvfile with given filename and current date in write mode
    with open("results/" + options["outfile"] + "-" + str( date.today() ), 'w') as csvfile:
        # the csv writer and it's various settings
        filewriter = csv.writer(
        csvfile,
        delimiter=',',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL)

        # Write the headings. For human readablity, removable for automation
        filewriter.writerow( [ 'Publication' , 'Headline' ] )

        # go through the websites
        for website in websites:

            # go through each website's headlines
            for headline in website["headlines"]:

                # write the website name and the headline
                filewriter.writerow( [ website[ "name" ] ,  headline ] )

        # close the out file
        csvfile.close()

        # not super neccessary, but makes me feel good
        return


# testing function
def printHeadlines(name):

    for website in websites:

        if (website["name"] == name):
            console.print(website["headlines"])

# MAIN ========================================================
def main():
    
    if "-h" in sys.argv:
        help()
        exit(code=1)

    if "-y" in sys.argv:
        confirmation = True
    else:
        confirmation = Confirm.ask("[blue underline]Proceed to scrape headlines?[/blue underline]")

    if confirmation == False:
        exit(code=1)

    # import the options
    options = importSettings('settings.json')

    # scrape headlines from all the websites
    for website in websites:
        website["headlines"] = scrape(website)

    # export headlines to the outfile
    export(options)


# grip it & rip it
main()