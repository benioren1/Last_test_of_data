from sqlalchemy import Column, Integer, String, Float,relationship

from data_base.db_connection.db import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    iyear = Column(Integer,nullable=True)
    imonth = Column(Integer,nullable=True)
    iday = Column(Integer,nullable=True)
    summary = Column(String,nullable=True)
    gname = Column(String,nullable=True)
    nkill = Column(Integer,nullable=True)
    nwound = Column(Integer,nullable=True)
    nperps = Column(Integer,nullable=True)
    location = relationship("Location", backref="event_loc", uselist=False)
    types = relationship("Types", backref="event_types", uselist=False)


    def to_dict(self):
        return {
            'id': self.id,
            'iyear': self.iyear,
            'imonth': self.imonth,
            'iday': self.iday,
            'summary': self.summary,
            'gname': self.gname,
            'nkill': self.nkill,
            'nwound': self.nwound,
            'nperps': self.nperps,
            'location': self.location.to_dict() if self.location else None,
            'types': self.types.to_dict() if self.types else None
        }



