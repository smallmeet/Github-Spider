"""
Store here experimental short codes 
"""
import requests
import json
import time

# enter user name and password for making API request with permission
username = raw_input("Enter username: ")
password = raw_input("Enter password: ")

# Extract commits for a repository and for each commit extract commiter, date
commit_url = "https://api.github.com/repos/apurushottam/Python-Codes/commits"
connect_timeout = 60.0

try:
	response = requests.get(commit_url, auth=(username, password), timeout=connect_timeout)

except requests.exceptions.Timeout as e:
	print "Server seems to be too slow in responding.", e

except requests.exceptions.RequestException as e:
	print "Some error:", e

if response.status_code != 200:
	print "Invalid response from server. Exiting!", str(response.status_code)

iteration = 0
info_array = json.loads(response.text or seed_response.content) # array of ditionaries
for info_dict in info_array:
	iteration += 1
	# get commit dictionary from info_dit
	commit_dict = info_dict["commit"]
	# get commiter dictionary from commit_dict
	commiter_dict = commit_dict["committer"]
	print "Iteration number", iteration
	print "Commiter name:", commiter_dict["name"]
	print "Commiter email: ", commiter_dict["email"]
	print "Commit date: ", str(commiter_dict["date"])
# info_dict = info_array[0]
# commit_dict_aray = info_dict["commit"]
# print ""

# iteration = 0
# for commit_dict in commit_dict_aray:
# 	print commit_dict
	# get commiter info dictionary
	# iteration += 1
	# commiter_info_dict = commit_dict["commiter"]
	# print "Iteration number " + str(iteration) + " commiter name: " + commiter_info_dict["name"]
	# print "Iteration number " + str(iteration) + " email: " + commiter_info_dict["email"]
	# print "Iteration number " + str(iteration) + " date: " + str(commiter_info_dict["date"])

