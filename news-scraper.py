#web requests
import requests
# regex
import re
#parser
from bs4 import BeautifulSoup
#creating csv files
import csv
#read json file for news settings
import json

# a list of dicts containing news sites and the regex settings for getting their headlines
# headlines will be added to the dicts when parsed
websites = []


def scrape(url, regex, element):
    #download page
    page = requests.get( url )

    #create BeautifulSoup parsing object
    mySoup = BeautifulSoup( page.content, 'html.parser' )

    print(mySoup.get_text())

    #use regex to get headlines
    pageHeadlines = mySoup.find_all(element, class_ = re.compile(regex) )

    #create empty array of headlines & populate with text from parsed elements
    headlines = []

    for content in pageHeadlines:
        headlines.append( content.get_text() )

    return headlines

def importSettings(filename):
    with open(filename) as file:
        data = json.load(file)
        for entry in data:
            websites.append(entry)

def export(filename):
    with open(filename, 'w') as csvfile:
        filewriter = csv.writer(
        csvfile,
        delimiter=',',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL)

        filewriter.writerow( [ 'Publication' , 'Headline' ] )
        for website in websites:
            for headline in website["headlines"]:
                filewriter.writerow( [ website[ "name" ] ,  headline ] )

#testing function
def printHeadlines(name):
    for website in websites:
        if (website["name"] == name):
            print(website["headlines"])

def main():
    print(">IMPORTING")
    importSettings('websites.json')
    print(">SCRAPING")
    for website in websites:
        print(website["name"])
        website["headlines"] = scrape(website["url"], website["regex"], website["element"])

    printHeadlines("CNN")
    # print("EXPORTING")
    # export('headlines.csv')

main()
