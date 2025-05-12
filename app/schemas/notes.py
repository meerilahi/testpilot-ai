from pydantic import BaseModel
from typing import List, Tuple, Optional
from pydantic import Field

class NotesInfo(BaseModel):
    notes_id: str
    title: str
    length: int 

class NotesInfoList(BaseModel):
    notes: List[NotesInfo]