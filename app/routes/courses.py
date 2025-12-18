from fastapi import APIRouter, HTTPException #To prevent overloading and errors
from typing import List, Optional
from app.models import Course, CourseCreate

router = APIRouter( #Beginning and grouping all routes
    prefix = "/courses",
    tags = ["Courses"]
)

#TEMPORARY SETUP
fake_courses = [
Course(id = 1, code = "ECE 150", name = "Intro to Programming", credits = 0.50),
Course(id = 2, code = "ECE 105", name = "Classical Mechanics", credits = 0.5)
]

#When sent Get/courses - calls list_courses
@router.get("/", response_model = list[Course], 
            summary = "List all courses (optionally filter by code).")
def list_courses(code: Optional[str] = None): #Returns the fake_courses list
    if code is None:
        return fake_courses
    #Makes a filtered list of the courses searched for (makes sure case doesnt matter)
    filtered = [ course for course in fake_courses
                 if course.code.lower() == code.lower()]
    return filtered

#Handles the request for POST/course and has the default API status_code (201 = "Created")
@router.post("/", response_model = Course, status_code = 201)
def create_course(payload: CourseCreate): #To create courses from user (stores info in payload)
    new_ID = len(fake_courses) + 1  #Decide the new ID = 1 + current max

    course = Course(
        id = new_ID,
        code = payload.code,
        name = payload.name,
        credits = payload.credits
    )
    fake_courses.append(course) #Adds the new course to the previous list
    return course

@router.get("/{course_id}", response_model = Course) #Handles the request to search ID
#Takes the input as a parameter and loops through the courses and returns the desired course
def get_course(course_id: int):
    for course in fake_courses:
        if course.id == course_id:
            return course
        raise HTTPException(status_code = 404, detail = {"code": "MISSING COURSE",
                                                         "message": "Course not found"})