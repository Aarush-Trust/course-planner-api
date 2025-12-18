from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Schedule, ScheduleCreate, Section, ScheduleConflict
from app.routes.sections import fake_sections
from datetime import time

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"],
)

#Hypothetical DataBase
fake_schedules: List[Schedule] = []

@router.get("/", response_model=List[Schedule])
def list_schedules():
    return fake_schedules


def sections_overlap(sec_a: Section, sec_b: Section) -> bool:
    #Only compare if they share at least one day
    shared_days = set(sec_a.days) & set(sec_b.days)
    if not shared_days:
        return False
    
    start_a = sec_a.start_time
    end_a = sec_a.end_time
    start_b = sec_b.start_time
    end_b = sec_b.end_time
    #Checks if the times overlap 
    return start_a < end_b and start_b < end_a


@router.post("/", response_model=Schedule, status_code=201, 
    summary="Create a schedule",
    description=(
    "Create a schedule for a given term with a set of section IDs. "
    "Validates that all sections exist, belong to the term, and do not have time conflicts.")
    )


def create_schedule(payload: ScheduleCreate):
    #Gather the Sections for the given ID
    selected_sections = []
    for sid in payload.section_ids:
        match = next((s for s in fake_sections if s.id == sid), None)
        if match is None:
            raise HTTPException(status_code=400, 
                                detail={ "code": "SECTION_NOT_FOUND",
                                "message": f"Section with id {sid} does not exist",})
        selected_sections.append(match)

    #Check Section in Term
    for s in selected_sections:
        if s.term_id != payload.term_id:
            raise HTTPException(status_code=400,
            detail={"code": "SECTION_TERM_MISMATCH",
        "message": f"Section {s.id} belongs to term {s.term_id}, not term {payload.term_id}",
    }
            )
    
    #Checks for any time conflicts
    conflicts = []
    n = len(selected_sections)
    for i in range(n):
        for j in range(i + 1, n):
            a = selected_sections[i]
            b = selected_sections[j]
            if sections_overlap(a, b):
                conflicts.append(
                    {
                        "section_a_id": a.id,
                        "section_b_id": b.id,
                        "shared_days": list(set(a.days) & set(b.days)),
                    }
                )
    if conflicts:
        raise HTTPException(
            status_code=400,
            detail={
            "code": "TIME_CONFLICT",
            "message": "Time conflicts detected between sections",
            "conflicts": conflicts,
        }
        )
    
    #Validation Passes, then create schedule
    new_id = len(fake_schedules) + 1
    schedule = Schedule(
        id = new_id,
        user_id = 1, #TEMPORARY
        term_id = payload.term_id,
        name = payload.name,
        section_ids = payload.section_ids
    )
    fake_schedules.append(schedule)
    return schedule


@router.get("/{schedule_id}", response_model = Schedule)
def get_schedule(schedule_id: int):
    for schedule in fake_schedules:
        if schedule.id == schedule_id:
            return schedule
    raise HTTPException(status_code = 404, detail = {"code": "MISSING SCHEDULE",
                                                    "message": "Schedule not found"})


@router.post("/check-conflicts", response_model=List[ScheduleConflict],
            summary = "Check for time conflicts between a list of sections before creating a schedule.")
def check_conflicts(section_ids: List[int]):
    selected_sections = []
    for sid in section_ids:
        match = next((s for s in fake_sections if s.id == sid), None)
        if match is None:
            raise HTTPException(status_code=400,
                                detail=f"Section with id {sid} does not exist",)
        selected_sections.append(match)


    conflicts: List[ScheduleConflict] = []
    n = len(selected_sections)
    for i in range(n):
        for j in range(i + 1, n):
            a = selected_sections[i]
            b = selected_sections[j]
            if sections_overlap(a, b):
                conflicts.append(
                    ScheduleConflict(
                        section_a_id=a.id,
                        section_b_id=b.id,
                        shared_days=list(set(a.days) & set(b.days)),
                    )
                )
    return conflicts