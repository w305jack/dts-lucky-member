from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
import datetime
import uuid




class Members(Base):
    __tablename__ = 'members'

    id = Column(String(50), primary_key=True)
    name = Column(String(50), unique=True)
    created_time = Column(DateTime(), nullable=False)
    modified_time = Column(DateTime(), nullable=False)

    def __init__(self, name, description=None, site_url=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_time = datetime.datetime.now()
        self.modified_time = datetime.datetime.now()

    def __repr__(self):
        return '<Member %r>' % (self.name)
