from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from data_base.db_connection.db import Base

class Location(Base):
    __tablename__ = 'location'

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    country = Column(Integer, nullable=True)
    country_txt = Column(String, nullable=True)
    city = Column(String, nullable=True)
    region = Column(Integer, nullable=True)
    region_txt = Column(String, nullable=True)

    # הקשר חזרה ל-Event
    events = relationship("Event", back_populates="location")

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'country': self.country,
            'country_txt': self.country_txt,
            'city': self.city,
            'region': self.region,
            'region_txt': self.region_txt
        }

