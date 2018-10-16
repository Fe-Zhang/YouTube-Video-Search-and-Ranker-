from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import csv

DEVELOPER_KEY="AIzaSyDs3Wcv8GUdz4DbMzmDyKNW93OiHDUh9Ho" #Insert your API key here

def get50YT(query, token):
    youtube = build("youtube","v3",developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=query,type="video",pageToken=token,
                                            order="relevance",part="id,snippet",
                                            maxResults=50, #I think they capped max results
                                            location=None,
                                            locationRadius=None).execute()

    vids = []
    
    for search_result in search_response.get("items",[]):
        if search_result["id"]["kind"] == "youtube#video":
            stats = youtube.videos().list(part="statistics",id=search_result['id']['videoId']).execute()
            vids.append({'search': search_result, \
                         'stat': stats['items'][0]['statistics']['viewCount']})
    try:
        nextToken = search_response["nextPageToken"]
        return(nextToken, vids)
    except Exception as e:
        nextToken = "last_page"
        return (nextToken, vids)

def top100YT(query):
    result = get50YT(query, None)
    data = result[1] #Returns token and data, this seperates data
    listyt = []
    for entry in data:
        listyt.append({'Title': entry['search']['snippet']['title'], \
                      'Author': entry['search']['snippet']['channelTitle'], \
                      'Views': entry['stat'], \
                      'Description': entry['search']['snippet']['description']})
    result = get50YT(query, result[0])
    for entry in data:
        listyt.append({'Title': entry['search']['snippet']['title'], \
                      'Author': entry['search']['snippet']['channelTitle'], \
                      'Views': entry['stat'], \
                      'Description': entry['search']['snippet']['description']})
    return listyt


def writeToCSV(string, dicts):
    with open(string+'.csv','w') as filename:
        keys = dicts[0].keys()
        writer = csv.DictWriter(filename,fieldnames = keys, extrasaction='ignore',delimiter=',')
        writer.writerows(dicts)

#search and write AA speaker
AASpeakerList = top100YT("AA Speaker")
writeToCSV("AASpeakerFileAPI", AASpeakerList)
#search motivational speaker
motivationalSpeakerList = top100YT("Motivational Speaker")
writeToCSV("motivationalSpeakerFileAPI", motivationalSpeakerList)


        
