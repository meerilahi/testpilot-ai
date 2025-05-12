from sqlalchemy import Column, Integer, String, ForeignKey, Text
from database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    total_pages = Column(Integer)

class NotePage(Base):
    __tablename__ = "note_pages"
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(String, ForeignKey("notes.id"))
    page_number = Column(Integer)
    content = Column(Text)
