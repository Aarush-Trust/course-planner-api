from fastapi import FastAPI #Main class to create web app
from app.routes.courses import router as courses_router #Shortens the course router name
from app.routes.sections import router as sections_router #Shortens the section router name
from app.routes.term import router as term_router #Shortens the term router name
from app.routes.schedules import router as schedules_router #Shortens the schedules router name

app = FastAPI ( #To create the web application
    title = "Course Planner API",
    description = "API for Waterloo-style course planning",
    version = "0.1.0"
)

app.include_router(courses_router) #Plugs in the router to the FastAPI
app.include_router(sections_router) #Plugs in the router to the FastAPI
app.include_router(term_router) #Plugs in the router to the FastAPI
app.include_router(schedules_router) #Plugs in the router to the FastAPI

@app.get("/health") #Responds to /health by running the function
def health_check():
    return {"status": "healthy", "message" : "Course API is Running"} #Returns JSON response