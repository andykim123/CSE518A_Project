#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:05:48 2019

@author: dohoonkim
"""

'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys
import irc.bot
import requests
import info
import datetime
import csv
import numpy as np

#Class for TwitchBot with IRC bot open for connection Twitch server with our local server
class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.userDict = []
        self.lastUpdatedTime = datetime.datetime.now()

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        
#Request certain capabilities such as tags before using them
    def on_welcome(self, c, e):
        print('Joining ' + self.channel)
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

#Aggregate the user message or chat and put into corresponding key, which is user.
    def on_pubmsg(self, c, e):
        temp = e.source.split('!')
        if temp[0] == temp[1].split('@')[0]:
            username = temp[0]
            content = e.arguments[0]

            # Value in tmi-sent-ts is timestamp of the message
            for tag in e.tags:
                if tag['key'] == "tmi-sent-ts":
                    timestamp = tag['value']

            if content == "END":
                self.userDict.append(["END",content,np.round(int(timestamp)//1000)])
                with open("out.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(self.userDict)
            else:
                self.userDict.append([username,content,np.round(int(timestamp)//1000)]) 

        return

def main():
    if len(sys.argv) != 1:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username  = info.username
    client_id = info.client_id
    token     = info.oauth
    channel   = info.channel
    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()