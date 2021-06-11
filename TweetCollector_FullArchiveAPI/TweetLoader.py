from sqlalchemy import create_engine
from datetime import datetime
from TweetCollector_FullArchiveAPI.Tables import Base, Tweet, Place
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import json

"""
The TweetLoader class takes care of transforming the fields from the response
objects to adhere to the data schema represented by the Tweet class.
It uses sqlAlchemy to load the tweets to a DB.
"""
class TweetLoader():

     ### CONSTRUCTOR ###
    def __init__(self, database_url):

         ### INSTANCE VARIABLES ###

        self.recreated_tables = False

        # an engine to communicate with PostgreSQL
        self.engine = create_engine(database_url)

        # a Session object to manage connections (session starts)
        self.Session = sessionmaker(bind=self.engine)

    ### METHODS ###

    # 1. start_load()
    # 2. transform_and_load()
    # 3. recreate_database()
    # 4. session_scope()

    """
    It handles the actual data loading into the DB. 
    It is called by the transform_and_load() method.
    """
    # START LOAD
    # 1.
    def start_load(self, tweet_to_add, recreate_db):

        # print("Transformasion okay! Loading to start!")

        # if only interested in the new data, recreate_db deletes data streamed before
        if recreate_db == True and self.recreated_tables == False:
            
            self.recreate_database()
            
            print("Recreate db ran!")
            
            self.recreated_tables = True

        # connect to DB with session
        with self.session_scope() as s:

            # add tweet to DB
            try:
                s.add(tweet_to_add)
                # print("Tweet Loading Successful!")
            except:
                print("Error in Loading!")

    
    """
    Transforms the received JSON response to abide the data schema in line
    with what's defined in the Tweet object.
    """
    # TRANSFORM AND LOAD
    # 2.
    def transform_and_load(self, json_response, query_tag, recreate_db):

        # inspect response line (optional)
        # print("json printed: ", json.dumps(json_response, indent=4, sort_keys=True))

        # i = 0

        tweet_place_id = ""
        tweet_place_geo_bbox = []
        tweet_place_full_name = ""
        tweet_place_type = ""
        tweet_country_code = ""
        rule_tag = query_tag

        # for every tweet (data_item is a tweet)
        for data_item in json_response["data"]:

            ### TWEET FIELDS
            tweet_id = data_item["id"]
            tweet_text = data_item["text"]
            tweet_created_at = data_item["created_at"]
            tweet_place_id = data_item["geo"]["place_id"]
            
            context_domain_array = [] # array to collect context_annotations
    
            ### CONTEXT_ANNOTATIONS: 
            # if there is a context_annotations array
            if "context_annotations" in data_item:
                # for each domain annotation
                for annotation in data_item["context_annotations"]:
                    # append it to local variable
                    context_domain_array.append(annotation["domain"]["name"])
                    
            # if there is no context_annotations   
            else:
                # make it NULL
                # print("context_annotation is null")
                context_domain_array = None

            # includes_i = 0
            
            ### PLACES
            # Places for loop (includes.places)
            for includes_item in json_response["includes"]["places"]:

                if (includes_item["id"] == tweet_place_id):

                    tweet_place_geo_bbox = includes_item["geo"]["bbox"]
                    tweet_place_full_name = includes_item["full_name"]
                    tweet_place_type = includes_item["place_type"]
                    tweet_country_code = includes_item["country_code"]

                # increment includes_i
                # includes_i += 1

            ### CONSTRUCT TWEET (for tweet and place)
            # construct tweet_data_dict (for each data_item)
            """
            tweet_data_dict = {'twitter_id': tweet_id,
                               'text': tweet_text,
                               'context_annotations': context_domain_array,
                               'created_at': tweet_created_at,
                               'places_geo_place_id': tweet_place_id,
                               'places_geo_bbox': tweet_place_geo_bbox,
                               'places_full_name': tweet_place_full_name,
                               'places_place_type': tweet_place_type,
                               'places_country_code': tweet_country_code,
                               'stream_rule_tag': rule_tag}
            """
            tweet_data_dict = {'twitter_id': tweet_id,
                               'text': tweet_text,
                               'context_annotations': context_domain_array,
                               'created_at': tweet_created_at,
                               'places_geo_place_id': tweet_place_id,
                               'stream_rule_tag': rule_tag}
            
            place_data_dict = {'places_geo_place_id': tweet_place_id,
                               'places_geo_bbox': tweet_place_geo_bbox,
                               'places_full_name': tweet_place_full_name,
                               'places_place_type': tweet_place_type,
                               'places_country_code': tweet_country_code}

            # construct a Tweet() object
            # data passed in to Tweet() has to be in a dictionary format
            single_tweet = Tweet(**tweet_data_dict)
            
            single_place = Place(**place_data_dict)

            # inspect transformed Tweet() object
            # print("single_tweet: ", single_tweet)

            ### LOAD TWEETs and PLACEs
            self.start_load(single_tweet, recreate_db)
            
            self.start_load(single_place, recreate_db)

            # increment i
            # i += 1

   
    """
    Recreates the database. It drops all tables and creates them again.
    If run for the first time, set this as true.
    """
    # RECREATE DATABASE
    # 3.
    def recreate_database(self):

        # drops all tables
        Base.metadata.drop_all(self.engine)

        # creates all tables
        Base.metadata.create_all(self.engine)

    
    """
    A context manager for the session. 
    It ensures that all connections are closed.
    """
    # A CONTEXT MANAGER
    # 4.
    @ contextmanager
    def session_scope(self):

        # local scope creates and uses a session
        session = self.Session()  # invokes sessionmaker.__call__()

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
