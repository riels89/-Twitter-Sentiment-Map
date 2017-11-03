'''
Created on Oct 21, 2017

@author: Riley
'''
import MySQLdb as mysql
import pandas
import matplotlib.pyplot as plt
#import concurrent.futures as ThreadPoolExecutor

from sentiment_analysis import sentiment_module as sent
host = "localhost"
user = "root"
password = "759778"
database = "twitter"

df = pandas.read_csv("state_table.csv")
df = [df["abbreviation"]]
locations = [item for sublist in df for item in sublist]

location_counter = {location : 0 for location in df[0]} 


db = mysql.connect(host,user,password,database)
db.set_character_set('utf8mb4')

cursor = db.cursor()

get_value = {"neg" : -1, "pos" : 1}
counter = 0


#pool = ThreadPoolExecutor.ThreadPoolExecutor(max_workers=10)
with db:
        cursor.execute("select table_id, tweet from tweet_info_all;")
        tweets = cursor.fetchall()
        
        
def calculate_sentiment(tweet):
    global counter
    sentiment , confidence = sent.sentiment(tweets[tweet][1])
    cursor.execute("update tweet_info_all set sentiment = %s, confidence = %s where table_id = %s;", (get_value[sentiment], confidence, tweets[tweet][0]))
    db.commit()
        
        
    counter+=1
    print(counter)
#107039
for tweet in range(0,len(tweets)):
    #ool.submit(calculate_sentiment(tweet))
    calculate_sentiment(tweet)
cursor.close()



#===============================================================================
# print (pandas.DataFrame(location_counter, index=[0]).to_string())
# plt.bar(range(len(location_counter)),location_counter.values(),align="center")
# plt.xticks(range(len(location_counter)), location_counter.keys())
# plt.show()
#===============================================================================













