from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from data_base.db_connection.db import Base


class Types(Base):
    __tablename__ = 'types'
    Event_id = Column(Integer, ForeignKey('Event.id'), primary_key=True)
    attacktype1 = Column(Integer,nullable=True)
    attacktype1_txt = Column(String,nullable=True)
    targtype1 = Column(Integer,nullable=True)
    targtype1_txt = Column(String,nullable=True)
    event = relationship("Event", backref="event_type", uselist=False)

    def to_dict(self):
        return {
            'Event_id': self.Event_id,
            'attacktype1': self.attacktype1,
            'attacktype1_txt': self.attacktype1_txt,
            'targtype1': self.targtype1,
            'targtype1_txt': self.targtype1_txt
        }

