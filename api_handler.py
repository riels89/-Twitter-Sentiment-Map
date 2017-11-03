'''
Created on Sep 22, 2017

@author: Riley
'''
import tweepy
from tweepy import OAuthHandler
import requests, json


consumer_key = "MNLSW7iOdXj9twapG9PhFBRI9"
consumer_secret = "eszoNctIFrBw0l70DImhj0U1W2PNiBz5OpsBthpBfuIt4MpXCx"
access_key = "4840275653-fdFnC6ntTdLqueaveb3BnVMXo6YCkoQEuOqcUuU"
access_secret = "LcSs0JVVMCChpHmXU2kNQww5dCb8oFGclK0KxZ2NvCCLn"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_api():
    
    return api

def get_auth():
    
    return auth