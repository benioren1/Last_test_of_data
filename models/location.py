from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from data_base.db_connection.db import Base


class Location(Base):
    __tablename__ = 'location'
    Event_id = Column(Integer, ForeignKey('Event.id'), primary_key=True)
    latitude = Column(Float,nullable=True)
    longitude = Column(Float,nullable=True)
    country = Column(Integer,nullable=True)
    country_txt = Column(String,nullable=True)
    city = Column(String,nullable=True)
    region = Column(Integer,nullable=True)
    region_txt = Column(String,nullable=True)
    event = relationship("Event", backref="event_loc", uselist=False)


    def to_dict(self):
        return {
            'Event_id': self.Event_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'country': self.country,
            'country_txt': self.country_txt,
            'region': self.region,
            'region_txt': self.region_txt
        }



