from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data_base.db_connection.db import Base

class Types(Base):
    __tablename__ = 'types'

    types_id = Column(Integer, primary_key=True, autoincrement=True)
    attacktype1 = Column(Integer, nullable=True)
    attacktype1_txt = Column(String, nullable=True)
    targtype1 = Column(Integer, nullable=True)
    targtype1_txt = Column(String, nullable=True)

    # הקשר חזרה ל-Event
    events = relationship("Event", back_populates="types")

    def to_dict(self):
        return {
            'attacktype1': self.attacktype1,
            'attacktype1_txt': self.attacktype1_txt,
            'targtype1': self.targtype1,
            'targtype1_txt': self.targtype1_txt
        }

