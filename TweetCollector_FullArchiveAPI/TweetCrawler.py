from sqlalchemy import create_engine
from datetime import datetime
from TweetCollector_FullArchiveAPI.Tables import Base, Tweet, Place
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from contextlib import contextmanager
import json

"""
The TweetCrawler class is responsible for query the DB.
"""


class TweetCrawler():

    ### CONSTRUCTOR ###
    def __init__(self, database_url):

        ### INSTANCE VARIABLES ###

        # an engine to communicate with PostgreSQL
        self.engine = create_engine(database_url)

        # a Session object to manage connections (session starts)
        self.Session = sessionmaker(bind=self.engine)

    ### METHODS ###

    # 1. crawl_data()
    # 2. session_scope()

    """
    Queries Data from the database, with an SQL statement
    as an argument as string.
    """
    # 1.

    def crawl_data_with_session(self, statement):

        # query to be returned
        # query_object = None
        
        # connect to DB with session
        with self.session_scope() as s:

            try:
                # use session to execute statement
                query_result = s.query(Tweet).all()
                
                print("Query successful!")
                
                return query_result

            except:
                print("Error in the query!")

        # return the query object
        # return query_object
        
        
        """
    Queries Data from the database, with an SQL statement
    as an argument. (With connection)
    """
    # 1.

    def crawl_data_with_connection(self, statement):

        # query to be returned
        # query_object = None
        
        with self.engine.connect() as con:

            try:
                
                query_result = con.execute(statement)
                        
                print("Query successful!")
                
                return query_result

            except:
                print("Error in the query!")
                
        # return the query object
        # return query_object
                
    """
    A context manager for the session. 
    It ensures that all connections are closed.
    """
    # 2.
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
