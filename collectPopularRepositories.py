"""
Script for collecting most popular repositories on github (in terms of number of
times the repositories have been starred, forked and number of commits).
The repository full name is being extracted here
"""
import requests
import json
import time

# enter user name and password for making API request with permission
username = raw_input("Enter username: ")
password = raw_input("Enter password: ")


# open file in append mode
try:
    fhand = open("repo_list.txt", "a")
except:
    print "Could not open file. Check file name in code."

repo_count = 0
# Example hit: https://api.github.com/search/repositories?q=stars%3A%3E0&sort=stars&page=2&per_page=100

def fetch_repos_stars(criteria):
    """
    Fetches 1000 most starred repository's full name and writes it to the external file
    (Only the first 1000 search results are available.)
    Input: Criteria a string indicating on what criteria the repositories should be fetched
    """
    global repo_count

    # we will make iternations for the first 20 pages with each page consisting of 100 search results
    for page_number in range(1, 11):
        req_url_stars = "https://api.github.com/search/repositories?q="+ criteria+ "%3A%3E0&sort=" +criteria+"&"\
            + "page=" + str(page_number)+ "&per_page=100"+"&format=json"

        connect_timeout = 60.0

        try:
            response = requests.get(req_url_stars, auth=(username, password), timeout=connect_timeout)
        except requests.exceptions.Timeout as e:
            print "Server seems to be too slow in responding. So exiting!", e
            break
        except requests.exceptions.RequestException as e:
            print "Some error:", e
            break

        if response.status_code != 200:
            print "Invalid response from server. Exiting!", str(response.status_code)
            break

        # parse response into a dictioanry
        response_dictionary = json.loads(response.text or response.content)
        # count of results returned
        count_results = response_dictionary["total_count"]
        # we dont want to hit server if the hit is above the max value we can get
        if page_number >= count_results/100 + 2:
            print "Exiting so as to not to cross maximum allowed results"
            return
        # extract array of repositories from the dictionary
        repos_array = response_dictionary["items"]

        for repo in repos_array:
            repo_count += 1
            repo_full_name = repo["full_name"]
            fhand.write(repo_full_name + "\n")
            print "Adding repository number " + str(repo_count) + ": " + repo_full_name


fetch_repos_stars("size")
fetch_repos_stars("stars")
fetch_repos_stars("forks")
fetch_repos_stars("commits")

fhand.close()

