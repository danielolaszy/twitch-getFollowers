from dotenv import load_dotenv  # pip install python-dotenv
import json
import pprint 
from requests.exceptions import HTTPError
import requests  # pip install requests
import os
import datetime
startTime = datetime.datetime.now()
load_dotenv()

# Twitch API Authentication
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('ACCESS_TOKEN')
headers = {'client-id': client_id, 'Authorization': 'Bearer ' + access_token}

try:
    def getUserInput():
        username = str(input("Enter a twitch channel: "))
        while username == type(str):
            print('Invalid input, please try again.')
            username = str(input("Enter a twitch channel: "))
        getUserFollows(username)


    def getUserId(username):
        print('Getting user ID for ' + username + '...')
        reqGetUserId = 'https://api.twitch.tv/helix/users?login=' + username
        respGetUserId = requests.get(reqGetUserId, headers=headers)
        jsonGetUserId = respGetUserId.json().get('data')[0]
        print(json.dumps(jsonGetUserId, indent=4))  # Dump whole Json
        # print(jsonGetUserId.get('id')) # Print only the user ID
        print('Found ID ' + str(jsonGetUserId.get('id')) + ' for ' + username + '!\n')
        return jsonGetUserId.get('id')
    
    def getUserTotalFollowers(username):
        request = 'https://api.twitch.tv/helix/users/follows?to_id=' + str(getUserId(username)) + '&first=1'
        response = requests.get(request, headers=headers)
        jsonResponse = response.json().get('total')
        return jsonResponse

    def getUserFollows(username):
        id = getUserId(username)
        pagination = ''
        print('Looking up ' + username + '\'s followers...')
        totalFollowers = getUserTotalFollowers(username)
        i = 0
        f = open(username + ".txt", "w")
        while i <= totalFollowers:
            # print(totalFollowers)
            request = 'https://api.twitch.tv/helix/users/follows?to_id=' + id + '&first=100' + pagination
            response = requests.get(request, headers=headers)
            json = response.json().get('data')
            pagination = '&after=' + str(response.json().get('pagination').get('cursor'))
            
            for user in json:
                f.write(str({
                    "id" : user.get('from_id'),
                    "user_login" : user.get('from_login'),
                    "followed_at" : user.get('followed_at')
                    }))
                f.write("\n")
                # print(i)
                i += 1
            print('Found ' + str(i) + ' followers for ' + username + '...')
        print('Writing total followers of ' + str(totalFollowers) + ' to file...')
        f.write('\nTotal followers: ' + str(totalFollowers))
        f.write('\nTotal time: ' + str(datetime.datetime.now() - startTime))
        f.close()
        
    getUserInput()
    print(datetime.datetime.now() - startTime)
except HTTPError as http_err:
    print(http_err)
except Exception as err:
    print(err)
