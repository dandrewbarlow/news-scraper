#web requests
import requests
# regex
import re
# parser
from bs4 import BeautifulSoup
# creating csv files
import csv
# read json file for settings
import json

# a list of dicts containing news sites and the regex settings for getting their headlines
# headlines will be added to the dicts when parsed
websites = []
options = {}

# the actual function to scrape a website
def scrape(website):
    # user feedback
    print("> Scraping", website["name"])

    # download page
    page = requests.get( website["url"] )

    #c reate BeautifulSoup parsing object
    mySoup = BeautifulSoup( page.content, 'html.parser' )

    # use regex to get headlines
    pageHeadlines = mySoup.find_all( website["element"], class_ = re.compile( website["regex"] ) )

    # create empty array of headlines
    headlines = []

    # go through matched headlines
    for content in pageHeadlines:

        # exclude anything that includes the publication's name
        if ( content.get_text().find( website["name"] ) == -1):
            # add the headlines to the array
            headlines.append( content.get_text() )

    # return said array
    return headlines

# import the scraping info from a json file into the websites variable/array
def importSettings(filename):
    # tell the user whats goin on
    print("> Importing")

    # open the .json file with the given filename
    with open(filename) as file:
        #decode the json data into the data variable
        data = json.load(file)

        #go through the data and populate the websites array with the info
        for entry in data["websites"]:
            websites.append(entry)

        options = data["options"]

        file.close()

        return options

# export scraped data into a csv using the given filename
def export(filename):
    # User feedback
    print("> Exporting")

    # create a csvfile with given filename in write mode
    with open(filename, 'w') as csvfile:
        # the csv writer and it's various settings
        filewriter = csv.writer(
        csvfile,
        delimiter=',',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL)

        # Write the headings. For human readablity, removable for automation
        filewriter.writerow( [ 'Publication' , 'Headline' ] )
        # go through the websites, and through each websites headlines
        for website in websites:
            for headline in website["headlines"]:
                #write the website name and the headline
                filewriter.writerow( [ website[ "name" ] ,  headline ] )

#testing function
def printHeadlines(name):
    for website in websites:
        if (website["name"] == name):
            print(website["headlines"])

def main():

    options = importSettings('settings.json')

    for website in websites:
        website["headlines"] = scrape(website)


    export(options["outfile"])

main()
