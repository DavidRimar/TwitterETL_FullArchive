from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY, Float, JSON

Base = declarative_base()

"""
Tweet Class (extends Base class)
Representation of the data schema of 'Tweet' table in the PostgreSQL.
"""


class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    twitter_id = Column(String)  # (data.id)
    text = Column(String)  # (data.text)
    context_annotations = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime)  # (data.created_at)
    places_geo_place_id = Column(String)  # (includes.places.id)  
    stream_rule_tag = Column(String)  # (matching_rules.tag)

    # Constructor
    def __repr__(self):
        return "<Tweet(twitter_id='{}', text='{}', context_annotations={}, created_at={}, places_geo_place_id={}, stream_rule_tag={})>".format(self.twitter_id, self.text, self.context_annotations, self.created_at, self.places_geo_place_id, self.stream_rule_tag)

    
class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)  # Auto-generated ID
    places_geo_place_id = Column(String)  # (includes.places.id)
    places_geo_bbox = Column(ARRAY(Float))  # (includes.places.geo.bbox)
    places_full_name = Column(String)  # (includes.places.full_name)
    places_place_type = Column(String)  # (includes.places.place_type)
    places_country_code = Column(String)  # (includes.places.country_code)

    # Constructor
    def __repr__(self):
        return "<Tweet(places_geo_place_id={}, places_geo_bbox={}, places_full_name={}, places_place_type={}, places_country_code={})>".format(self.places_geo_place_id, self.places_geo_bbox, self.places_full_name, self.places_place_type, self.places_country_code)