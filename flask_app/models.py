from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class HostLocationType(str, PyEnum):
    PUBLIC_PARK = "public_park"
    SCHOOL = "school"
    SHOPPING_AREA = "shopping_area"
    OTHER = "other"

class PlaygroundFeatureOrm(Base):
    __tablename__ = 'playground_features'
    id = Column(Integer, primary_key=True)
    primary_name = Column(String, nullable=False)
    aliases = Column(String, nullable=True)  # Store aliases as a comma-separated string

    @hybrid_property
    def aliases_set(self):
        return set(self.aliases.split(',')) if self.aliases else set()

    @aliases_set.setter
    def aliases_set(self, value):
        self.aliases = ','.join(value)

class AgeRangeOrm(Base):
    __tablename__ = 'age_ranges'
    id = Column(Integer, primary_key=True)
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)

class LocationOrm(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class AddressOrm(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)

class HostLocationOrm(Base):
    __tablename__ = 'host_locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Enum(HostLocationType), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    address = relationship("AddressOrm")
    location = relationship("LocationOrm")

class PlaygroundImageOrm(Base):
    __tablename__ = 'playground_images'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    taken_at = Column(DateTime, nullable=False)
    children_detected = Column(Boolean, nullable=False)
    needs_face_blurring = Column(Boolean, nullable=False)
    playground_id = Column(Integer, ForeignKey('playgrounds.id'))
    estimated_age_range_id = Column(Integer, ForeignKey('age_ranges.id'))
    estimated_age_range = relationship("AgeRangeOrm")
    features_detected = relationship("PlaygroundFeatureOrm", secondary='playground_image_features')

class PlaygroundOrm(Base):
    __tablename__ = 'playgrounds'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    host_location_id = Column(Integer, ForeignKey('host_locations.id'))
    host_location = relationship("HostLocationOrm")
    features = relationship("PlaygroundFeatureOrm", secondary='playground_features')
    images = relationship("PlaygroundImageOrm")
    recommended_age_range_id = Column(Integer, ForeignKey('age_ranges.id'))
    recommended_age_range = relationship("AgeRangeOrm")
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow)

# Create an engine and bind it to the Base
engine = create_engine('sqlite:///playgrounds.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
