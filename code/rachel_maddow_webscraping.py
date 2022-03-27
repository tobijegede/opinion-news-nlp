
'''
How to run this file on the command line:

$ python rachel_maddow_webscraping.py <insert number here> 

OR 

$ python3 rachel_maddow_webscraping.py <insert number here> 

For example: 
$ python rachel_maddow_webscraping.py 5 
$ python3 rachel_maddow_webscraping.py 5 

The number represents how many pages of information you need data for 

'''

#import required libraries
import requests
from bs4 import BeautifulSoup
import os
import sys #allows you to get command line arguments


#get command line arguments
args = sys.argv

#store the total number of pages for data (from March 2020 to March 2022)
#total_num_pages = 25 #need to edit this to your specifications!
total_num_pages = int(args[1])



#create the get transcript function
def get_transcript(search_url):
    '''
    Input: url (string): this is the link to the SEARCH LANDING PAGE (i.e. NOT the actually site that has the transcript text)
    Output: None (does not return anything but writes the text of the transript to a file)

    '''

    # ----------  GET TO THE WEBISTE & EXTRACT HTML
    #step 1: store the URL
    # "https://www.msnbc.com/transcripts/show/rachel-maddow-show?dateRange=2020-03-01+TO+2022-03-31"
    rachel_maddow_URL = search_url

    #step 2: get to the landing page of the website
    landing_page = requests.get(rachel_maddow_URL)

    #step 3: convert page into html
    soup = BeautifulSoup(landing_page.content, "html.parser")


    #------ PARSE THROUGH THE HTML
    #step 4: extract the transcript feed page part of the soup
    transcript_feed = soup.find(class_="transcripts-feed")

    #step 5: get all of the transcript cards -- creates an object that is iterable to look at
    transcript_cards = transcript_feed.find_all("div", class_ ="transcript-card")

    #step 6: terate through the all of the transcript cards on the page & extract the relevant information
    transcript_info = {} #key = air date, value is a dictionary with the (transcript url, guest, and text of the show)

    for card in transcript_cards: #all information is stored at the date level
        air_date = card.find("div", class_="transcript-card__air-date").text
        transcript_url = card.find("a", class_="transcript-card__show-name")["href"] #get the link for the website
        guests = card.find("span", class_="transcript-card__guests").text[8:].split(",")#removes a "guests:" tag from in front of the list of guests 

        transcript_info[air_date] = {"transcript_url": transcript_url,
                                    "guests": guests }

    # --- GET THE ACTUAL TRANSCRIPT TEXT

    #step 7: iterate through all of the air dates to get the actual text of the transcript + write the text to a file 
    for air_date in list(transcript_info.keys()):

        #get needed information
        show_url = transcript_info[air_date]["transcript_url"]
        #print(show_url)
        
        #go to the url
        show_page = requests.get(show_url)

        #convert the page into a soup object
        show_soup =  BeautifulSoup(show_page.content, "html.parser")

        #get the content of the transcript = <div class="article-body__content">

        #extract the transcript feed page part of the soup
        transcript_text = show_soup.find(class_="article-body__content").text

        #add the transcript text to the dictionary
        transcript_info[air_date]["transcript_text"] = transcript_text

    # --- NOW THAT WE HAVE THE ACTUAL TEXT OF THE TRANSCRIPT, EXPORT THIS TO A TEXT FILE
        
        #create a file name + output file path
        list_air_date = air_date.split()


        filename = list_air_date[0] + "_" + list_air_date[1] + "_" + list_air_date[2] + "_" + "rachel" + "_" + "maddow" + "_" + "transcript.txt"
        repo_path = os.path.dirname(os.getcwd())
        output_path = os.path.join(repo_path, "data", "01-raw", "rachel_maddow", filename)

        #print(output_path)

        #export the file
        with open(output_path,"w") as f:
            f.write(transcript_text)




#note: There is an if statement bc the URL is different for the first page
for i in range(total_num_pages):
    page_num = i + 1 

    if page_num == 1:
        URL = "https://www.msnbc.com/transcripts/show/rachel-maddow-show?dateRange=2020-03-01+TO+2022-03-31"

        #call transcripts function
        get_transcript(URL)


    else: 
        URL = "https://www.msnbc.com/transcripts/show/rachel-maddow-show?page="+ str(page_num) +  "&dateRange=2020-03-01+TO+2022-03-31"

        #call transcripts function
        get_transcript(URL)


