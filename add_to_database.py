'''
Created on Oct 2, 2017

@author: Riley
'''
import MySQLdb as mysql
host = "localhost"
user = "root"
password = "759778"
database = "twitter"

db = mysql.connect(host,user,password,database)
db.set_character_set('utf8mb4')

cursor = db.cursor()

cursor.execute('SET NAMES utf8mb4 ;')
cursor.execute('SET CHARACTER SET utf8mb4 ;')
cursor.execute('SET character_set_connection=utf8mb4 ;')
cursor.execute('SET character_set_server = utf8mb4')
#cursor.execute('SET COLLATE utf8_general_ci;')

def add(user_id, tweet, sentiment, confidence, state):
    with db:
        #print("insert into tweet_info(id, tweet, sentiment, confidence, state)values(%s, %s, %s, %s, %s);", (user_id, tweet, sentiment, confidence, state))
        cursor.execute("insert into tweet_info(id, tweet, sentiment, confidence, state)values(%s, %s, %s, %s, %s);", (user_id, tweet, sentiment, confidence, state))
