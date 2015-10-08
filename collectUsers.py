"""
Script for collecting usernames on github. This script will add duplicate usernames 
(check removed for efficiency). The resulting output text will be cleaned using another script for
removing duplicates.
"""
import requests
import json
import time

username = raw_input("Enter username: ")
password = raw_input("Enter password: ")
seed_id = raw_input("Select user id as seed for collecting users: ")


# GLOBALS
user_added_count = 0

# Open file in append mode
# This is the file where user_ids will be added
fhand = open("new_list.txt", "a")

def store_followers(user_id):
    """
    Extract 'login' of followers of a Github user and stores them to a txt file.
    For each user it extracts maximum 100 of the user's followers.
    
    Input : user_id string for a given user
    Output: String indicating success or failure in getting proper response from server
    """
    global user_added_count
    BASE_URL = 'https://api.github.com/users/'
    req_url = BASE_URL + user_id+ "/followers" + "?per_page=100"
    # make a request after a time gap of 0.25 seconds
    time.sleep(0.25)
    connect_timeout = 60.0
    try:
        followers_response = requests.get(req_url, auth=(username, password), timeout= connect_timeout)
    
    # for both connect and read timeouts
    except requests.exceptions.Timeout as e:
        print "Server seems to be too slow in responding. So exiting!"
        return "failed" 

    # print failure due to some other reason             
    except requests.exceptions.RequestException as e:
        print "Error:", e
        return "failed"

    if followers_response.status_code != 200:
        print "Github is fed up. Has kicked you out! Check your request url."
        return "failed"

    # get array of followers
    followers_array = json.loads(followers_response.text or followers_response.content)
    print "Number of followers of", user_id, ":", len(followers_array)

    for follower in followers_array:
        try:
            user_id = follower.get("login", None)
        except:
            print follower
        # if there is some user id we will add that to the follower list and
        # write to the file
        if user_id:
            user_added_count += 1
            fhand.write(user_id + "\n")
            print "User number " + str(user_added_count) + ": " + user_id

    return "success"

# Get number of followers of the seed
user_url = "https://api.github.com/users/" + seed_id    # url for getting details of the seed
user_detail_response = requests.get(user_url, auth=(username, password))
user_detail_dict = json.loads(user_detail_response.text or user_detail_response.content)
# number of followers of the seed
count_followers = user_detail_dict["followers"]
print "Number of Followers:", count_followers
# total number of pages to iterate provided there are 100 followers per pages
page_count = count_followers/100 + 1
# list of followers for seed
seed_followers_list = list()

for idx in range(1, page_count + 1):
    time.sleep(0.25)
    seed_req_url = "https://api.github.com/users/" + seed_id + "/followers?"+"page="+ str(idx) + "&per_page=100"
    try:
        seed_response = requests.get(seed_req_url, auth=(username, password))
    except requests.exceptions.RequestException as e:
        print e
    # extract array of followers here and add to the list of seed followers
    seed_array = json.loads(seed_response.text or seed_response.content)
    print "Adding new followers to seed from page number:" , str(idx)
    seed_followers_list += seed_array

print "Followers of seed:" , len(seed_followers_list)

# Follower number
count = 0
for seed_follower in seed_followers_list:
    user_id = seed_follower.get("login", None)
    if user_id:
        count += 1
        print "Looking up for max 100 followers of: " + str(user_id) + " whose # is " + str(count)
        print "---------------------------------------------"
        msg = store_followers(user_id)
        if msg == "failed":
            break

fhand.close()
# https://api.github.com/search/repositories?q=stars%3A%3E0&sort=stars&page=2&per_page=100
# Get commits : https://api.github.com/repos/apurushottam/Python-Codes/commits
# https://api.github.com/search/repositories?q=stars%3A%3E0&sort=stars&per_page=100
