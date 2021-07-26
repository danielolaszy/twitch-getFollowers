from dotenv import load_dotenv  # pip install python-dotenv
from ast import literal_eval # used to convert str to dict
import csv
import json
from requests.exceptions import HTTPError
import requests  # pip install requests
import os
import math
import datetime
startTime = datetime.datetime.now()
load_dotenv()

# Twitch API Authentication
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

try:
    def getAccessToken():
        request = 'https://id.twitch.tv/oauth2/token?client_id=' + client_id + '&client_secret=' + client_secret + '&grant_type=client_credentials'
        response = requests.post(request)
        jsonResponse = response.json()
        access_token = jsonResponse.get('access_token')
        return access_token

    headers = {'client-id': client_id, 'Authorization': 'Bearer ' + getAccessToken()}

    def getFollowing():
        username = str(input("Enter a twitch channel: "))
        while username == type(str):
            print('Invalid input, please try again.')
            username = str(input("Enter a twitch channel: "))
        return username

    def getFollower():
        username = str(input("Channel to filter: "))
        while username == type(str):
            print('Invalid input, please try again.')
            username = str(input("Channel to filter: "))
        return username

    def getUserId(username):
        print('Getting user ID for ' + username + '...')
        reqGetUserId = 'https://api.twitch.tv/helix/users?login=' + username
        respGetUserId = requests.get(reqGetUserId, headers=headers)
        jsonGetUserId = respGetUserId.json().get('data')[0]
        # print(json.dumps(jsonGetUserId, indent=4))  # Dump whole Jsonc
        # print(jsonGetUserId.get('id')) # Print only the user ID
        print('Found ID ' + str(jsonGetUserId.get('id')) + ' for ' + username + '!')
        return jsonGetUserId.get('id')
    
    def getUserTotalFollowers(userId):
        request = 'https://api.twitch.tv/helix/users/follows?to_id=' + str(userId) + '&first=1'
        response = requests.get(request, headers=headers)
        jsonResponse = response.json().get('total')
        return jsonResponse

    def getUserFollows(username):
        id = getUserId(username)
        pagination = ''
        print('Looking up ' + username + '\'s followers...')
        totalFollowers = getUserTotalFollowers(id)
        i = 0
        # f = open(username + ".json", "w")
        while i <= (math.floor(totalFollowers / 100)*100):
            request = 'https://api.twitch.tv/helix/users/follows?to_id=' + id + '&first=100' + pagination
            response = requests.get(request, headers=headers)
            responseHeaders = response.headers['Content-Type']
            if responseHeaders == "text/html":
                print("Response header content type is 'text/html'")
                continue
            else:
                jsonResp = response.json().get('data')
                # print("\n")
                pagination = '&after=' + str(response.json().get('pagination').get('cursor'))
                for user in jsonResp:
                    data = {
                    "id" : user.get('from_id'),
                    "user_login" : user.get('from_login'),
                    "followed_at" : user.get('followed_at')
                    }
                    with open(username + ".json", "a", encoding='utf-8') as f:
                        json.dump(data, f)
                        f.write('\n')
                    i += 1
                print('Found ' + str(i) + ' followers for ' + username + '...')

        print('Writing total followers of ' + str(totalFollowers) + ' to file...')
        f.close()

    def file_len(file_name):
        print("Counting total lines in " + file_name)
        with open(file_name) as f:
            for i, l in enumerate(f):
                pass
        print("Found a total number of " + str(i + 1) + " lines in " + file_name)
        return i + 1

    def followerPlacement(username, file):
        i=0
        fileLine = {}
        with open(file) as temp_f:
            datafile = temp_f.readlines()
        for line in datafile:
            i += 1
            if "\"" + username + "\"" in line:
                print("Found user " + username + " in " + file)
                fileLine = literal_eval(line), i # The string is found
                break
        fileTotalLines = file_len(file)
        fileUserLogin = fileLine[0]["user_login"]
        fileFollowedAt = fileLine[0]["followed_at"]

        delta = (fileTotalLines - i)

        data = {
            "follower" : fileUserLogin,
            "following" : file[:-5],
            "date" : fileFollowedAt,
            "n" : delta + 1,
            "total" : fileTotalLines,
        }
        print(username + " is follower #" + str(delta + 1) + " of " + file[:-4] + "\n")
        with open("follows.json","a") as f:
            json.dump(data, f)
            f.write('\n')

    def readChannelsFile():
        try:
            with open('channels.csv') as f:
                reader = csv.reader(f)
                data = list(reader)
            return data[0]
        except:
            print("Failed to read channels.csv, make sure you are in the right directory.")

        
    def main():
        channels = readChannelsFile()
        searchUser = getFollower()
        for channel in channels:
            # channelName = getFollowing()
            getUserFollows(channel)
            followerPlacement(searchUser, channel + ".json")

    main()

    print(datetime.datetime.now() - startTime)
except HTTPError as http_err:
    print(http_err)
except Exception as err:
    print(err)
