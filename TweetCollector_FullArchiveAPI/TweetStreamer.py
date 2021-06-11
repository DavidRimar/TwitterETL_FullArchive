import sys
import requests
import os
import json
from TweetCollector_FullArchiveAPI.TweetLoader import TweetLoader
import time


class TweetStreamer:

    # ======== CONSTRUCTOR
    def __init__(self, bearer_token, database_url):

        # ======== INSTANCE VARIABLES
        self.authentication_header = self.create_headers(bearer_token)
        
        self.tweet_loader = TweetLoader(database_url)

    # ======== METHODS
    """
    Creates a key-value pair for authorization
    """
    def create_headers(self, bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    
    """
    Makes a GET request and returns the streaming rules
    """
    def get_tweets(self, start_time, end_time, query, recreate_db=False, max_tweets=10):

        # boolean for search end
        search_finished = False
        
        # variable to count pages
        result_page = 1
        
        # next_token
        # next_token = None # ""
        
        # define Twitter endpoint
        full_archive_endpoint = "https://api.twitter.com/2/tweets/search/all"

        # set start and end time
        #start_time = "2021-04-01T00:00:00Z"
        #end_time = "2021-04-04T00:00:00Z"

        # describe the search with a tag
        query_tag = "GENERAL"
        
        # set query parameters to e sent as part of the GET request
        query_params = {
            'query': query,
            'max_results': f'{max_tweets}',
            'start_time': start_time,
            'end_time': end_time,
            'tweet.fields': 'id,created_at,geo,context_annotations',
            'expansions': 'geo.place_id',
            'place.fields': 'country,country_code,full_name,geo,id,name,place_type'}

        # WHILE LOOP
        while (search_finished == False):
            
            # DO ALL THE STREAMING STUFF

            # make the code sleep for 1 minute before making a new request
            time.sleep(11)
            
            # GET request (query = params)
            response = requests.request(
                "GET", full_archive_endpoint, headers=self.authentication_header, params=query_params)

            # confirm if request has gone through
            print("HTTP Response: ", response.status_code)

            # raise exception if not
            if response.status_code != 200:
                raise Exception(
                    "Cannot get stream (HTTP {}): {}".format(
                        response.status_code, response.text
                    )
                )

            # use tweetloader object to transform and load the data to db
            for response_line in response.iter_lines():

                # response_line exists
                if response_line:

                    # convert json to python dict
                    json_response = json.loads(response_line)

                    # print response (optional)
                    print("PAGE: ", result_page)
                    print("JSON response meta:\n", json_response["meta"])
                    
                    # CHECK IF THE meta.next_token DOES NOT exists
                    if "next_token" not in json_response["meta"]:
                        
                        print("There is NO next token!")
                        
                        # if so, set search_finished == True
                        search_finished = True
                        
                    else:
                        
                        # print("There is a new next token!")
                        result_page += 1
                        
                        # set the next_token to be queried in the new GET request
                        next_token = json_response["meta"]["next_token"]
                        
                        # add next_token to query parameters
                        query_params["next_token"] = next_token
                        
                    # load json response to db
                    self.tweet_loader.transform_and_load(json_response, query_tag, recreate_db)
