from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Section

router = APIRouter(
    prefix="/sections",
    tags=["Sections"],
)

#Hypothetical data
fake_sections: List[Section] = [
    Section(
        #ECE 150, Winter 2026
        id = 1,
        course_id = 1,
        term_id = 1,
        section_code = "LEC 001",
        days = ["MON", "WED"],
        start_time = "10:30",
        end_time = "11:20",
        location = "RCH 101",
    ),

    Section(
        #ECE 105, Winter 2026
        id = 2,
        course_id = 2,
        term_id = 1,
        section_code = "LEC 002",
        days = ["MON", "WED"],
        start_time = "10:30",
        end_time = "11:20",
        location = "RCH 105",
    )
]

#Returns List of Sections
@router.get("/", response_model=List[Section],
            summary = "List all sections for debugging / selection.")
def list_sections():
    return fake_sections

@router.get("/{section_id}", response_model = Section) #Returns the section asked
def get_section(section_id: int):
    for section in fake_sections:
        if section.id == section_id:
            return section
    raise HTTPException(status_code = 404, detail = {"code": "MISSING SECTION",
                                                    "message": "Section not found"})