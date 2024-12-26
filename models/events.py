from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from data_base.db_connection.db import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    summary = Column(String, nullable=True)
    gname = Column(String, nullable=True)
    killed = Column(Float, nullable=True)
    wounded = Column(Float, nullable=True)
    nperps = Column(Float, nullable=True)
    location_id = Column(Integer, ForeignKey('location.location_id'))
    types_id = Column(Integer, ForeignKey('types.types_id'))

    # הקישורים ב-back_populates לא בהכרח צריכים להיות הפוך, רק לבדוק אם הם מוגדרים כראוי.
    location = relationship("Location", back_populates="events")
    types = relationship("Types", back_populates="events")

    def to_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'summary': self.summary,
            'gname': self.gname,
            'killed': self.killed,
            'wounded': self.wounded,
            'nperps': self.nperps,
            'location': self.location.to_dict() if self.location else None,
            'types': self.types.to_dict() if self.types else None
        }
