from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time
from sqlmodel import SQLModel, Field

#To define shape of incoming data
class CourseCreate(BaseModel):
    code: str
    name: str
    credits: float

#To define what fields every course must follow (output)
class Course(BaseModel):
    #Following are used to validate the data provided
    id: int
    code: str
    name: str
    credits: float

#Term Model
class Term(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date

#Sections Model
class Section(BaseModel):
    id: int
    course_id: int
    term_id: int
    section_code: str
    days: List[str]
    start_time: time
    end_time: time
    location: Optional[str] = None

#To define shape of incoming data
class ScheduleCreate(BaseModel):
    term_id: int
    name: str
    section_ids: List[int]

#Schedule Model
class Schedule(BaseModel):
    id: int
    user_id: int
    term_id: int
    name: str
    section_ids: List[int]

#Check Conflicts
class ScheduleConflict(BaseModel):
    section_a_id: int
    section_b_id: int
    shared_days: List[str]