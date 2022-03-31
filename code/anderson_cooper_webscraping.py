# libraries
import requests
from bs4 import BeautifulSoup
import os

# repo path
repo_path = os.path.dirname(os.getcwd())

# manually create list of urls for transcript pages since January 2020
url_list = [
    'https://transcripts.cnn.com/show/acd',
    'https://transcripts.cnn.com/show/acd?start_fileid=acd_2021-12-28_01',
    'https://transcripts.cnn.com/show/acd?start_fileid=acd_2021-08-20_01',
    'https://transcripts.cnn.com/show/acd?start_fileid=acd_2021-04-13_01',
    'https://transcripts.cnn.com/show/acd?start_fileid=acd_2020-12-08_01',
    'https://transcripts.cnn.com/show/acd?start_fileid=acd_2020-08-18_01',
    'https://transcripts.cnn.com/show/acd?start_fileid=acd_2020-04-20_01']

# create empty links list
links = []

# loop through urls, parse page, collect transcript links
for url in url_list:
    
    # parse transcript landing page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # find "bullet items" - segment transcripts by air date
    main = soup.find(id = 'cnnMainContent')
    sub = main.find_all(class_ = 'cnnSectBulletItems')
    
    # for each air date, collect transcript links for each segment
    for a in main.find_all('a', href = True): 
        if (a.text) and ('date' in a['href']):
            links += [a['href']]
    
# loop through links, parse page, collect transcript body text
# output text to file if length > 0 and does not contain 'did not air'
for link in links:

    # create transcript link
    url = 'https://transcripts.cnn.com' + link

    # parse transcript page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # find transcript body text
    main = soup.find(id = 'cnnMainContent')
    sub = main.find_all(class_ = 'cnnBodyText')
    
    # extract transcript body text
    transcript_text = sub[2].text
    
    # create file name based on transcript date and segment number
    filename = 'ac360_' + link.split('/')[4] + '_' + link.split('/')[6] + '_transcript.txt'
    output_path = os.path.join(repo_path, "data", "01-raw", "anderson_cooper", filename)

    # if text > 0 and does not contain 'did not air', write to text file
    if ('did not air' not in transcript_text.lower()) and (len(transcript_text) > 0):
        with open(output_path, 'w') as f:
            f.write(transcript_text)