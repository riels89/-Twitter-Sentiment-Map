
'''
Created on Sep 5, 2017

@author: Riley
'''
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from html.parser import HTMLParser
import api_handler
import pandas
import traceback
#import matplotlib.pyplot as plt
import add_to_database as db


counter = 0
df = pandas.read_csv("state_table.csv")
df = [df["name"], df["abbreviation"]]
locations = [item for sublist in df for item in sublist]

name_to_abv = dict(zip(tuple(df[0]), tuple(df[1])))
abv_to_abv = dict(zip(tuple(df[1]), tuple(df[1])))
location_converter = {**abv_to_abv, **name_to_abv}

location_counter = {location : 0 for location in df[1]} 
unparseable = 0


#here if I ever need just the text of the tweet
def parse_tweet(text):
    
    print("before processing: ",text)
    if(text.startswith("RT")):
        text = text[3:]
    while text[0] == "@":
        text = text[text.find(" ")+1:]
    return text


class listener(StreamListener):
    
    def on_data(self, data):
        try:           
            data = json.loads(HTMLParser().unescape(data))
            location = data["user"]["location"]
            
            #parse location into something we can use
            if location is not None:
                parsed_location = [parsed_location for parsed_location in locations if parsed_location in location]
                if (len(parsed_location) == 0):
                    global unparseable
                    unparseable += 1
                    return True
                else:
                    parsed_location = location_converter[parsed_location[0]]
                    if location_counter[parsed_location] <3000:
                        global counter
                        counter+=1
                        print("Current counter: ", counter)
                        location_counter[parsed_location] += 1
                    else: return True
                    
            else: return (True)
            
            if(data['truncated']):
                text = data['extended_tweet']['full_text']
            elif 'retweeted_status' in data:
                if 'extended_tweet' in data['retweeted_status']:
                    text = data['retweeted_status']['extended_tweet']['full_text']
                else:
                    text = data['retweeted_status']['text']
            else: 
                text = data['text']
            id = data["user"]["id"]
            
            #add to data base with sentiment and confidence as None because we will process those later
            db.add(id, text, None, None, parsed_location)
            
            #===================================================================
            # if counter == 10000 :
            #         print (pandas.DataFrame(location_counter, index=[0]).to_string())
            #         plt.bar(range(len(location_counter)),location_counter.values(),align="center")
            #         plt.xticks(range(len(location_counter)), location_counter.keys())
            #         plt.show()
            #===================================================================
            return(True)
        
        except Exception as e:
            print ("Error: ", e)
            print(traceback.format_exc())
            
    def on_error(self, status):
        print (status)
        
try:
    twitterStream = Stream(api_handler.get_auth(), listener())
    #should make a thread pool rather than using async
    twitterStream.filter(track=["Trump"], async=True)
except Exception as e:
    print("Error")
    print(traceback.format_exc())
print ("Final counter: ", counter)
