# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 23:22:25 2021

@author: Tibor
"""


import pandas as pd
from wlnupdates import Search,Wrapper
import time
import numpy as np




PATH="<INSERT YOUR PATH TO YOUR GENERATED FILE>"
readingListDF = pd.read_excel(PATH+"Reading list einträge.xlsx", sheet_name="List of Books")
readingListDF.reset_index(inplace=True)

novel_owned_list = readingListDF[["Title","index"]].values.tolist()
[x[0].encode('utf-8') for x in novel_owned_list]



# get a series ID for each title
data = Search()
Series_ID = []

print("crawling for titles")
# All possible relevant titles listed
for title in novel_owned_list:
    time.sleep(0.2)
    Series_ID.append([title[0],data.title_search(title[0], similarityNum=0, fullList=True),title[1]])


# Get the most relevant entry
Unique_series_ID = []
for entry in Series_ID:
    Unique_series_ID.append([entry[0],entry[1][0]["sid"],entry[2]])

data1 = Wrapper()
print("Getting data")
# Extract all data
for pos, val in enumerate(Unique_series_ID):
    time.sleep(0.3)
    Unique_series_ID[pos].append(data1.get_series_data(str(val[1])))
    

final_extracted_dict = {}
i=0
for entry in Unique_series_ID:
    #the result dict

    
    #get the metadata
    infos1 = entry[3]
    infos = infos1["data"]
    
    # get latest chapter/vol
    latest_chapter = infos["latest_chapter"]
    latest_chapter_published = infos["latest_published"]
    latest_volume = infos["latest_volume"]
    latest_volume_published = infos["most_recent"]
    original_status = infos["orig_status"]
    publish_date = infos["pub_date"]
    true_title = infos["title"]
    
    #get author/publisher data
    publisher_list =[]
    try:
        for pub in infos["publishers"]:    
            publisher_list.append(pub["publisher"])
    except:
        pass
    
    author_list =[]

    for pub in infos["authors"]:    
        author_list.append(pub["author"])

   
    # Get Release history 
    Release_list =[]
    try:
        for release in infos["releases"]:    
            Release_list.append(release["published"])
    except:
        pass
    
    chapter_list =[]
    try:
        for release in infos["releases"]:    
            chapter_list.append(release["chapter"])
    except:
        pass
    
    #tags and genres
    genre_list = []
    for entry1 in infos["genres"]:
        genre_list.append(entry1["genre"])
    
    tag_list = []
    for entry2 in infos["tags"]:
        tag_list.append(entry2["tag"])
    
    
    
    
    created_dict = {
        "index" : entry[2],
        "Original Title" : true_title,
        "Own title" : "",
        "Type": "",
        "Last Chapter read" : "",
        "original Status": original_status,
        "Latest Chapter released": latest_chapter,
        "Latest Chapter publish date": latest_chapter_published,
        "Last Volume read": "",
        "Latest Volume released" : latest_volume,
        "Latest Volume publish date" : latest_volume_published,
        "Last Read": "",
        "Times Read": "",
        "Current Status": "",
        "publishers" : publisher_list,
        "authors" : author_list,
        "first published": publish_date,
        "Reread?": "",
        "Rating /10": "",
        "Genres": genre_list,
        "Tags": tag_list,
        "Release History": Release_list,
        "Chapter list": chapter_list
        }
    final_extracted_dict[i] = created_dict
    i = i+1
# create DF from generated data
extractedDF = pd.DataFrame.from_dict(final_extracted_dict, orient='index')


# Bring Genres in first NF

lens = list(map(len, extractedDF['Genres'].values))
 
genreDF = pd.DataFrame({'index': np.repeat(
    extractedDF['index'], lens), 'Genres': np.concatenate(extractedDF['Genres'].values)})
 
# bring Tags in first NF

lens1 = list(map(len, extractedDF['Tags'].values))
 
TagDF = pd.DataFrame({'index': np.repeat(
    extractedDF['index'], lens1), 'Tags': np.concatenate(extractedDF['Tags'].values)})

# Bring Publishers in first NF 
lens2 = list(map(len, extractedDF['publishers'].values))
 
PublisherDF = pd.DataFrame({'index': np.repeat(
    extractedDF['index'], lens2), 'publishers': np.concatenate(extractedDF['publishers'].values)})

# Bring Authors in first NF

lens3 = list(map(len, extractedDF['authors'].values))
 
authorDF = pd.DataFrame({'index': np.repeat(
    extractedDF['index'], lens3), 'authors': np.concatenate(extractedDF['authors'].values)})


# Bring Release history in first NF

lens4 = list(map(len, extractedDF['Release History'].values))
 
releaseDF = pd.DataFrame({'index': np.repeat(
    extractedDF['index'], lens4), 'Release History': np.concatenate(extractedDF['Release History'].values), "Chapter List": np.concatenate(extractedDF['Chapter list'].values)})

# Bring Chapterlist in first NF

# lens5 = list(map(len, extractedDF['Chapter list'].values))
 
# chapterDF = pd.DataFrame({'index': np.repeat(
#     extractedDF['index'], lens5), 'Chapter list': np.concatenate(extractedDF['Chapter list'].values)})



# clean input
extractedDF= extractedDF.drop(columns=["Genres","Tags","publishers","authors","Release History","Chapter list"])

writer = pd.ExcelWriter(PATH+"Reading list_generiert.xlsx", engine='xlsxwriter')

extractedDF.to_excel(writer, sheet_name='List of books',index=False)

genreDF.to_excel(writer, sheet_name='Generated Genre List',index=False)

TagDF.to_excel(writer, sheet_name='Generated Tag List',index=False)

authorDF.to_excel(writer, sheet_name='Generated Author list',index=False)

PublisherDF.to_excel(writer, sheet_name='Generated Publisher list',index=False)

releaseDF.to_excel(writer, sheet_name='Generated Release History List',index=False)

#chapterDF.to_excel(writer, sheet_name='Generated Chapter History List',index=False)
writer.save()
