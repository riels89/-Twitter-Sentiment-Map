'''
Created on Oct 30, 2017

@author: Riley
'''
import MySQLdb as mysql
import pandas

host = "localhost"
user = "root"
password = "759778"
database = "twitter"

df = pandas.read_csv("state_table.csv")
df = [df["abbreviation"]]
locations = [item for sublist in df for item in sublist]

location_sentiment = {location : 0 for location in df[0]} 
location_confidence = {location : 0 for location in df[0]} 
db = mysql.connect(host,user,password,database)
db.set_character_set('utf8mb4')

cursor = db.cursor()

with db:
    for location in locations:
        cursor.execute("select sentiment, confidence from tweet_info_all where state = %s;", [location])
        sentiments, confidences = zip(*cursor.fetchall())
        location_sentiment[location] = sum(sentiments) / float(len(sentiments))
        location_confidence[location] = sum(confidences) / float(len(confidences))
        cursor.execute("insert into average_state_sentiment (state, sentiment, confidence) values (%s,%s,%s);",[location, location_sentiment[location], location_confidence[location]])
        db.commit()

print (sum(location_sentiment.values()) / float(len(location_sentiment)))
print (sum(location_confidence.values()) / float(len(location_confidence)))
