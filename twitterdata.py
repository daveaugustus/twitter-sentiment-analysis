import os
import sys
import yaml
import twitter

# Two way security
with open('/home/dave/route.yaml', 'r') as route_file:
    route = yaml.load(route_file, Loader=yaml.FullLoader)

with open(route['route_twitter'], 'r') as yaml_file:
    file = yaml.load(yaml_file, Loader=yaml.FullLoader)



consumer_key = file['consumer_key']
consumer_secret = file['consumer_secret']
access_token_key = file['access_token']
access_secret_key = file['access_secret']

api = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret,access_token_key = access_token_key, access_token_secret = access_secret_key)

print(api.VerifyCredentials())
