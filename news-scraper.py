'''
Andrew Barlow
Python Web Scraper
8/13/20

github.com/dandrewbarlow/news-scraper

Made for grabbing news headlines, but also made modular enough that it could easily be repurposed.
Check out the README for high level info, but there shouldn't be any surprises in the code.
Lots of comments, no weird tricks, this was also an excersise in trying to write good code,
so I tried to make it pretty.
'''


# web requests
# https://2.python-requests.org/en/master/
import requests
# parser
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
# regular expressions (regex)
import re
# creating csv files
import csv
# read json file for settings
import json
# so we can export the csv with a date to keep files unique
from datetime import date

# a list of dicts containing news sites and the regex settings for getting their headlines
# headlines will be added to the dicts when parsed
websites = []

# a dict of settings and their value. Currently only the output directory
options = {}


# the actual function to scrape a website
def scrape(website):

    # user feedback
    print("> Scraping", website["name"])

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
        print("ERROR: Failed to scrape content (", website["name"], ")")

    # return said array
    return headlines


# import the scraping info from a json file into the websites variable/array
def importSettings(filename):

    # tell the user whats goin on
    print("> Importing")

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
def export(filename):

    # User feedback
    print("> Exporting")

    # create a csvfile with given filename in write mode
    with open(filename + '-' + date.today().strftime("%m-%d-%Y") + '.csv', 'w') as csvfile:

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

            print(website["headlines"])


# main function
def main():
    # import the options
    options = importSettings('settings.json')

    # scrape headlines from all the websites
    for website in websites:
        website["headlines"] = scrape(website)

    # export headlines to the outfile
    export(options["outfile"])


# grip it & rip it
main()
